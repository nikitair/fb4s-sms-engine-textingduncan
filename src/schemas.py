from pydantic import BaseModel
from typing import List, Union


class EventSchema(BaseModel):
    eventId: str
    eventCreated: str
    event: str
    resourceIds: list[int]
    uri: str


class SendSMSSchema(BaseModel):
    to_number: str
    sms_body: str


class MailWizzSMSSchema(BaseModel):
    subscription_list_uid: List[str]
    campaign_uid: str
    subscriber_email: str
    campaign_special_id: Union[int, str]
    phone_number: str
