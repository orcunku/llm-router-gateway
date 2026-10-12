import logging
import os
import secrets
import time

import httpx
from fastapi import FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from router.engine import AdaptiveRouter, RequestMetaData
from serving.adapters import ModelDispatcher

app = FastAPI(title="Multi-Model LLM Gateway")
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

router_engine = AdaptiveRouter()
dispatcher = ModelDispatcher()


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "LLM Gateway Router"}


@app.post("/v1/chat/completions")
async def handle_request(
    req: RequestMetaData,
    authorization: str | None = Header(default=None),
):
    api_auth_token = os.getenv("API_AUTH_TOKEN", "")
    if not api_auth_token:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Gateway authentication is not configured.",
        )

    scheme, _, supplied_token = (authorization or "").partition(" ")
    if (
        scheme.lower() != "bearer"
        or not supplied_token
        or not secrets.compare_digest(supplied_token, api_auth_token)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A valid bearer token is required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    start_time = time.time()
    selected_model = router_engine.route(req)

    try:
        response_text = await dispatcher.dispatch(selected_model, req.prompt)
    except httpx.HTTPError as exc:
        logger.error("Model provider request failed: %s", type(exc).__name__)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Model provider request failed.",
        ) from None

    total_latency = round((time.time() - start_time) * 1000, 2)
    return {
        "response": response_text,
        "model_used": selected_model,
        "latency_ms": total_latency,
        "cached": False,
    }
