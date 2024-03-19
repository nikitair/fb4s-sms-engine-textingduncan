import os
import json
import uvicorn
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI
from schemas import EventSchema, SendSMSSchema
from logs.logging_config import logger
from logs.logging_utils import log_server_start, log_server_stop
from services import sms_services
# from utils.utils import backup_request_response


load_dotenv()

SERVER_PORT = os.getenv("SERVER_PORT")
SERVER_HOST = os.getenv("SERVER_HOST")


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    log_server_start()


@app.on_event("shutdown")
async def shutdown_event():
    log_server_stop()


@app.get("/")
async def index_view():
    logger.info(f"{index_view.__name__} -- INDEX ENDPOINT TRIGGERED")
    return {"success": True, "message": "SMS Engine Index"}


@app.post("/sms/note-created")
async def note_created_webhook_view(request: EventSchema):
    result = {}
    payload = dict(request)

    logger.info(f"{note_created_webhook_view.__name__} -- NOTE to SMS WEBHOOK ENDPOINT TRIGGERED")
    logger.info(f"{note_created_webhook_view.__name__} -- RECEIVED PAYLOAD - {payload}")

    note_ids = payload["resourceIds"]
    if note_ids:
        result = sms_services.process_fub_note(note_ids[0])
        logger.info(f"{note_created_webhook_view.__name__} -- NOTE PROCESSING RESPONSE DATA - {result}")

    backup_data = {
        "request": payload,
        "response": result,
        "created_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M UTC")
    }

    # temporary backing up data to json
    logger.info(f"{note_created_webhook_view.__name__} -- BACKING UP DATA")
    try:
        with open("data/backups.json", "r") as f:
            backups = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        backups = []

    backups.append(backup_data)

    with open("data/backups.json", "w") as f:
        json.dump(backups, f, indent=4)
        logger.info(f"{note_created_webhook_view.__name__} -- BACKED UP DATA")

    return {
        "success": True if result.get("sms_sent") else False,
        "data": result
        }


@app.post("/sms/send")
def send_sms_view(request: SendSMSSchema):
    logger.info(f"{send_sms_view.__name__} -- SEND SMS WEBHOOK ENDPOINT TRIGGERED")

    result = {
        "success": False
    }

    payload = dict(request)

    logger.info(f"{send_sms_view.__name__} -- PAYLOAD RECEIVED - {payload}")
    to_number = payload.get("to_number")
    sms_body = payload.get("sms_body")

    is_sent = index_view.send_sms(to_number, sms_body)

    if is_sent:
        logger.info(f"{send_sms_view.__name__} -- SMS SUCCESSFULLY SENT TO - {to_number}")
        result["success"] = True
    else:
        logger.warning(f"{send_sms_view.__name__} -- ! FAILED SENDING SMS TO - {to_number}")

    return result


if __name__ == "__main__":
    uvicorn.run(app=app, port=int(SERVER_PORT), host=SERVER_HOST)
