from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "leads.db"

app = FastAPI(title="Real Estate Lead Engine")


INTEREST_OPTIONS = [
    "Buy",
    "Sell",
    "Invest",
    "Rent",
    "Other",
]


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                interest_type TEXT NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request, success: Optional[str] = None) -> str:
    options_html = "".join(
        [f'<option value="{option}">{option}</option>' for option in INTEREST_OPTIONS]
    )
    success_banner = (
        "<p style='color: green; font-weight: bold;'>Lead saved successfully.</p>"
        if success
        else ""
    )
    return f"""
    <html>
        <head>
            <title>Real Estate Lead Engine</title>
            <meta charset="UTF-8" />
        </head>
        <body style="font-family: Arial, sans-serif; max-width: 720px; margin: 2rem auto;">
            <h1>Local Real Estate Lead Form</h1>
            <p>Capture local prospects and store them in SQLite.</p>
            {success_banner}
            <form action="/submit" method="post">
                <label>Name</label><br />
                <input type="text" name="name" required style="width: 100%; margin-bottom: 0.75rem;" />

                <label>Phone</label><br />
                <input type="tel" name="phone" required style="width: 100%; margin-bottom: 0.75rem;" />

                <label>Email</label><br />
                <input type="email" name="email" required style="width: 100%; margin-bottom: 0.75rem;" />

                <label>Interest Type</label><br />
                <select name="interest_type" required style="width: 100%; margin-bottom: 0.75rem;">
                    {options_html}
                </select>

                <label>Notes</label><br />
                <textarea name="notes" rows="4" style="width: 100%; margin-bottom: 0.75rem;"></textarea>

                <button type="submit">Save Lead</button>
            </form>

            <p style="margin-top: 1rem;"><a href="/leads">View Saved Leads</a></p>
        </body>
    </html>
    """


@app.post("/submit")
def submit_lead(
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    interest_type: str = Form(...),
    notes: str = Form(""),
) -> RedirectResponse:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO leads (name, phone, email, interest_type, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name.strip(), phone.strip(), email.strip(), interest_type.strip(), notes.strip()),
        )
        conn.commit()

    # Notification template placeholder for future SMTP/CRM integration.
    build_email_notification_template(name, phone, email, interest_type, notes)

    return RedirectResponse(url="/?success=1", status_code=303)


@app.get("/leads", response_class=HTMLResponse)
def list_leads() -> str:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, name, phone, email, interest_type, notes, created_at
            FROM leads
            ORDER BY created_at DESC, id DESC
            """
        ).fetchall()

    table_rows = "".join(
        [
            f"""
            <tr>
                <td>{row['id']}</td>
                <td>{row['name']}</td>
                <td>{row['phone']}</td>
                <td>{row['email']}</td>
                <td>{row['interest_type']}</td>
                <td>{row['notes']}</td>
                <td>{row['created_at']}</td>
            </tr>
            """
            for row in rows
        ]
    )

    return f"""
    <html>
        <head>
            <title>Saved Leads</title>
            <meta charset="UTF-8" />
        </head>
        <body style="font-family: Arial, sans-serif; max-width: 1000px; margin: 2rem auto;">
            <h1>Saved Leads</h1>
            <p><a href="/">Back to Form</a></p>
            <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%;">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Phone</th>
                        <th>Email</th>
                        <th>Interest</th>
                        <th>Notes</th>
                        <th>Created At</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows if table_rows else '<tr><td colspan="7">No leads saved yet.</td></tr>'}
                </tbody>
            </table>
        </body>
    </html>
    """


def build_email_notification_template(
    name: str,
    phone: str,
    email: str,
    interest_type: str,
    notes: str,
) -> str:
    """Returns a structured email body that can be sent by a future notification layer."""
    return (
        "New Real Estate Lead\n"
        "---------------------\n"
        f"Name: {name}\n"
        f"Phone: {phone}\n"
        f"Email: {email}\n"
        f"Interest Type: {interest_type}\n"
        f"Notes: {notes or 'None'}\n"
    )
