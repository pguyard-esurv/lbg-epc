import json
import logging
import os

import requests
import sentry_sdk
from dotenv import load_dotenv

from logging_config import get_logger

load_dotenv()

# Safe environment reads
EHOUSE_USERNAME = os.getenv("EHOUSE_USERNAME")
EHOUSE_PASSWORD = os.getenv("EHOUSE_PASSWORD")
EHOUSE_API_BASE_URL = os.getenv("EHOUSE_API_BASE_URL") or ""
EHOUSE_KEY_INVOICE_ITEM_ID = os.getenv("EHOUSE_KEY_INVOICE_ITEM_ID")
EHOUSE_CLIENT_INVOICE_ITEM_CODE = os.getenv("EHOUSE_CLIENT_INVOICE_ITEM_CODE")
try:
    EHOUSE_CLIENT_INVOICE_ITEM_CODE = (
        int(EHOUSE_CLIENT_INVOICE_ITEM_CODE)
        if EHOUSE_CLIENT_INVOICE_ITEM_CODE is not None
        else None
    )
except Exception:
    EHOUSE_CLIENT_INVOICE_ITEM_CODE = None

base_dir = os.path.dirname(os.path.abspath(__file__))
pem_file_path = os.path.join(base_dir, "custom_ca_bundle.pem")

# module logger (adapter injects request_id)
logger = get_logger(__name__)


def _get_request_id():
    try:
        from flask import g

        return getattr(g, "request_id", None)
    except Exception:
        return None


def _mask_email(email: str | None) -> str | None:
    if not email or "@" not in email:
        return None
    local, domain = email.split("@", 1)
    if not local:
        return f"***@{domain}"
    return f"{local[0]}***@{domain}"


def get_ehouse_token():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    request_id = _get_request_id()
    logger.info(
        "get_ehouse_token.start",
        extra={
            "request_id": request_id,
            "url": EHOUSE_API_BASE_URL + "token",
            "username_present": bool(EHOUSE_USERNAME),
        },
    )

    data = {
        "grant_type": "password",
        "username": EHOUSE_USERNAME,
        "password": EHOUSE_PASSWORD,
    }

    url = EHOUSE_API_BASE_URL + "token"
    try:
        response = requests.post(
            url=url, headers=headers, data=data, verify=pem_file_path
        )
        status = getattr(response, "status_code", None)
        logger.info(
            "get_ehouse_token.response",
            extra={"request_id": request_id, "status_code": status},
        )
        response.raise_for_status()
        token_response_dict = response.json()
        token = f"Bearer {token_response_dict['access_token']}"
        return token
    except Exception as e:
        logger.exception(
            "get_ehouse_token.exception", extra={"request_id": request_id, "url": url}
        )
        sentry_sdk.capture_exception(e)
        raise


def get_key_invoice_item_id(ehouse_access_token):
    request_id = _get_request_id()
    logger.info("get_key_invoice_item_id.start", extra={"request_id": request_id})

    headers = {"Accept": "application/json", "Authorization": ehouse_access_token}

    url = EHOUSE_API_BASE_URL + "v2/KeyInvoiceItems"

    try:
        response = requests.get(url=url, headers=headers, verify=pem_file_path)
        status = getattr(response, "status_code", None)
        logger.info(
            "get_key_invoice_item_id.response",
            extra={"request_id": request_id, "status_code": status},
        )
        response.raise_for_status()
        key_invoice_items = response.json()
        items = key_invoice_items.get("keyInvoiceItemsList", [])
        logger.debug(
            "get_key_invoice_item_id.items_count",
            extra={"request_id": request_id, "count": len(items)},
        )
        for item in items:
            if item.get("clientInvoiceItemCode") == EHOUSE_CLIENT_INVOICE_ITEM_CODE:
                logger.info(
                    "get_key_invoice_item_id.found",
                    extra={
                        "request_id": request_id,
                        "key_invoice_item_id": item.get("id"),
                    },
                )
                return item.get("id")
        logger.warning(
            "get_key_invoice_item_id.not_found",
            extra={
                "request_id": request_id,
                "clientInvoiceItemCode": EHOUSE_CLIENT_INVOICE_ITEM_CODE,
            },
        )
        raise Exception("keyInvoiceItem id not found")
    except Exception as e:
        logger.exception(
            "get_key_invoice_item_id.exception",
            extra={"request_id": request_id, "url": url},
        )
        sentry_sdk.capture_exception(e)
        raise


