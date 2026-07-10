from minsearch import Index


def build_index(chunks):
    """
    Build a MinSearch index from resume chunks.
    """

    documents = []

    for i, chunk in enumerate(chunks):
        documents.append(
            {
                "id": i,
                "content": chunk,
            }
        )

    index = Index(
        text_fields=["content"],
        keyword_fields=[]
    )

    index.fit(documents)

    return index