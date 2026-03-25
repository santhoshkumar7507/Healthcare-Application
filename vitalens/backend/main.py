"""
VitaLens — Health Intelligence Platform
Backend Entry Point  |  main.py

Run: uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

load_dotenv()

from database import engine, Base
from routes.predict   import router as predict_router
from routes.records   import router as records_router
from routes.hospitals import router as hospitals_router
from routes.auth      import router as auth_router


# ─── Lifespan ───────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    print("✓ VitaLens API started")
    print("✓ Database ready")
    yield
    # Shutdown
    print("VitaLens API stopped")


# ─── App ────────────────────────────────────────────────
app = FastAPI(
    title="VitaLens API",
    description="AI-powered disease risk prediction",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# ─── CORS ───────────────────────────────────────────────
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5500").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ────────────────────────────────────────────
app.include_router(auth_router,      prefix="/api/auth",      tags=["Authentication"])
app.include_router(predict_router,   prefix="/api/predict",   tags=["Disease Prediction"])
app.include_router(records_router,   prefix="/api/records",   tags=["Health Records"])
app.include_router(hospitals_router, prefix="/api/hospitals", tags=["Hospital Finder"])


# ─── Health Check ───────────────────────────────────────
@app.get("/api/health", tags=["System"])
async def health():
    return {"status": "ok", "service": "VitaLens", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
