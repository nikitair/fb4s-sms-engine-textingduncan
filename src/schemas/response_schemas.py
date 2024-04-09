from typing import Union

from pydantic import BaseModel


class IndexResponseSchema(BaseModel):
    success: bool
    message: str


class NoteProcessingSchema(BaseModel):
    sms_text: Union[None, str]
    contact_name: Union[None, str]
    contact_phone: Union[None, str]
    sms_sent: bool
    assigned_team_member_id: Union[None, int]
    sms_signature: Union[None, str]


class FUBNoteCreatedResponseSchema(BaseModel):
    success: bool
    data: NoteProcessingSchema


class SimpleResponseSchema(BaseModel):
    success: bool
