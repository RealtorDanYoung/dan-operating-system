# Dan Operating System

A lightweight, modular workspace for real estate lead capture, automation templates, finance operations, and crypto strategy experimentation.

## Repository Structure
- `real_estate/lead_engine` - local FastAPI lead capture app backed by SQLite
- `automation/apps_script` - Google Apps Script templates for sheet-based automation
- `finance_ops` - starter area for finance and operations workflows
- `crypto_lab` - mock-data strategy sandbox with risk management stub
- `docs` - project notes and roadmap

## Run the Real Estate Lead Engine (Local)
```bash
cd real_estate/lead_engine
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000`:
- `/` for lead submission form
- `/leads` for viewing saved leads

## What this repo is for
- Capture local lead data without paid tools
- Prototype automation and data workflows rapidly
- Build future-ready modules for CRM, reporting, and strategy systems

## Suggested Next Upgrades
1. Add Pydantic models + server-side validation for stronger data quality.
2. Add SMTP sender implementation to dispatch `build_email_notification_template` output.
3. Add CRM adapter interface (`HubSpot`, `GoHighLevel`, etc.) with feature flags.
4. Add tests (FastAPI endpoint tests + crypto strategy unit tests).
5. Add `.env` config handling and structured logging across modules.

## Next Recommended Iteration Plan
- **Iteration A:** harden lead engine (validation, dedupe checks, optional authentication)
- **Iteration B:** connect Apps Script endpoint sync and lead scoring fields
- **Iteration C:** add crypto backtest harness and persistent trade journal
- **Iteration D:** build cross-module reporting dashboard in `finance_ops`
