
def chunk_text(text, chunk_size=500, overlap=100):
    """
    Divide extracted text into smaller chunks
    with overlapping content.
    """

    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("Overlap must be non-negative and smaller than chunk size.")

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = min(start + chunk_size, text_length)

        # Avoid cutting a word in half when possible
        if end < text_length:
            space_position = text.rfind(" ", start, end)

            if space_position > start:
                end = space_position

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = end - overlap

    return chunks
