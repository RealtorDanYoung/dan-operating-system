# Daily Workflow

## Morning Setup
1. Activate environment:
   ```bash
   source .venv/bin/activate
   ```
2. Run service:
   ```bash
   uvicorn real_estate.lead_engine.main:app --reload
   ```
3. Open dashboard at `http://127.0.0.1:8000/leads`.

## During the Day
1. Enter each incoming lead from calls/text/email/web into `GET /` form.
2. Review `GET /leads` list every 2-3 hours.
3. Move statuses:
   - `new` → first contact pending
   - `contacted` → reached out
   - `qualified` → actively working
   - `nurture` → long cycle follow-up
   - `closed` → finished/won/lost
4. Use text templates in `real_estate/templates/` for consistent replies.

## End of Day
1. Check all `new` leads have a same-day touch.
2. Export or copy priority leads for next-day schedule.
3. Commit any system improvements to version control.
