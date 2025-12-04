from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import uuid
import traceback

from embeddings import get_embedding
from utils import text_splitter
from models import Chunk
import vector_store

router = APIRouter(prefix="/api/files", tags=["files"])

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a markdown/text file for RAG processing."""
    try:
        file_bytes = await file.read()
        file_text = file_bytes.decode('utf-8')
        
        document_id = str(uuid.uuid4())
        
        chunks: list[Chunk] = text_splitter.split_text(file_text, document_id, file.filename)
        for chunk in chunks:
            chunk.embedding = get_embedding(chunk.text)
        
        await vector_store.upsert_chunks(chunks)
        
        return JSONResponse({
            "document_id": document_id,
            "num_chunks": len(chunks)
        })
    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse(status_code=400, content={"error": str(e)})