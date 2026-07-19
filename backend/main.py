"""MarketinAI backend: lead capture + health + static files."""
import json
import logging
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("marketinai")

DB_PATH = os.getenv("LEADS_DB_PATH", "/data/leads.db")
STATIC_DIR = os.getenv("STATIC_DIR", "/app/static")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def init_db():
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT,
                nombre TEXT,
                email TEXT NOT NULL,
                telefono TEXT,
                empresa TEXT,
                web TEXT,
                vertical TEXT,
                mensaje TEXT,
                extras TEXT,
                consent_rgpd BOOLEAN,
                consent_marketing BOOLEAN,
                source TEXT,
                created_at TEXT
            )
            """
        )
        conn.commit()


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close()


app = FastAPI(
    title="MarketinAI Backend",
    description="Lead capture and static file serving for marketinai.net",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response


class LeadPayload(BaseModel):
    service: str = "MKAI-AE-99"
    nombre: str = ""
    email: EmailStr
    telefono: str = ""
    empresa: str = ""
    web: str = ""
    vertical: str = ""
    mensaje: str = ""
    extras: dict = Field(default_factory=dict)
    consent_rgpd: bool = False
    consent_marketing: bool = False
    source: str = "marketinai.net"
    ts: str = ""


@app.on_event("startup")
async def startup():
    init_db()


@app.get("/api/marketinai/health")
async def health():
    return {"status": "ok", "service": "marketinai", "version": "1.0.0"}


@app.post("/api/marketinai/lead-capture")
async def lead_capture(payload: LeadPayload):
    if not payload.consent_rgpd:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "Se requiere el consentimiento RGPD."},
        )
    try:
        with get_db() as conn:
            conn.execute(
                """
                INSERT INTO leads
                (service, nombre, email, telefono, empresa, web, vertical, mensaje,
                 extras, consent_rgpd, consent_marketing, source, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload.service,
                    payload.nombre,
                    payload.email.lower().strip(),
                    payload.telefono,
                    payload.empresa,
                    payload.web,
                    payload.vertical,
                    payload.mensaje,
                    json.dumps(payload.extras) if payload.extras else None,
                    payload.consent_rgpd,
                    payload.consent_marketing,
                    payload.source,
                    payload.ts or datetime.now(timezone.utc).isoformat(),
                ),
            )
            conn.commit()
            lead_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        logger.info("Lead captured: id=%s service=%s email=%s", lead_id, payload.service, payload.email)
        return {
            "success": True,
            "message": "Lead captured. Te contactamos en menos de 24h.",
            "lead_id": lead_id,
        }
    except Exception as exc:
        logger.error("Lead capture error: %s", exc)
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Error al guardar el lead. Intenta por email o Telegram."},
        )


@app.get("/api/marketinai/leads")
async def list_leads():
    """Admin endpoint to list recent leads (basic, no auth for now)."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT id, service, nombre, email, web, created_at FROM leads ORDER BY id DESC LIMIT 100"
        ).fetchall()
    return {"leads": [{"id": r[0], "service": r[1], "nombre": r[2], "email": r[3], "web": r[4], "created_at": r[5]} for r in rows]}


# Static files at the end so API routes take precedence
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
