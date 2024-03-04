from twilio.rest import Client
from logger import logger as logging
from utils import format_phone_number


class Twilio:
    TWILIO_SID = 'AC2eae5ba834000cabf93c85b12c51fe32'
    TWILIO_AUTH_TOKEN = '2a6716c10b49845defbd7f5761272cc1'

    def __init__(self):
        self.client = Client(self.TWILIO_SID, self.TWILIO_AUTH_TOKEN)

    def send_sms(self, phone_number, message):
        phone_number = format_phone_number(phone_number)

        logging.info(f"{self.send_sms.__name__} -- TWILIO - SENDING SMS TO - {phone_number}")

        result = {
            "success": None,
            "sms_sid": None
        }

        try:
            sms = self.client.messages.create(
                body=message,
                from_='+15166146500',
                to=phone_number
            )
            logging.info(f"{self.send_sms.__name__} -- TWILIO - STATUS - {sms.status}")

            result["success"] = True if sms.status in ("delivered", "queued", "sending", "sent", "receiving", "received", "accepted") else False
            result["sms_id"] = sms.sid

        except Exception:
            logging.error(f"{self.send_sms.__name__} -- !!! TWILIO ERROR")
        
        return result

    def sms_status(self, sid):
        logging.info(f"{self.sms_status.__name__} -- TWILIO - CHECKING DELIVERY STATUS OF - {sid}")
        status = None

        try:
            status = self.client.messages(sid).fetch().status
            # status = self.client.messages(sid).fetch().error_code
            logging.info(f"{self.sms_status.__name__} -- TWILIO - DELIVERY STATUS - {status}")
        except Exception:
            logging.error(f"{self.sms_status.__name__} -- !!! TWILIO ERROR")

        return True if status == "delivered" else False
    

    def __str__(self):
        return "Twillio"

if __name__ == "__main__":
    twilio = Twilio()
    # message = twilio.send_sms('(844) 900-0770', 'test message')
    # print(message)
    # time.sleep(1)
    status = twilio.sms_status("SMf157a5106119ecfd9dbf27af9e6b7228")
    print(status)
