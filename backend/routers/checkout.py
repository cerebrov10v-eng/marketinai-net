"""Stripe checkout and webhook router."""
import os
import json
import logging
import time
import hashlib
from datetime import datetime, timezone
from typing import Optional

import requests
import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, Header
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from database import get_db, Order

logger = logging.getLogger("marketinai.checkout")

router = APIRouter(tags=["checkout"])

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY

# Analytics config
GA4_MEASUREMENT_ID = os.getenv("GA4_MEASUREMENT_ID", "G-5LBQF27NSV")
GA4_API_SECRET = os.getenv("GA4_API_SECRET", "")
META_PIXEL_ID = os.getenv("META_PIXEL_ID", "4569300959968212")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")

# Product catalog
PRODUCT_CATALOG = {
    "marketinai_starter_monthly": {
        "name": "MarketinAI Starter",
        "description": "Plan Starter mensual",
        "amount": 4900,
        "currency": "EUR",
        "type": "subscription",
        "interval": "month",
    },
    "marketinai_pro_monthly": {
        "name": "MarketinAI Pro",
        "description": "Plan Pro mensual",
        "amount": 9900,
        "currency": "EUR",
        "type": "subscription",
        "interval": "month",
    },
    "marketinai_agency_monthly": {
        "name": "MarketinAI Agency",
        "description": "Plan Agency mensual",
        "amount": 19900,
        "currency": "EUR",
        "type": "subscription",
        "interval": "month",
    },
    "marketinai_starter_yearly": {
        "name": "MarketinAI Starter (Anual)",
        "description": "Plan Starter anual (2 meses gratis)",
        "amount": 49000,
        "currency": "EUR",
        "type": "subscription",
        "interval": "year",
    },
    "marketinai_pro_yearly": {
        "name": "MarketinAI Pro (Anual)",
        "description": "Plan Pro anual (2 meses gratis)",
        "amount": 99000,
        "currency": "EUR",
        "type": "subscription",
        "interval": "year",
    },
    "marketinai_agency_yearly": {
        "name": "MarketinAI Agency (Anual)",
        "description": "Plan Agency anual (2 meses gratis)",
        "amount": 199000,
        "currency": "EUR",
        "type": "subscription",
        "interval": "year",
    },
    "marketinai_setup": {
        "name": "MarketinAI Setup DFY",
        "description": "Setup Done-For-You (one-time)",
        "amount": 39700,
        "currency": "EUR",
        "type": "payment",
    },
    "marketinai_e2e_test": {
        "name": "MarketinAI E2E Test",
        "description": "Validación temporal del flujo de pago (1€, reembolsable)",
        "amount": 100,
        "currency": "EUR",
        "type": "payment",
    },
}


def get_price_id(product_id: str) -> Optional[str]:
    """Return Stripe price ID from env if configured, else None."""
    mapping = json.loads(os.getenv("STRIPE_PRICE_MAP", "{}"))
    return mapping.get(product_id)


class CheckoutRequest(BaseModel):
    product: str
    email: EmailStr
    success_url: Optional[str] = None
    cancel_url: Optional[str] = None
    metadata: Optional[dict] = None


class CheckoutResponse(BaseModel):
    checkout_url: str
    session_id: str


