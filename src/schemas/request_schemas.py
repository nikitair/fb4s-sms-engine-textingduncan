from typing import List, Optional, Union

from pydantic import BaseModel


class FUBNoteCreatedSchema(BaseModel):
    eventId: str
    eventCreated: str
    event: str
    resourceIds: list[int]
    uri: str


class SendSMSSchema(BaseModel):
    to_number: str
    sms_body: str


class MailWizzSMSSchema(BaseModel):
    # subscription_list_uid: Optional[List[str]]
    # campaign_uid: Optional[str]
    # subscriber_email: Optional[str]
    campaign_special_id: Union[int, str]
    phone_number: str
    campaign_day: int
    # jerk_realtor_name: Optional[str]
    # tm_name: Optional[str]
    # mls: Optional[str]
