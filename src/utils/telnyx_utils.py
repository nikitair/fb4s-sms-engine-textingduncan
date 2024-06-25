from logs.logging_config import logger
import requests
from dataclasses import dataclass


@dataclass
class TelnyxService:
    api_key: str
    profile_id: str
    from_caller_id: str = "FB4S Team"
    url: str = "https://api.telnyx.com/v2/messages"


    def send_sms(self, to_phone_number: str, sms_body: str) -> bool | None:        
        logger.info(f"Telnyx: send SMS - (to: {to_phone_number}; body: {sms_body})")
        
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
                "webhook_url": "https://textingduncan.onrender.com/telnyx-webhook"
            }
        )
        
        status_code = response.status_code
        logger.info(f"Telnyx API: Status Code - ({status_code})")
        
        if status_code == 200:
            # logger.debug(f"Telnyx API Response - ({response.json()})")
            return True
        else:
            logger.error(f"!!! Telnyx API: Error - ({response.text})")
            return False
        
        