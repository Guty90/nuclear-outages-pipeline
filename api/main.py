import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.data    import router as data_router
from routes.refresh import router as refresh_router

# ── Logging ──────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ── App ───────────────────────────────────────────────────────────
app = FastAPI(
    title="Nuclear Outages API",
    description="API for querying U.S. Nuclear Outages data from the EIA",
    version="1.0.0",
)

# ── CORS ──────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ────────────────────────────────────────────────────────
app.include_router(data_router)
app.include_router(refresh_router)