def send_book_ehouse_job_request(
    street_address,
    postcode,
    town,
    name,
    email_address,
    phone_number,
    key_invoice_item_id,
    ehouse_access_token,
):
    request_id = _get_request_id()
    masked_email = _mask_email(email_address)
    logger.info(
        "send_book_ehouse_job_request.start",
        extra={
            "request_id": request_id,
            "street_address": street_address,
            "postcode": postcode,
            "town": town,
            "vendorName_present": bool(name),
            "vendorEmail_masked": masked_email,
            "vendorPhone_present": bool(phone_number),
            "key_invoice_item_id": key_invoice_item_id,
        },
    )

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": ehouse_access_token,
    }

    data = {
        "keyInvoiceItems": [{"id": key_invoice_item_id, "quantity": 1}],
        "streetAddress": street_address,
        "town": town,
        "postcode": postcode,
        "sendVendorBookingSms": True,
        "sendVendorBookingEmail": True,
        "vendorName": name,
        "VendorMobile": phone_number,
        "vendorEmail": email_address,
    }

    url = EHOUSE_API_BASE_URL + "v2/Orders"

    try:
        response = requests.post(
            url=url, headers=headers, data=json.dumps(data), verify=pem_file_path
        )
        status = getattr(response, "status_code", None)
        logger.info(
            "send_book_ehouse_job_request.response",
            extra={"request_id": request_id, "status_code": status},
        )
        return response
    except Exception as e:
        logger.exception(
            "send_book_ehouse_job_request.exception",
            extra={"request_id": request_id, "url": url},
        )
        sentry_sdk.capture_exception(e)
        raise


def book_ehouse_job(street_address, postcode, town, name, email_address, phone_number):
    request_id = _get_request_id()
    logger.info(
        "book_ehouse_job.start",
        extra={
            "request_id": request_id,
            "street_address": street_address,
            "postcode": postcode,
            "town": town,
            "vendorName_present": bool(name),
            "vendorEmail_present": bool(email_address),
            "vendorPhone_present": bool(phone_number),
        },
    )

    ehouse_access_token = get_ehouse_token()

    try:
        key_invoice_item_id = get_key_invoice_item_id(ehouse_access_token)
    except Exception as e:
        logger.warning(
            "book_ehouse_job.key_invoice_item_id_fallback",
            extra={"request_id": request_id, "fallback_used": True},
        )
        sentry_sdk.capture_exception(e)
        key_invoice_item_id = EHOUSE_KEY_INVOICE_ITEM_ID

    response = send_book_ehouse_job_request(
        street_address,
        postcode,
        town,
        name,
        email_address,
        phone_number,
        key_invoice_item_id,
        ehouse_access_token,
    )

    try:
        status = getattr(response, "status_code", None)
        if status != 200:
            # log response body for debugging but keep it as string to avoid JSON issues
            body = None
            try:
                body = response.json()
            except Exception:
                body = getattr(response, "text", None)
            logger.error(
                "book_ehouse_job.failed",
                extra={
                    "request_id": request_id,
                    "status_code": status,
                    "response_body": str(body),
                },
            )
            raise Exception(body)
        logger.info(
            "book_ehouse_job.success",
            extra={"request_id": request_id, "status_code": status},
        )
    except Exception as e:
        logger.exception("book_ehouse_job.exception", extra={"request_id": request_id})
        sentry_sdk.capture_exception(e)
        raise


"""

street_address = ''
postcode = ''
town =  ''
name = ''
email_address = ''
phone_number = ''

book_ehouse_job(street_address, postcode, town, name, email_address, phone_number)
"""
