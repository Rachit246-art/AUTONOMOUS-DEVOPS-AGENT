# It validates that error_message coming from postman.

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ErrorLogCreate(BaseModel):

    error_message: str


class ErrorLogResponse(BaseModel):

    id: int
    error_message: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
