from pydantic import BaseModel


class EventSchema(BaseModel):
    eventId: str
    eventCreated: str
    event: str
    resourceIds: list[int]
    uri: str


class SendSMSSchema(BaseModel):
    to_number: str
    sms_body: str
