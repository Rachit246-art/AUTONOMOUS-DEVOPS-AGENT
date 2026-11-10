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
