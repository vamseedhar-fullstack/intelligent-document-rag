from pathlib import Path
import pymupdf
from fastapi import HTTPException, UploadFile
from app.chunking import chunk_text
from app.embeddings import embed_texts
from uuid import uuid4
from app.embeddings import embed_texts
from app.vector_store import store_chunks


MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


async def extract_pdf(file: UploadFile) -> dict:
    """Validate an uploaded PDF, extract its text, and split it into chunks."""

    # 1. Validate the filename and extension.
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    # 2. Read the file and enforce the size limit.
    content = await file.read(MAX_FILE_SIZE + 1)

    if not content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="The file exceeds the 10 MB limit.",
        )

    # 3. Open the PDF and extract text.
    try:
        with pymupdf.open(stream=content, filetype="pdf") as pdf:
            if pdf.needs_pass:
                raise HTTPException(
                    status_code=400,
                    detail="Password-protected PDFs are not supported.",
                )

            page_count = len(pdf)
            extracted_text = "\n".join(
                page.get_text() for page in pdf
            ).strip()

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="Could not read this PDF. Please upload a valid PDF.",
        ) from exc

    # 4. Handle PDFs that contain no extractable text.
    if not extracted_text:
        raise HTTPException(
            status_code=422,
            detail=(
                "No text could be extracted from this PDF. "
                "It may be scanned and require OCR."
            ),
        )

    # 5. Split extracted text into chunks.
    chunks = chunk_text(extracted_text)

    # 6. Convert chunks into numerical vectors.
    embeddings = embed_texts(chunks)

    document_id = str(uuid4())

    store_chunks(
    chunks=chunks,
    document_id=document_id,
    filename=Path(file.filename).name,
    )
    
    # 6. Return document metadata and its chunks.
    return {
        "document_id": document_id,
        "filename": Path(file.filename).name,
        "page_count": page_count,
        "character_count": len(extracted_text),
        "chunk_count": len(chunks),
        "chunks": [
            {
                "chunk_id": index,
                "text": chunk,
            }
            for index, chunk in enumerate(chunks)
        ],
        "embeddings": embeddings
    }
