# It validates that error_message coming from postman.


from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class ErrorLogCreate(BaseModel):
    error_message: str


class ErrorLogResponse(BaseModel):
    id: int
    error_message: str
    created_at: datetime
    retrieved_chunks: int
    sources: List[str]
    solution: str

    model_config = ConfigDict(from_attributes=True)
