from __future__ import annotations

import html
import logging
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI(title="Dan Young Lead Engine", version="0.1.0")

LOGGER = logging.getLogger("lead_engine")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "leads.db"

CONTACT_PREFERENCES = {"call", "text", "email"}
INTEREST_TYPES = {"buyer", "seller", "probate", "other"}
LEAD_STATUSES = {"new", "contacted", "qualified", "nurture", "closed"}
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _db_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with _db_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                contact_preference TEXT NOT NULL,
                interest_type TEXT NOT NULL,
                notes TEXT,
                source TEXT,
                status TEXT NOT NULL DEFAULT 'new',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
    LOGGER.info("Database initialized at %s", DB_PATH)


@app.on_event("startup")
def startup_event() -> None:
    init_db()


def _validate_choice(value: str, allowed: Iterable[str], field: str) -> str:
    normalized = value.strip().lower()
    if normalized not in allowed:
        raise HTTPException(status_code=400, detail=f"Invalid {field}.")
    return normalized


def _validate_email(email: str) -> str:
    normalized = email.strip()
    if normalized and not EMAIL_PATTERN.match(normalized):
        raise HTTPException(status_code=400, detail="Invalid email format.")
    return normalized


@app.get("/", response_class=HTMLResponse)
def form_page() -> str:
    return """
    <html>
      <head><title>Dan Young Lead Form</title></head>
      <body>
        <h1>New Lead Intake</h1>
        <form method='post' action='/submit'>
          <label>Name* <input type='text' name='name' required /></label><br/>
          <label>Phone <input type='text' name='phone' /></label><br/>
          <label>Email <input type='email' name='email' /></label><br/>
          <label>Contact Preference*
            <select name='contact_preference' required>
              <option value='call'>Call</option>
              <option value='text'>Text</option>
              <option value='email'>Email</option>
            </select>
          </label><br/>
          <label>Interest Type*
            <select name='interest_type' required>
              <option value='buyer'>Buyer</option>
              <option value='seller'>Seller</option>
              <option value='probate'>Probate</option>
              <option value='other'>Other</option>
            </select>
          </label><br/>
          <label>Notes <textarea name='notes'></textarea></label><br/>
          <label>Source <input type='text' name='source' /></label><br/>
          <button type='submit'>Save Lead</button>
        </form>
        <p><a href='/leads'>View all leads</a></p>
      </body>
    </html>
    """


@app.post("/submit")
def submit_lead(
    name: str = Form(...),
    phone: str = Form(""),
    email: str = Form(""),
    contact_preference: str = Form(...),
    interest_type: str = Form(...),
    notes: str = Form(""),
    source: str = Form(""),
) -> RedirectResponse:
    clean_name = name.strip()
    if not clean_name:
        raise HTTPException(status_code=400, detail="Name is required.")

    clean_email = _validate_email(email)
    clean_contact_preference = _validate_choice(
        contact_preference, CONTACT_PREFERENCES, "contact preference"
    )
    clean_interest_type = _validate_choice(interest_type, INTEREST_TYPES, "interest type")

    now = datetime.now(timezone.utc).isoformat()

    with _db_connection() as connection:
        connection.execute(
            """
            INSERT INTO leads (
                name, phone, email, contact_preference,
                interest_type, notes, source, status,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 'new', ?, ?)
            """,
            (
                clean_name,
                phone.strip(),
                clean_email,
                clean_contact_preference,
                clean_interest_type,
                notes.strip(),
                source.strip(),
                now,
                now,
            ),
        )

    LOGGER.info("Lead submitted: name=%s interest=%s", clean_name, clean_interest_type)
    return RedirectResponse(url="/leads", status_code=303)


@app.get("/leads", response_class=HTMLResponse)
def list_leads() -> str:
    with _db_connection() as connection:
        leads = connection.execute("SELECT * FROM leads ORDER BY created_at DESC").fetchall()

    rows = []
    for lead in leads:
        rows.append(
            f"""
            <tr>
                <td>{lead['id']}</td>
                <td>{html.escape(lead['name'])}</td>
                <td>{html.escape(lead['phone'] or '')}</td>
                <td>{html.escape(lead['email'] or '')}</td>
                <td>{html.escape(lead['contact_preference'])}</td>
                <td>{html.escape(lead['interest_type'])}</td>
                <td>{html.escape(lead['source'] or '')}</td>
                <td>{html.escape(lead['status'])}</td>
                <td>{html.escape(lead['created_at'])}</td>
                <td>
                    <form method='post' action='/leads/{lead['id']}/status'>
                        <select name='status'>
                            {''.join(_status_options(lead['status']))}
                        </select>
                        <button type='submit'>Update</button>
                    </form>
                </td>
            </tr>
            """
        )

    return f"""
    <html>
      <head><title>Lead Dashboard</title></head>
      <body>
        <h1>Lead Dashboard</h1>
        <p><a href='/'>Add new lead</a></p>
        <table border='1' cellpadding='6'>
          <thead>
            <tr>
              <th>ID</th><th>Name</th><th>Phone</th><th>Email</th><th>Preference</th>
              <th>Interest</th><th>Source</th><th>Status</th><th>Created</th><th>Follow-up</th>
            </tr>
          </thead>
          <tbody>
            {''.join(rows) or '<tr><td colspan="10">No leads yet.</td></tr>'}
          </tbody>
        </table>
      </body>
    </html>
    """


def _status_options(current: str) -> list[str]:
    options = []
    for status in sorted(LEAD_STATUSES):
        selected = "selected" if status == current else ""
        options.append(f"<option value='{status}' {selected}>{status.title()}</option>")
    return options


@app.post("/leads/{lead_id}/status")
def update_status(lead_id: int, status: str = Form(...)) -> RedirectResponse:
    clean_status = _validate_choice(status, LEAD_STATUSES, "status")
    updated_at = datetime.now(timezone.utc).isoformat()

    with _db_connection() as connection:
        cursor = connection.execute(
            "UPDATE leads SET status = ?, updated_at = ? WHERE id = ?",
            (clean_status, updated_at, lead_id),
        )

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Lead not found.")

    LOGGER.info("Lead status updated: id=%s status=%s", lead_id, clean_status)
    return RedirectResponse(url="/leads", status_code=303)
