from logging_config import logger
import requests
from dataclasses import dataclass
from utils import utils
from utils.retool_utils import Retool


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
            response_data = response.json()
            logger.debug(f"Telnyx: response data - ({response_data})")
        
            try:
                # collect statistics
                stats_collected = self.collect_stats(response_data)
                logger.info(f"Telnyx: Stats collected - ({stats_collected})")
            except Exception as ex:
                logger.exception(f"Telnyx: !!! Failed collecting stats - ({ex})")
            
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
                response_data = response_try.json()
                logger.debug(f"Telnyx: response data - ({response_data})")

                try:
                    # collect statistics
                    stats_collected = self.collect_stats(response_data)
                    logger.info(f"Telnyx: Stats collected - ({stats_collected})")
                except Exception as ex:
                    logger.exception(f"Telnyx: !!! Failed collecting stats - ({ex})")
                
                return True
            else:
                logger.error(f"!!! Telnyx 2 Try: Error - ({response_try.text})")
                
                db_insert_payload = {
                    "sender": self.from_phone_number,
                    "receiver": to_phone_number,
                    "sms_body": sms_body,
                    "direction": "outbound",
                    "messaging_type": "message",
                    "delivery_status": "failed",
                    "message_id": None,
                    "messaging_profile_id": self.profile_id,
                    "cost_amount": 0,
                    "currency": None
                }
                try:
                    # collect statistics
                    retool = Retool()
                    save_stats_result = retool.send_telnyx_stats(db_insert_payload)
                    logger.info(f"Retool: DB saving result - ({save_stats_result})")
                except Exception as ex:
                    logger.exception(f"Telnyx: !!! Failed collecting stats - ({ex})")
                
                return False
            
            
    def collect_stats(self, telnyx_response_payload: dict) -> bool:
        logger.info(f"Telnyx: collect stats for payload - ({telnyx_response_payload})")
        db_insert_payload = {
                "sender": telnyx_response_payload["data"]["from"]["phone_number"],
                "receiver": telnyx_response_payload["data"]["to"][0]["phone_number"],
                "sms_body": telnyx_response_payload["data"]["text"],
                "direction": telnyx_response_payload["data"]["direction"],
                "messaging_type": telnyx_response_payload["data"]["record_type"],
                "delivery_status": telnyx_response_payload["data"]["to"][0]["status"],
                "message_id": telnyx_response_payload["data"]["id"],
                "messaging_profile_id": telnyx_response_payload["data"]["messaging_profile_id"],
                "cost_amount": telnyx_response_payload["data"]["cost"]["amount"],
                "currency": telnyx_response_payload["data"]["cost"]["currency"]
        }
        logger.info(f"Telnyx: DB statistics Insert payload - ({db_insert_payload})")
        
        retool = Retool()
        save_stats_result = retool.send_telnyx_stats(db_insert_payload)
        logger.info(f"Retool: DB saving result - ({save_stats_result})")
        return save_stats_result

        
        
        
