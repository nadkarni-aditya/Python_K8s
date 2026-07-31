from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from prometheus_fastapi_instrumentator import Instrumentator

from . import models
from .database import engine
from .routers import auth, mediaposts, user, vote
from .config import settings

# models.Base.metadata.create_all(bind=engine)  # Alembic owns the schema now

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mediaposts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# --- Operational endpoints -------------------------------------------------
# /health = liveness: "is the process alive?" No DB check. k8s RESTARTS the pod if this fails.
# /ready  = readiness: "can I serve traffic?" Checks DB. k8s STOPS ROUTING to the pod if this
#           fails (but doesn't restart it). This is what makes rolling updates zero-downtime.
@app.get("/health", tags=["Ops"])
def health():
    return {"status": "ok"}


@app.get("/ready", tags=["Ops"])
def ready():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not ready", "reason": "database unreachable"},
        )


# /metrics — Prometheus scrapes this. Exposes per-route request counts, latency
# histograms, and status codes: everything needed for RPS, p95, and error rate.
Instrumentator().instrument(app).expose(app, endpoint="/metrics", tags=["Ops"])