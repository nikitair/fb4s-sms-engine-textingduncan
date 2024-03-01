from utils.fub_utils import FUB


def forward_note_to_buyer_by_sms(note_id: int) -> bool:

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

            if buyer_phone:

                # send sms
                ...
