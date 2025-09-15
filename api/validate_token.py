import logging
import os
import uuid

import requests
from dotenv import load_dotenv

from api.logging_config import get_logger

load_dotenv()

# use the shared LoggerAdapter so request_id is injected automatically
logger = get_logger(__name__)
LBG_SUBSCRIPTION_KEY = os.getenv("LBG_SUBSCRIPTION_KEY")
LBG_API_BASE_URL = os.getenv("LBG_API_BASE_URL")
LBG_API_ENV = os.getenv("LBG_API_ENV")
PROD_STATUS = os.getenv("PROD_STATUS")


def validate_token(token):

    halifax_url = "https://mortgages.secure.halifax-online.co.uk/homes/external-apis/sustainability/v1/epc/token"

    lloyds_url = "https://mortgages.secure.lloydsbank.co.uk/home/external-apis/sustainability/epc/token"

    url = halifax_url

    correlation_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())

    headers = {
        "x-correlation-id": correlation_id,
        "x-session-id": session_id,
        "Ocp-Apim-Subscription-Key": LBG_SUBSCRIPTION_KEY,
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "User-Agent": "e.surv-user",
        "origin": "https://lbg-epc.esurv.co.uk/",
        "Referer": "https://lbg-epc.esurv.co.uk/",
    }

    data = {"token": token}

    try:
        logger.debug(
            "validate_token.call_start", extra={"url": url, "session_id": session_id}
        )
        response = requests.put(url, headers=headers, json=data, verify=False)

        logger.info(
            "validate_token.call_finished",
            extra={"status_code": getattr(response, "status_code", None)},
        )

        if response.status_code == 200:
            json_response = response.json()
            status = json_response.get("status")
            logger.info("validate_token.success", extra={"status": status})
            return status  # Expected values: 'valid', 'invalid', 'expired', 'used'
        else:
            try:
                json_response = response.json()
                errors = json_response.get("errors", [])
                error_messages = "; ".join(
                    [f"{error.get('code')}: {error.get('message')}" for error in errors]
                )
            except Exception:
                error_messages = response.text if hasattr(response, "text") else None
            logger.warning(
                "validate_token.error_response",
                extra={"status_code": response.status_code, "errors": error_messages},
            )
            return f"Error {response.status_code}: {error_messages}"
    except Exception as e:
        logger.exception("validate_token.exception", extra={"url": url})
        return f"Exception occurred: {str(e)}"
