from utils.fub_utils import FUB
from logs.logging_config import logger


def send_note_to_buyer_by_sms_view(note_id: int) -> bool:
    logger.info(f"{send_note_to_buyer_by_sms_view.__name__} -- SENDING NOTE AS SMS")

    fub = FUB()

    # get note data
    note_data = fub.get_note(note_id)

    if note_data["success"] == True:

        # get buyer_id and note message for sms
        buyer_id = note_data["data"]["personId"]
        note_message = note_data["data"]["body"]

        # get buyer data
        buyer_data = fub.get_buyer(buyer_id)

        if buyer_data["success"] == True:

            buyer_name = buyer_data["data"]["name"]
            buyer_phones = buyer_data["data"]["phones"]

            # get buyer phone number
            buyer_phone = buyer_phones[0]["value"] if buyer_phones and type(buyer_phones) == list else None

            logger.info(f"{send_note_to_buyer_by_sms_view.__name__} -- BUYER NAME - {buyer_name}; BUYER PHONE - {buyer_phone}")

            if buyer_phone:

                # send sms
                ...
