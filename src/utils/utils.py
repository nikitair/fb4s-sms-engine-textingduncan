import phonenumbers
from logs.logging_config import logger
import requests
# from schemas.fub_webhook_schemas import EventSchema


def format_phone_number(phone_number: str):
    """
    converts phone numbers to a desired format
    (012) 345-6789 -> +10123456789, etc.
    """
    phone_number_formatted = ""
    try:
        phone_number_formatted = phonenumbers.format_number(
            phonenumbers.parse(phone_number, 'US'),
            phonenumbers.PhoneNumberFormat.E164)
        logger.info(f"{format_phone_number.__name__} -- FORMATTED PHONE NUMBER -- FROM - {phone_number} - TO - {phone_number_formatted}")
    except Exception as ex:
        logger.warning(f"{format_phone_number.__name__} -- ! FAILED FORMATTING - {phone_number} - {ex}")
    return phone_number_formatted


def backup_request_response(func):
    """
    decorator to backup api requests and responses
    """
    ...


def notify_team_by_email(email_text: str):
    response = requests.post(
        url="https://api.retool.com/v1/workflows/bb40dd15-f40f-4565-a671-ecbb0d06a575/startTrigger?workflowApiKey=retool_wk_26708f61a11642369c829a57dd42bbc5",
        json={
            "email": "nikita@actse.ltd",
            "template": email_text,
            "subject": "Texting Duncan Event"
            }
    )
    if response.status_code == 200:
        return True
