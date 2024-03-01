import os
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from schemas.fub_webhooks_schemas import EventSchema

load_dotenv()

SERVER_PORT = os.getenv("SERVER_PORT")
SERVER_HOST = os.getenv("SERVER_HOST")


app = FastAPI()


@app.get("/")
def index():
    return {"success": True, "message": "Hello World"}


@app.post("/sms")
def sms(request: EventSchema):

    print(request.json())

    return {"success": True, "message": "Hello World", "data": request}


if __name__ == "__main__":
    uvicorn.run(app=app, port=int(SERVER_PORT), host=SERVER_HOST)
