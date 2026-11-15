# We are creating a Python representation of the table we already created manually in SSMS.
# We are mapping our existing SSMS table to Python.


from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func

from app.database import Base


class ErrorLog(Base):

    __tablename__ = "ErrorLogs"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    error_message = Column(
        String,
        nullable=False
    )

    solution = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
