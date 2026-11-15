# The repository layer handles database operations.



from sqlalchemy.orm import Session

from app.models import ErrorLog


def create_error(db: Session, error_data: dict):

    new_error = ErrorLog(**error_data)

    try:
        db.add(new_error)
        db.commit()
        db.refresh(new_error)

        return new_error

    except Exception:
        db.rollback()
        raise


def update_error_solution(db: Session, error_id: int, solution: str):

    try:
        error_record = db.query(ErrorLog).filter(
            ErrorLog.id == error_id
        ).first()

        if error_record is None:
            raise ValueError("Error record not found.")

        error_record.solution = solution

        db.commit()
        db.refresh(error_record)

        return error_record

    except Exception:
        db.rollback()
        raise
