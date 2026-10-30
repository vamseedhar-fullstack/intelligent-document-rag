from fastapi import FastAPI, File, UploadFile
from app.documents import extract_pdf

app = FastAPI(
    title="AI Document Intelligence",
    description="An AI-powered document analysis API",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    return await extract_pdf(file)
