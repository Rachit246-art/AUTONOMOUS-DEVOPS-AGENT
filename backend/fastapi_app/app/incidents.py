from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ErrorLogCreate, ErrorLogResponse
from app.error_service import save_error


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)


@router.post("/", response_model=ErrorLogResponse)
def create_incident(
    error: ErrorLogCreate,
    db: Session = Depends(get_db)
):

    saved_error = save_error(
        db=db,
        error_message=error.error_message
    )

    return saved_error
