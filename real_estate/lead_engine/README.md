# Real Estate Lead Engine

A lightweight FastAPI service for collecting local real estate leads and storing them in SQLite.

## Features
- Local HTML form at `/`
- Saves leads to SQLite via `/submit`
- Lists all captured leads at `/leads`
- Includes an email notification template function for future SMTP/CRM integrations

## Local setup (macOS/Linux)

```bash
cd real_estate/lead_engine
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Then open: `http://127.0.0.1:8000`

## Notes
- SQLite database file is stored at `real_estate/lead_engine/leads.db`.
- This starter app is intentionally simple and built for local development.
