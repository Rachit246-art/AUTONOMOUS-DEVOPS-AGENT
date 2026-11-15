# If we write all database queries directly inside API endpoints, our code becomes difficult to maintain.
# Instead, we keep database operations in the repository layer.
# In our current project, its responsibility is to receive error data and pass it to the repository for database insertion.
# This is where we'll connect SQL Server and RAG.




from pathlib import Path
import sys

from sqlalchemy.orm import Session

from app.error_repository import create_error, update_error_solution


# Add project root to Python import path
PROJECT_ROOT = Path(__file__).resolve().parents[3]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.rag_engine.rag_pipeline import generate_rag_response


def save_error(db: Session, error_message: str):

    # Step 1: Save original error in SQL Server
    error_data = {
        "error_message": error_message
    }

    saved_error = create_error(
        db=db,
        error_data=error_data
    )

    # Step 2: Generate solution using complete RAG pipeline
    print("\n========== GENERATING RAG SOLUTION ==========")

    rag_result = generate_rag_response(error_message)

    solution = rag_result["solution"]

    # Step 3: Save generated solution against the same error ID
    updated_error = update_error_solution(
        db=db,
        error_id=saved_error.id,
        solution=solution
    )

    # Step 4: Return complete response
    return {
        "id": updated_error.id,
        "error_message": updated_error.error_message,
        "created_at": updated_error.created_at,
        "retrieved_chunks": rag_result["retrieved_chunks"],
        "sources": rag_result["sources"],
        "solution": updated_error.solution
    }
