import csv
import json
import os

import phonenumbers
import requests
from dotenv import load_dotenv

from logs.logging_config import logger

# from schemas.fub_webhook_schemas import EventSchema


load_dotenv()


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


def notify_team_by_email(emails: str, email_text: str, subject: str):
    response = requests.post(
        url=os.getenv("RETOOL_EMAIL_URL"),
        json={
            "email": emails,
            "template": email_text,
            "subject": subject
            }
    )
    if response.status_code == 200:
        return True


def convert_csv_to_json(csv_path: str, json_path: str):
    """
    loads data from csv file and stores it into JSON
    output -> list[dict]
    file output -> .json
    """
    data = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            row["sms_sent"] = None
            row["sms_delivered"] = None
            row["sms_body"] = None
            row["sent_at"] = None

            data.append(row)

    with open(json_path, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=2)

    logger.info(
        f"{convert_csv_to_json.__name__} -- CONVERTED CSV [{csv_path}] TO JSON [{json_path}]")
    return data


if __name__ == "__main__":
    convert_csv_to_json("data/blast/test_contacts.csv", "data/blast/test_contacts.json")
