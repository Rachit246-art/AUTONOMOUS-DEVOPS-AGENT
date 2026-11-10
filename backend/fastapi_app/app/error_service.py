# If we write all database queries directly inside API endpoints, our code becomes difficult to maintain.
# Instead, we keep database operations in the repository layer.
# In our current project, its responsibility is to receive error data and pass it to the repository for database insertion.


from sqlalchemy.orm import Session

from app.error_repository import create_error


def save_error(db: Session, error_message: str):

    error_data = {
        "error_message": error_message
    }

    saved_error = create_error(
        db=db,
        error_data=error_data
    )

    return saved_error
