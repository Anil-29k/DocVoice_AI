# DocVoice AI - Backend

## Setup

Python 3.10+ is recommended.

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Optional: copy `.env.example` to `.env` and set `MONGODB_URI`.

Start the API:

```bash
uvicorn app.main:app --reload
```

API docs:
`http://127.0.0.1:8000/docs`

### Important
`pyttsx3` uses the operating system's installed speech engine. On some Linux systems, `espeak-ng` may need to be installed separately.

This MVP supports PDFs with selectable text. OCR for scanned PDFs can be added as a later feature.
