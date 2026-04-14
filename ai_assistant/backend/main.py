import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from ai_assistant.backend.database import get_db, DocumentMetadata, CHROMA_PATH
from ai_assistant.backend.processor import extract_text_from_pdf
from ai_assistant.backend.ai_engine import AIEngine
from pydantic import BaseModel
from typing import List

from dotenv import load_dotenv

# Load environment variables at the top level
load_dotenv()

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_ai_engine = None

def get_ai_engine():
    global _ai_engine
    if _ai_engine is None:
        try:
            print("Initializing AI Engine...")
            _ai_engine = AIEngine(chroma_path=CHROMA_PATH)
            print("AI Engine initialized successfully.")
        except Exception as e:
            import traceback
            error_msg = traceback.format_exc()
            with open("backend_errors.log", "a") as f:
                f.write(f"--- Engine Init Error ---\n{error_msg}\n")
            print(f"ERROR: Failed to initialize AI Engine: {e}")
            raise e
    return _ai_engine

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    citations: List[dict]

@app.post("/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    doc_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{doc_id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        pages_content = extract_text_from_pdf(file_path, original_filename=file.filename)
        engine = get_ai_engine()
        engine.add_documents(pages_content)
        
        new_doc = DocumentMetadata(id=doc_id, filename=file.filename)
        db.add(new_doc)
        db.commit()
        
        return {"id": doc_id, "filename": file.filename, "status": "success"}
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else "N/A"
        with open("backend_errors.log", "a") as f:
            f.write(f"--- Upload error ---\nFile Size: {file_size}\n{error_msg}\n")
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def list_documents(db: Session = Depends(get_db)):
    docs = db.query(DocumentMetadata).all()
    return [{"id": d.id, "filename": d.filename, "date": d.upload_date} for d in docs]

@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str, db: Session = Depends(get_db)):
    doc = db.query(DocumentMetadata).filter(DocumentMetadata.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete from AI engine (Chroma)
    engine = get_ai_engine()
    engine.delete_document(doc.filename)
    
    # Delete from SQLite
    db.delete(doc)
    db.commit()
    
    return {"status": "deleted"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        engine = get_ai_engine()
        # Use the new async method to avoid blocking the event loop
        answer, source_docs = await engine.get_answer_async(request.query)
        citations = []
        for doc in source_docs:
            citations.append({
                "filename": doc.metadata.get("filename"),
                "page": doc.metadata.get("page")
            })
        return {"answer": answer, "citations": citations}
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        with open("backend_errors.log", "a") as f:
            f.write(f"--- Chat error ---\n{error_msg}\n")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT_BACKEND", 8600))
    uvicorn.run(app, host="0.0.0.0", port=port)
