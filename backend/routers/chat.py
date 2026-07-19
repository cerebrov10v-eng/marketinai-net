"""Chat router for MarketinAI assistant."""
import os
import json
import logging
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger("marketinai.chat")

router = APIRouter(tags=["chat"])

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


class ChatMessage(BaseModel):
    role: str  # user / assistant / system
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = "gpt-4o-mini"
    temperature: Optional[float] = 0.7


class ChatResponse(BaseModel):
    reply: str
    model: Optional[str] = None


SYSTEM_PROMPT = """Eres Amanda, la asistente de MarketinAI, una agencia de marketing con IA para PYMEs españolas.
Responde de forma clara, concisa y orientada a resultados. Si el usuario pregunta por precios,
menciona los planes Starter (49€/mes), Pro (99€/mes) y Agency (199€/mes), todos con trial gratis.
Si quiere reservar o comprar, guíalo al formulario de lead o a /precios.
Nunca inventes funciones que no existan; si no sabes algo, pide su email para que un humano le contacte.
"""


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend([{"role": m.role, "content": m.content} for m in payload.messages])

    if OPENAI_API_KEY:
        try:
            import openai
            client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
            response = await client.chat.completions.create(
                model=payload.model or "gpt-4o-mini",
                messages=messages,
                temperature=payload.temperature or 0.7,
            )
            return ChatResponse(
                reply=response.choices[0].message.content,
                model=response.model,
            )
        except Exception as exc:
            logger.error("OpenAI chat error: %s", exc)
            # fallback to static reply
            pass

    # Static fallback for common intents
    last = payload.messages[-1].content.lower() if payload.messages else ""
    if "precio" in last or "plan" in last or "cuanto" in last:
        reply = (
            "Tenemos 3 planes: Starter 49€/mes, Pro 99€/mes y Agency 199€/mes. "
            "Todos incluyen 14 días de trial gratis. ¿Te gustaría que te reserve una demo?"
        )
    elif "demo" in last or "probar" in last:
        reply = "Puedes empezar tu trial gratis de 14 días sin tarjeta. Déjame tu email y te envío el acceso."
    elif "hola" in last or "buenas" in last:
        reply = "¡Hola! Soy Amanda de MarketinAI. ¿En qué puedo ayudarte hoy?"
    else:
        reply = (
            "Entendido. Para darte la mejor respuesta, ¿puedes dejarme tu email? "
            "Así un experto de MarketinAI te contactará en menos de 24h."
        )

    return ChatResponse(reply=reply, model="fallback")
