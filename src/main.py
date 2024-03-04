import os
import json
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from schemas.fub_webhook_schemas import EventSchema
from logs.logging_config import logger
from logs.logging_utils import log_server_start, log_server_stop
from views.sms_views import send_note_to_buyer_by_sms_view


load_dotenv()

SERVER_PORT = os.getenv("SERVER_PORT")
SERVER_HOST = os.getenv("SERVER_HOST")


app = FastAPI()


# TODO: find the better solution
@app.on_event("startup")
async def startup_event():
    log_server_start()


@app.on_event("shutdown")
async def shutdown_event():
    log_server_stop()


@app.get("/")
async def index():
    logger.info(f"{index.__name__} -- INDEX ENDPOINT TRIGGERED")
    return {"success": True, "message": "Hello World"}


@app.post("/sms")
async def sms(request: EventSchema):

    backup_payload = {
        "payload": None,
        "response": None
    }

    payload = dict(request)
    with open("data/payloads.json", "r") as f:
        json_data: list = json.load(f)

    json_data.append(payload)

    logger.info(f"{sms.__name__} -- SMS ENDPOINT TRIGGERED")
    logger.info(f"{sms.__name__} -- RECEIVED PAYLOAD - {payload}")



    note_ids = request.resourceIds
    if note_ids:
        result = send_note_to_buyer_by_sms_view(note_ids[0])

    logger.info(f"{sms.__name__} -- SMS RESPONSE DATA - result")

    backup_payload["payload"] = payload
    backup_payload["response"] = result

    with open("data/payloads.json", "w") as f:
        json.dump(backup_payload, f, indent=4)

    return {"success": True, "data": result}


if __name__ == "__main__":
    uvicorn.run(app=app, port=int(SERVER_PORT), host=SERVER_HOST)
