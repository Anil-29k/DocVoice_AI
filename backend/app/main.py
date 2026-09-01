from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.documents import router as documents_router

app = FastAPI(title="DocVoice AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "DocVoice AI API is running"}
