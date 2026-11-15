
from sentence_transformers import SentenceTransformer

# Load the embedding model
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def generate_embeddings(text_chunks):
    """
    Convert a list of text chunks into numerical vectors.
    """

    if not text_chunks:
        return []

    embeddings = model.encode(
        text_chunks,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    return embeddings
