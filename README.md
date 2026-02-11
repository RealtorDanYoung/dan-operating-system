# Dan Young Arizona Real Estate Lead & Follow-up System

Lightweight local FastAPI application for capturing and managing real-estate leads.

## Project Structure

```text
real_estate/
  lead_engine/
    main.py
    requirements.txt
    leads.db (created at runtime)
  templates/
    new_lead_reply.txt
    appointment_confirmation.txt
    follow_up_3_day.txt
    follow_up_14_day.txt
docs/
  DAILY_WORKFLOW.md
  ROADMAP.md
```

## Exact macOS Run Steps

1. Open Terminal and move into this repository:
   ```bash
   cd /workspace/dan-operating-system
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r real_estate/lead_engine/requirements.txt
   ```
4. Start the local API server:
   ```bash
   uvicorn real_estate.lead_engine.main:app --reload
   ```
5. Open your browser:
   - Lead form: http://127.0.0.1:8000/
   - Leads dashboard: http://127.0.0.1:8000/leads

## API Endpoints

- `GET /` – lead intake form
- `POST /submit` – stores a lead into local SQLite with `created_at`
- `GET /leads` – lead table with status controls
- `POST /leads/{id}/status` – updates lead status (`new/contacted/qualified/nurture/closed`)

## Notes

- The database is local SQLite: `real_estate/lead_engine/leads.db`.
- Logging is enabled via Python's built-in `logging` module.
- Email/follow-up templates are stored in `real_estate/templates/` for reusable messaging.
