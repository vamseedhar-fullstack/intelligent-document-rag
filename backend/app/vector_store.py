from pathlib import Path
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


DB_PATH = str(Path(__file__).resolve().parent.parent / "chroma_db")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

vector_store = Chroma(
    collection_name="documents_v2",
    embedding_function=embeddings,
    persist_directory=DB_PATH,
)


def store_chunks(chunks: list[str], document_id: str, filename: str):
    documents = [
        Document(
            page_content=chunk,
            metadata={
                "document_id": document_id,
                "filename": filename,
                "chunk_index": index,
            },
        )
        for index, chunk in enumerate(chunks)
    ]

    ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]

    if documents:
        vector_store.add_documents(documents=documents, ids=ids)


def search_chunks(question: str, top_k: int = 3):
    if not question.strip():
        return []

    results = vector_store.similarity_search(question, k=top_k)

    return [
        {
            "text": doc.page_content,
            "metadata": doc.metadata,
        }
        for doc in results
    ]
