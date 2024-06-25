from logs.logging_config import logger
import requests
from dataclasses import dataclass
from utils import utils


@dataclass
class TelnyxService:
    api_key: str
    profile_id: str
    from_phone_number: str
    from_caller_id: str = "FB4S Team"
    url: str = "https://api.telnyx.com/v2/messages"


    def send_sms(self, to_phone_number: str, sms_body: str) -> bool | None:
        to_phone_number = utils.format_phone_number(to_phone_number)
        logger.info(f"Telnyx: send SMS - (to: {to_phone_number}; body: {sms_body}; Caller ID: {self.from_caller_id})")
        
        response = requests.post(
            url=self.url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "type": "SMS",
                "text": f"{sms_body}",
                "from": self.from_caller_id,
                "to": to_phone_number,
                "messaging_profile_id": self.profile_id,
                "webhook_url": "https://hook.us1.make.com/08g2zxt99khp9706o2plha4rihjtqrw6"
            }
        )
        
        status_code = response.status_code
        logger.info(f"Telnyx: Status Code - ({status_code})")
        
        if status_code == 200:
            return True
        else:
            logger.error(f"!!! Telnyx: Error - ({response.text})")
            logger.warning(f"Telnyx: Try with Phone Number - (from: {self.from_phone_number}; to: {to_phone_number}; body: {sms_body})")
            
            response_try = requests.post(
                url=self.url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                        "type": "SMS",
                        "text": f"{sms_body}",
                        "from": self.from_phone_number,
                        "to": to_phone_number,
                        "messaging_profile_id": self.profile_id,
                        "webhook_url": "https://hook.us1.make.com/08g2zxt99khp9706o2plha4rihjtqrw6"
                }
            )
            status_code = response_try.status_code
            logger.info(f"Telnyx 2 Try: Status Code - ({status_code})")
            
            if status_code == 200:
                return True
            else:
                logger.error(f"!!! Telnyx 2 Try: Error - ({response.text})")
                return False
