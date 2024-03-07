from utils.fub_utils import FUB
from utils.twilio_utils import Twilio
from logs.logging_config import logger


def send_note_to_buyer_by_sms_view(note_id: int) -> dict:
    logger.info(f"{send_note_to_buyer_by_sms_view.__name__} -- SENDING NOTE AS SMS")

    result = {
        "sms_text": None,
        "contact_name": None,
        "contact_phone": None,
        "sms_sent": False
    }

    fub = FUB()
    

    # get note data
    note_data = fub.get_note(note_id)

    if note_data["success"] is True:

        # get buyer_id and note message for sms
        buyer_id = note_data["data"]["personId"]
        note_message: str = note_data["data"]["body"]

        result["sms_text"] = note_message

        # get buyer data
        buyer_data = fub.get_buyer(buyer_id)

        if buyer_data["success"] is True and "[scheduled]" in note_message:

            buyer_name = buyer_data["data"]["name"]
            result["contact_name"] = buyer_name

            buyer_phones = buyer_data["data"]["phones"]

            # get buyer phone number
            buyer_phone = buyer_phones[0]["value"] if buyer_phones and isinstance(buyer_phones, list) else None

            logger.info(f"{send_note_to_buyer_by_sms_view.__name__} -- BUYER NAME - {buyer_name}; BUYER PHONE - {buyer_phone}")

            if buyer_phone:
                twilio = Twilio()
                result["contact_phone"] = buyer_phone

                note_message = note_message.replace("[scheduled] ", "")

                # send sms
                sending_result = twilio.send_sms(buyer_phone, note_message)
                result["sms_sent"] = sending_result["success"]

    return result
