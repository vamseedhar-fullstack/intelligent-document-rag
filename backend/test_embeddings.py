
from app.embeddings import embed_texts


def test_embeddings_are_generated():
    texts = [
        "The requested claim amount is 10000 rupees.",
        "The employee joined the company in 2020.",
    ]

    embeddings = embed_texts(texts)

    assert len(embeddings) == 2
    assert len(embeddings[0]) > 0
    assert len(embeddings[0]) == len(embeddings[1])
    assert all(isinstance(value, float) for value in embeddings[0])
