import requests
from logs.logging_config import logger


class Retool:
    
    def __init__(self) -> None:
        logger.info("Retool -- CLASS INITIALIZED")


    def get_sms_template(self, campaign_special_id: int, campaign_day: int):
        logger.info(f"{self.get_sms_template.__name__} -- GETTING SMS TEMPLATE WITH campaign_special_id - {campaign_special_id}; campaign_day - {campaign_day}")
        response = requests.post(
            url="https://api.retool.com/v1/workflows/6037d941-19f8-49d2-a152-29af3b9ea8fc/startTrigger?workflowApiKey=retool_wk_019e31ef121b4c03af2302633668c492",
            json={"campaign_special_id": campaign_special_id, "campaign_day": campaign_day}
        )
        status_code = response.status_code
        data = response.json()
        logger.info(f"{self.get_sms_template.__name__} -- STATUS CODE - {status_code}; DATA - {data}")

        if status_code != 200:
            logger.warning(f"{self.get_sms_template.__name__} -- ! SMS TEMPLATE NOT FOUND")
        
        return data
