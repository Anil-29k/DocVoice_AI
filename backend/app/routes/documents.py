from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.services.pdf_service import extract_pdf_text
from app.services.nlp_service import summarize_text, extract_keywords
from app.services.tts_service import text_to_speech
from app.database.mongodb import save_document

router = APIRouter(tags=["documents"])

BASE_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BASE_DIR / "uploads"
AUDIO_DIR = BASE_DIR / "audio"
UPLOAD_DIR.mkdir(exist_ok=True)
AUDIO_DIR.mkdir(exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024


@router.post("/documents/process")
async def process_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size must be 10 MB or less.")

    document_id = str(uuid4())
    safe_name = Path(file.filename).name
    pdf_path = UPLOAD_DIR / f"{document_id}_{safe_name}"
    pdf_path.write_bytes(content)

    try:
        text = extract_pdf_text(pdf_path)
        if not text.strip():
            raise HTTPException(
                status_code=422,
                detail="No selectable text was found. Scanned/OCR PDFs are not supported in this MVP."
            )

        summary = summarize_text(text)
        keywords = extract_keywords(text)

        audio_text = summary if summary else text[:5000]
        audio_path = AUDIO_DIR / f"{document_id}.wav"
        text_to_speech(audio_text, audio_path)

        result = {
            "id": document_id,
            "filename": safe_name,
            "text_preview": text[:3000],
            "word_count": len(text.split()),
            "summary": summary,
            "keywords": keywords,
            "audio_url": f"/api/documents/{document_id}/audio",
        }

        save_document(result)
        return result

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Processing failed: {exc}")


@router.get("/documents/{document_id}/audio")
def get_audio(document_id: str):
    audio_path = AUDIO_DIR / f"{document_id}.wav"
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Audio not found.")
    return FileResponse(audio_path, media_type="audio/wav", filename=f"{document_id}.wav")
