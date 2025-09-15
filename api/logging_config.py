import json
import logging
import os
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    def format(self, record):
        message = record.getMessage()
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": message,
        }

        for k, v in record.__dict__.items():
            if k in (
                "name",
                "msg",
                "args",
                "levelname",
                "levelno",
                "pathname",
                "filename",
                "module",
                "exc_info",
                "exc_text",
                "stack_info",
                "lineno",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "processName",
                "process",
            ):
                continue
            if k.startswith("_"):
                continue
            try:
                json.dumps(v)
                log_record[k] = v
            except (TypeError, ValueError):
                # Handle non-serializable objects gracefully
                log_record[k] = repr(v) if hasattr(v, '__repr__') else str(type(v))

        if record.exc_info:
            try:
                exc_type = (
                    record.exc_info[0].__name__
                    if record.exc_info[0] is not None
                    else None
                )
            except (AttributeError, TypeError):
                exc_type = (
                    str(record.exc_info[0]) if record.exc_info[0] is not None else None
                )
            try:
                exc_message = (
                    str(record.exc_info[1]) if record.exc_info[1] is not None else None
                )
            except (AttributeError, TypeError):
                exc_message = None
            log_record["error"] = {"type": exc_type, "message": exc_message}
            try:
                log_record["stack"] = self.formatException(record.exc_info)
            except (AttributeError, TypeError, ValueError):
                log_record["stack"] = "Stack trace unavailable"

        return json.dumps(log_record, default=str)


def configure_root_logger():
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Validate log level
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if LOG_LEVEL not in valid_levels:
        LOG_LEVEL = "INFO"
        print(f"Warning: Invalid LOG_LEVEL, defaulting to INFO. Valid levels: {valid_levels}")
    
    service_name = os.getenv("SERVICE_NAME", "lbg-epc")
    env_name = os.getenv("ENV", "dev")

    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())

    root_logger = logging.getLogger()
    
    # More robust handler management
    existing_handlers = [h for h in root_logger.handlers if isinstance(h, logging.StreamHandler)]
    if not existing_handlers:
        root_logger.addHandler(handler)
    elif not any(isinstance(h.formatter, JSONFormatter) for h in existing_handlers):
        # Replace non-JSON handlers
        for handler_to_remove in existing_handlers:
            root_logger.removeHandler(handler_to_remove)
        root_logger.addHandler(handler)
    
    root_logger.setLevel(LOG_LEVEL)

    class ContextFilter(logging.Filter):
        def filter(self, record):
            record.service = service_name
            record.env = env_name
            return True
    
    # Only add filter if not already present
    context_filter = ContextFilter()
    if not any(isinstance(f, ContextFilter) for f in root_logger.filters):
        root_logger.addFilter(context_filter)


configure_root_logger()


class RequestIdAdapter(logging.LoggerAdapter):
    """LoggerAdapter that injects request_id from Flask's `g` when available."""

    def process(self, msg, kwargs):
        extra = kwargs.setdefault("extra", {})
        # only import flask.g at runtime to avoid hard dependency outside request contexts
        try:
            from flask import g

            request_id = getattr(g, "request_id", None)
        except (ImportError, RuntimeError, AttributeError):
            # ImportError: Flask not available
            # RuntimeError: Outside application context
            # AttributeError: g doesn't exist
            request_id = None
        
        # Only set if not already provided by caller
        if "request_id" not in extra:
            extra["request_id"] = request_id
        
        return msg, kwargs


def get_logger(name: str | None = None) -> logging.LoggerAdapter:
    """Return a LoggerAdapter that automatically injects request_id into log calls.

    Usage:
        logger = get_logger(__name__)
        logger.info("something happened")  # will include request_id in extra
    """
    base = logging.getLogger(name)
    return RequestIdAdapter(base, {})
