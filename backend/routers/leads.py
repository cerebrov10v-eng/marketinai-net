"""Lead capture router."""
import json
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from database import get_db, Lead

router = APIRouter(tags=["leads"])


class LeadCaptureRequest(BaseModel):
    email: EmailStr
    service: str = "marketinai"
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    empresa: Optional[str] = None
    web: Optional[str] = None
    vertical: Optional[str] = None
    mensaje: Optional[str] = None
    extras: Optional[dict] = Field(default_factory=dict)
    consent_rgpd: bool = False
    consent_marketing: bool = False
    source: str = "marketinai"
    funnel: str = "services"
    url: Optional[str] = None
    tags: Optional[str] = None
    metadata: Optional[dict] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_content: Optional[str] = None
    utm_term: Optional[str] = None


class LeadResponse(BaseModel):
    success: bool
    message: str
    lead_id: Optional[int] = None


@router.post("/lead-capture", response_model=LeadResponse)
async def lead_capture(payload: LeadCaptureRequest, db: Session = Depends(get_db)):
    if not payload.consent_rgpd:
        raise HTTPException(status_code=400, detail="Se requiere el consentimiento RGPD.")
    try:
        lead = Lead(
            email=payload.email.lower().strip(),
            service=payload.service,
            nombre=payload.nombre,
            telefono=payload.telefono,
            empresa=payload.empresa,
            web=payload.web,
            vertical=payload.vertical,
            mensaje=payload.mensaje,
            extras=json.dumps(payload.extras) if payload.extras else None,
            consent_rgpd=payload.consent_rgpd,
            consent_marketing=payload.consent_marketing,
            source=payload.source,
            funnel=payload.funnel,
            url=payload.url,
            tags=payload.tags,
            metadata_json=json.dumps(payload.metadata) if payload.metadata else None,
            utm_source=payload.utm_source,
            utm_medium=payload.utm_medium,
            utm_campaign=payload.utm_campaign,
            utm_content=payload.utm_content,
            utm_term=payload.utm_term,
        )
        db.add(lead)
        db.commit()
        db.refresh(lead)
        return LeadResponse(success=True, message="Lead captured", lead_id=lead.id)
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save lead: {exc}")
