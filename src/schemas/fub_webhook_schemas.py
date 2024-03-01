from pydantic import BaseModel
from typing import Any


class EventSchema(BaseModel):
    eventId: str
    eventCreated: str
    event: str
    resourceIds: list[Any]
    uri: str
