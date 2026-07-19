"""
MarketinAI standalone backend API.
Serves /api/marketinai/* endpoints without depending on Cerebro V10 monolith.
"""
import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routers import health, leads, checkout, chat

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("marketinai.api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    logger.info("MarketinAI API started")
    yield
    logger.info("MarketinAI API shutting down")


app = FastAPI(
    title="MarketinAI API",
    description="Standalone backend for marketinai.net",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers under /api/marketinai prefix
app.include_router(health.router, prefix="/api/marketinai")
app.include_router(leads.router, prefix="/api/marketinai")
app.include_router(checkout.router, prefix="/api/marketinai")
app.include_router(chat.router, prefix="/api/marketinai")


@app.get("/")
async def root():
    return {"status": "MarketinAI API", "docs": "/docs"}
