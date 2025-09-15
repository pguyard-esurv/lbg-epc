import json
import logging
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

from api import logging_config


def test_json_formatter_outputs_json_and_includes_timestamp_and_level(caplog):
    logger = logging.getLogger("test_logger")
    handler = logging.StreamHandler()
    formatter = logging_config.JSONFormatter()
    handler.setFormatter(formatter)
    logger.handlers = []
    logger.addHandler(handler)
    logger.setLevel("INFO")

    with caplog.at_level(logging.INFO):
        logger.info("smoke test message", extra={"foo": "bar"})

    # caplog.records contains the LogRecord object; format it using our formatter
    assert caplog.records
    rec = caplog.records[0]
    formatted = formatter.format(rec)
    parsed = json.loads(formatted)
    assert parsed.get("message") == "smoke test message"
    assert parsed.get("level") == "INFO"
    assert "timestamp" in parsed
    assert parsed.get("foo") == "bar"
    # Test that timestamp is in ISO format with timezone
    timestamp = parsed.get("timestamp")
    assert timestamp.endswith("+00:00") or timestamp.endswith("Z")
    # Should be parseable as ISO datetime
    datetime.fromisoformat(timestamp.replace("Z", "+00:00"))


def test_request_id_adapter_injects_request_id(monkeypatch, caplog):
    # create a dummy g with request_id
    class DummyG:
        request_id = "test-req-123"

    def fake_get_g():
        return DummyG()

    # monkeypatch flask.g access by stubbing in a module with g attribute
    monkeypatch.setitem(
        __import__("sys").modules, "flask", type("m", (), {"g": DummyG})
    )

    logger = logging_config.get_logger("adapter_test")
    formatter = logging_config.JSONFormatter()
    logger.logger.handlers = []
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.logger.addHandler(handler)
    logger.logger.setLevel("INFO")

    with caplog.at_level(logging.INFO):
        logger.info("adapter message")

    assert caplog.records
    rec = caplog.records[0]
    # format via JSONFormatter to get the JSON output
    formatted = formatter.format(rec)
    parsed = json.loads(formatted)
    assert parsed.get("message") == "adapter message"
    assert parsed.get("request_id") == "test-req-123"


def test_json_formatter_handles_non_serializable_objects(caplog):
    logger = logging.getLogger("test_logger")
    handler = logging.StreamHandler()
    formatter = logging_config.JSONFormatter()
    handler.setFormatter(formatter)
    logger.handlers = []
    logger.addHandler(handler)
    logger.setLevel("INFO")

    class NonSerializable:
        def __repr__(self):
            return "NonSerializable()"

    with caplog.at_level(logging.INFO):
        logger.info("test message", extra={"obj": NonSerializable()})

    rec = caplog.records[0]
    formatted = formatter.format(rec)
    parsed = json.loads(formatted)
    assert parsed.get("obj") == "NonSerializable()"


def test_json_formatter_handles_exception_info(caplog):
    logger = logging.getLogger("test_logger")
    handler = logging.StreamHandler()
    formatter = logging_config.JSONFormatter()
    handler.setFormatter(formatter)
    logger.handlers = []
    logger.addHandler(handler)
    logger.setLevel("ERROR")

    try:
        raise ValueError("test error")
    except ValueError:
        with caplog.at_level(logging.ERROR):
            logger.exception("An error occurred")

    rec = caplog.records[0]
    formatted = formatter.format(rec)
    parsed = json.loads(formatted)
    assert parsed.get("message") == "An error occurred"
    assert "error" in parsed
    assert parsed["error"]["type"] == "ValueError"
    assert parsed["error"]["message"] == "test error"
    assert "stack" in parsed


def test_request_id_adapter_handles_no_flask_context():
    # Test when Flask g is not available
    logger = logging_config.get_logger("test")
    formatter = logging_config.JSONFormatter()
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.logger.handlers = []
    logger.logger.addHandler(handler)
    logger.logger.setLevel("INFO")

    # This should not raise an exception even without Flask context
    try:
        logger.info("test message")
    except Exception as e:
        assert False, f"Logger should handle missing Flask context gracefully: {e}"


def test_request_id_adapter_preserves_user_provided_request_id(monkeypatch, caplog):
    # Test that user-provided request_id is not overridden
    class DummyG:
        request_id = "auto-generated-id"

    monkeypatch.setitem(
        __import__("sys").modules, "flask", type("m", (), {"g": DummyG})
    )

    logger = logging_config.get_logger("adapter_test")
    formatter = logging_config.JSONFormatter()
    logger.logger.handlers = []
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.logger.addHandler(handler)
    logger.logger.setLevel("INFO")

    with caplog.at_level(logging.INFO):
        logger.info("test message", extra={"request_id": "user-provided-id"})

    rec = caplog.records[0]
    formatted = formatter.format(rec)
    parsed = json.loads(formatted)
    # Should use the user-provided ID, not the auto-generated one
    assert parsed.get("request_id") == "user-provided-id"


def test_configure_root_logger_validates_log_level():
    # Test invalid log level handling
    with patch.dict("os.environ", {"LOG_LEVEL": "INVALID"}, clear=False):
        with patch("builtins.print") as mock_print:
            logging_config.configure_root_logger()
            mock_print.assert_called_once()
            assert "Invalid LOG_LEVEL" in mock_print.call_args[0][0]


def test_get_logger_returns_adapter():
    logger = logging_config.get_logger("test")
    assert isinstance(logger, logging_config.RequestIdAdapter)
    assert isinstance(logger.logger, logging.Logger)
