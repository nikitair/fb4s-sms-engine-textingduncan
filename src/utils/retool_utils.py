import os

import requests
from dotenv import load_dotenv

from logging_config import logger

load_dotenv()


class Retool:

    def __init__(self) -> None:
        logger.info("Retool -- CLASS INITIALIZED")

    def get_sms_template(self, campaign_special_id: int, campaign_day: int):
        logger.info(f"{self.get_sms_template.__name__} -- GETTING SMS TEMPLATE WITH campaign_special_id - {campaign_special_id}; campaign_day - {campaign_day}")
        response = requests.post(
            url=os.getenv("RETOOL_GET_SMS_TEMPLATE_URL"),
            json={"campaign_special_id": campaign_special_id, "campaign_day": campaign_day}
        )
        status_code = response.status_code
        data = response.json()
        logger.info(f"{self.get_sms_template.__name__} -- STATUS CODE - {status_code}; DATA - {data}")

        if status_code != 200:
            logger.warning(f"{self.get_sms_template.__name__} -- ! SMS TEMPLATE NOT FOUND")
        return data
    
    
    def send_telnyx_stats(self, insert_payload: dict) -> bool:
        logger.info(f"Retool: save Telnyx stats to DB - ({insert_payload})")
        
        response = requests.post(
            url=os.getenv("RETOOL_SAVE_TELNYX_STATS_URL"),
            headers={
                "X-Workflow-Api-Key": os.getenv("RETOOL_SAVE_TELNYX_STATS_API_KEY")
            },
            json=insert_payload
        )
        status_code = response.status_code
        logger.info(f"Retool: status code - ({status_code})")
        return True if status_code == 200 else False
