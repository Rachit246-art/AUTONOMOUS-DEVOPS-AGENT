# The important part is that we don't need to provide each filename manually.
# Our loader automatically finds all PDF, TXT and Markdown documents.

# Function :	Responsibility
# load_document()	: Reads one document and extracts its text
# load_all_documents() :	Finds and loads all supported documents
# PROJECT_ROOT : Locates the main project directory
# DOCUMENTS_DIR	: Points to data/documents/

from pathlib import Path
import fitz


# Locate the project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Documents directory
DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"


def load_document(file_path):
    """Extract text from a single document."""

    file_path = Path(file_path)
    extension = file_path.suffix.lower()

    # Extract text from PDF
    if extension == ".pdf":

        text = ""

        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text() + "\n"

    # Read TXT and Markdown files
    elif extension in [".txt", ".md"]:

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

    else:
        raise ValueError(f"Unsupported file format: {extension}")

    return {
        "source": file_path.name,
        "file_type": extension,
        "text": text
    }


def load_all_documents():
    """Load all supported documents from the documents folder."""

    documents = []

    for file_path in DOCUMENTS_DIR.iterdir():

        if file_path.is_file() and file_path.suffix.lower() in [".pdf", ".txt", ".md"]:

            document = load_document(file_path)

            documents.append(document)

            print(f"Loaded: {file_path.name}")

    return documents


if __name__ == "__main__":

    loaded_documents = load_all_documents()

    print("\nTotal documents loaded:", len(loaded_documents))

    for document in loaded_documents:
        print("\nSource:", document["source"])
        print("Extracted characters:", len(document["text"]))
