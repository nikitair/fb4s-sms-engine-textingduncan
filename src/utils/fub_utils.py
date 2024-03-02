import os
import traceback
import requests
from dotenv import load_dotenv
from logs.logging_config import logger

load_dotenv()

FUB_API_KEY = os.getenv("FUB_API_KEY")
BASE_URL = "https://api.followupboss.com/v1"


class FUB:

    def __init__(self):
        logger.info(f"FUB OBJECT INITIALIZED")


    def get_note(self, note_id: int) -> dict:
        logger.info(f"{self.get_note.__name__} -- GETTING NOTE WITH ID - {note_id}")
        result = {"success": False, "data": {}}

        response = requests.get(
            url=f"{BASE_URL}/notes/{note_id}",
            headers = {
                "accept": "application/json",
                "authorization": f"Basic {FUB_API_KEY}"
            }
        )

        status_code = response.status_code
        logger.info(f"{self.get_note.__name__} -- FUB API STATUS CODE - {status_code}")

        try:
            result["data"] = response.json()
            logger.info(f"{self.get_note.__name__} -- FUB API RESPONSE - {result['data']}")
        except Exception:
            logger.exception(f"{self.get_note.__name__} -- !!! FUB API ERROR")
        if status_code == 200: 
            result["success"] = True

        return result
    

    def get_buyer(self, buyer_id: int) -> dict:
        logger.info(f"{self.get_buyer.__name__} -- GETTING BUYER WITH ID - {buyer_id}")
        result = {"success": False, "data": {}}

        response = requests.get(
            url=f"{BASE_URL}/people/{buyer_id}",
            headers = {
                "accept": "application/json",
                "authorization": f"Basic {FUB_API_KEY}"
            }
        )

        status_code = response.status_code
        logger.info(f"{self.get_buyer.__name__} -- FUB API STATUS CODE - {status_code}")

        try:
            result["data"] = response.json()
            logger.info(f"{self.get_buyer.__name__} -- FUB API RESPONSE - {response['data']}")
        except Exception:
            logger.exception(f"{self.get_buyer.__name__} -- !!! FUB API ERROR")

        if status_code == 200: 
            result["success"] = True

        return result



if __name__ == "__main__":
    ...
