import os
from dotenv import load_dotenv
import json
import time
from datetime import datetime

from logging_config import logger
from utils.fub_utils import FUB
from utils.retool_utils import Retool
# from utils.twilio_utils import Twilio
from utils.telnyx_utils import TelnyxService

load_dotenv()

TELNYX_API_KEY = os.getenv("TELNYX_API_KEY", "")
TELNYX_PUBLIC_KEY = os.getenv("TELNYX_PUBLIC_KEY", "")
TELNYX_PROFILE_ID = os.getenv("TELNYX_PROFILE_ID", "")
TELNYX_PHONE_NUMBER = os.getenv("TELNYX_PHONE_NUMBER", "")


def get_signature(team_member_id: int):

    team_member_signature = "\n\nFB4S Team"

    try:
        with open("database/signatures.json", "r") as f:
            all_signatures = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_signatures = []

    for signature in all_signatures:
        if signature.get("fub_id") == team_member_id:
            team_member_signature = signature.get("signature")
            break

    return team_member_signature


def process_fub_note(note_id: int) -> dict:
    result = {
        "sms_text": None,
        "contact_name": None,
        "contact_phone": None,
        "sms_sent": False,
        "assigned_team_member_id": None,
        "sms_signature": None
    }

    fub = FUB()

    # get note data
    note_data = fub.get_note(note_id)

    if note_data["success"] is True:

        # get buyer_id and note message for sms
        buyer_id = note_data["data"]["personId"]
        note_message: str = note_data["data"]["body"]

        # get buyer data
        buyer_data = fub.get_buyer(buyer_id)

        if buyer_data["success"] is True and "[scheduled]" in note_message:
            logger.info(f"*** SENDING NOTE AS SMS")

            buyer_name = buyer_data["data"]["name"]
            assigned_team_member_id = buyer_data["data"]["assignedUserId"]
            result["assigned_team_member_id"] = assigned_team_member_id

            team_member_signature = get_signature(assigned_team_member_id)
            result["sms_signature"] = team_member_signature

            note_message += team_member_signature

            result["contact_name"] = buyer_name

            buyer_phones = buyer_data["data"]["phones"]

            # get buyer phone number
            buyer_phone = buyer_phones[0]["value"] if buyer_phones and isinstance(buyer_phones, list) else None

            logger.info(f"{process_fub_note.__name__} -- BUYER NAME - {buyer_name}; BUYER PHONE - {buyer_phone}")

            if buyer_phone:
                telnyx = TelnyxService(
                    api_key=TELNYX_API_KEY, 
                    profile_id=TELNYX_PROFILE_ID,
                    from_phone_number=TELNYX_PHONE_NUMBER
                )
                result["contact_phone"] = buyer_phone

                note_message = note_message.replace("[scheduled] ", "")

                # send sms
                # logger.info(f"{process_fub_note.__name__} -- SENDING NOTE AS SMS - {note_message}")
                sending_result = telnyx.send_sms(buyer_phone, note_message)
                result["sms_sent"] = sending_result

                # updating note
                fub.update_note(note_id=note_id, note_text=note_message)

        result["sms_text"] = note_message

    return result


def blast_send_sms(contacts_file_path: str, sms_body: str):
    logger.info(f"{blast_send_sms.__name__} -- STARTING SMS BLAST")

    telnyx = TelnyxService(
        api_key=TELNYX_API_KEY, 
        profile_id=TELNYX_PROFILE_ID,
        from_phone_number=TELNYX_PHONE_NUMBER
    )
    contacts = []

    with open(contacts_file_path, "r") as f:
        contacts = json.load(f)

    logger.info(f"{blast_send_sms.__name__} -- {len(contacts)} CONTACT RECEIVED")

    if contacts:
        for i, contact in enumerate(contacts, start=1):
            logger.info(f"{blast_send_sms.__name__} -- # {i} - [{round(i/len(contacts)*100, 2)}%]")
            logger.info(f"{blast_send_sms.__name__} -- CONTACT DATA - {contact}")

            phone_number = contact.get("Phone")

            sending_result = telnyx.send_sms(phone_number, sms_body)

            if sending_result:

                contact["sms_sent"] = True
                contact["sms_body"] = sms_body
                contact["sent_at"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M UTC")

            with open(contacts_file_path, "w") as f:
                json.dump(contacts, f, indent=4)

            time.sleep(5)

    logger.info(f"{blast_send_sms.__name__} -- SMS BLAST COMPLETED")


def send_sms(to_number: str, sms_body: str):
    telnyx = TelnyxService(
        api_key=TELNYX_API_KEY, 
        profile_id=TELNYX_PROFILE_ID,
        from_phone_number=TELNYX_PHONE_NUMBER
    )
    sms_sending_result = telnyx.send_sms(to_number, sms_body)
    return True if sms_sending_result else False


def process_mailwizz_data(campaign_special_id: int, to_phone_number: str, campaign_day: int, jerk_realtor_name: str = None, tm_name: str = None, mls: str = None):
    logger.info(f"{process_mailwizz_data.__name__} -- PROCESSING MAILWIZZ WEBHOOK DATA")

    # getting sms template if exists
    retool = Retool()
    retool_response = retool.get_sms_template(campaign_special_id, campaign_day)

    if retool_response["success"] is True:

        # sending sms
        template: str = retool_response["sms_template"]

        # Jerk Realtors Logic:
        if campaign_special_id == 9:
            logger.info(f"{process_mailwizz_data.__name__} -- JERK REALTORS LOGIC")

            logger.info(f"{process_mailwizz_data.__name__} -- TM NAME - {tm_name}")
            logger.info(f"{process_mailwizz_data.__name__} -- MLS - {mls}")
            logger.info(f"{process_mailwizz_data.__name__} -- JR NAME - {jerk_realtor_name}")

            match campaign_day:
                case 1:
                    template = template.replace('zzzzz', tm_name)
                    template = template.replace('xxxxx', mls)

                case 2:
                    template = template.replace('yyyyy', jerk_realtor_name)

                case _:
                    pass
        
        logger.info(f"{process_mailwizz_data.__name__} -- SMS TEMPLATE TO SEND - {template}; TO - {to_phone_number}")
        return send_sms(to_phone_number, template)


def get_telnyx_stats():
    logger.info("Get Telnyx stats")
    telnyx = TelnyxService(
        api_key=TELNYX_API_KEY, 
        profile_id=TELNYX_PROFILE_ID,
        from_phone_number=TELNYX_PHONE_NUMBER
    )
    return telnyx.get_messaging_stats()