@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout(payload: CheckoutRequest, db: Session = Depends(get_db)):
    if not STRIPE_SECRET_KEY:
        raise HTTPException(status_code=503, detail="Stripe not configured")

    product = PRODUCT_CATALOG.get(payload.product)
    if not product:
        raise HTTPException(status_code=400, detail=f"Unknown product: {payload.product}")

    success_url = payload.success_url or os.getenv(
        "STRIPE_SUCCESS_URL", "https://marketinai.net/pago-exitoso?session_id={CHECKOUT_SESSION_ID}"
    )
    cancel_url = payload.cancel_url or os.getenv(
        "STRIPE_CANCEL_URL", "https://marketinai.net/pricing"
    )

    # Save order record
    order = Order(
        email=payload.email.lower().strip(),
        tier=payload.product,
        amount=product["amount"] / 100,
        currency=product["currency"],
        status="pending",
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    line_items = []
    price_id = get_price_id(payload.product)
    if price_id:
        line_items.append({"price": price_id, "quantity": 1})
    else:
        price_data = {
            "currency": product["currency"].lower(),
            "unit_amount": product["amount"],
            "product_data": {
                "name": product["name"],
                "description": product.get("description"),
            },
        }
        if product.get("type") == "subscription":
            price_data["recurring"] = {"interval": product.get("interval", "month")}
        line_items.append({"price_data": price_data, "quantity": 1})

    mode = "subscription" if product.get("type") == "subscription" else "payment"

    try:
        session = stripe.checkout.Session.create(
            customer_email=payload.email,
            line_items=line_items,
            mode=mode,
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                "order_id": str(order.id),
                "tier": payload.product,
                **(payload.metadata or {}),
            },
        )
        order.stripe_session_id = session.id
        db.commit()
        return CheckoutResponse(checkout_url=session.url, session_id=session.id)
    except Exception as exc:
        db.rollback()
        logger.error("Stripe checkout error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    if STRIPE_WEBHOOK_SECRET:
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
        except stripe.error.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid signature")
    else:
        event = json.loads(payload)

    if event.get("type") == "checkout.session.completed":
        session = event["data"]["object"]
        order_id = session.get("metadata", {}).get("order_id")
        if order_id:
            order = db.query(Order).filter(Order.id == int(order_id)).first()
            if order:
                order.status = "paid"
                order.paid_at = datetime.now(timezone.utc)
                order.stripe_payment_intent = session.get("payment_intent") or session.get("subscription")
                db.commit()
                logger.info("Order %s marked as paid", order_id)
                try:
                    send_purchase_events(session)
                except Exception as exc:
                    logger.error("Failed to send purchase events: %s", exc)

    return {"received": True}


@router.get("/verify-session")
async def verify_session(session_id: str):
    """Verify a Stripe Checkout session and return payment details."""
    if not STRIPE_SECRET_KEY:
        raise HTTPException(status_code=503, detail="Stripe not configured")
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id required")

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except stripe.error.InvalidRequestError:
        raise HTTPException(status_code=404, detail="Session not found")
    except stripe.error.AuthenticationError:
        logger.error("Stripe authentication error: invalid API key")
        raise HTTPException(status_code=503, detail="Stripe API key invalid")
    except stripe.error.APIConnectionError:
        logger.error("Stripe connection error")
        raise HTTPException(status_code=503, detail="Stripe unavailable")
    except Exception as exc:
        logger.error("Stripe verify-session error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))

    return {
        "verified": session.payment_status == "paid",
        "payment_status": session.payment_status,
        "amount": session.amount_total / 100 if session.amount_total else 0,
        "currency": session.currency.upper() if session.currency else "EUR",
        "plan": session.metadata.get("tier", "unknown") if session.metadata else "unknown",
        "customer_email": session.customer_email,
    }


def _hash_email(email: Optional[str]) -> Optional[str]:
    if not email:
        return None
    return hashlib.sha256(email.lower().strip().encode()).hexdigest()


def send_purchase_events(session: dict):
    """Send purchase event to GA4 (Measurement Protocol) and Meta Conversions API."""
    amount = (session.get("amount_total") or 0) / 100
    currency = (session.get("currency") or "eur").upper()
    plan = session.get("metadata", {}).get("tier", "unknown")
    transaction_id = session.get("id")
    customer_email = session.get("customer_email")
    client_id = session.get("client_reference_id") or transaction_id or "unknown"

    # GA4 Measurement Protocol
    if GA4_API_SECRET and GA4_MEASUREMENT_ID:
        try:
            ga4_payload = {
                "client_id": client_id,
                "events": [{
                    "name": "purchase",
                    "params": {
                        "transaction_id": transaction_id,
                        "value": amount,
                        "currency": currency,
                        "plan": plan,
                        "items": [{"item_name": plan, "quantity": 1, "price": amount}],
                    },
                }],
            }
            requests.post(
                f"https://www.google-analytics.com/mp/collect?measurement_id={GA4_MEASUREMENT_ID}&api_secret={GA4_API_SECRET}",
                json=ga4_payload,
                timeout=5,
            )
            logger.info("Sent GA4 purchase event for %s", transaction_id)
        except Exception as exc:
            logger.error("GA4 purchase event failed: %s", exc)

    # Meta Conversions API
    if META_ACCESS_TOKEN and META_PIXEL_ID:
        try:
            user_data = {}
            email_hash = _hash_email(customer_email)
            if email_hash:
                user_data["em"] = email_hash

            meta_payload = {
                "data": [{
                    "event_name": "Purchase",
                    "event_time": int(time.time()),
                    "user_data": user_data,
                    "custom_data": {
                        "value": amount,
                        "currency": currency,
                        "content_name": plan,
                        "plan": plan,
                        "transaction_id": transaction_id,
                    },
                    "action_source": "website",
                    "event_source_url": "https://marketinai.net/pago-exitoso",
                }],
            }
            requests.post(
                f"https://graph.facebook.com/v18.0/{META_PIXEL_ID}/events",
                params={"access_token": META_ACCESS_TOKEN},
                json=meta_payload,
                timeout=5,
            )
            logger.info("Sent Meta purchase event for %s", transaction_id)
        except Exception as exc:
            logger.error("Meta purchase event failed: %s", exc)
