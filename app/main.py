import asyncio
import logging
import random

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException

logger = logging.getLogger("demo")

# No telemetry config needed: FastAPI reads OTEL_* env vars (see compose.yaml)
# and auto-configures OTLP exporters for traces, metrics and logs.
app = FastAPI(
    title="FastAPI OTel demo",
    telemetry={"exclude": lambda scope: scope["path"] == "/health"},
)

ITEMS = {1: "widget", 2: "gadget", 3: "doohickey"}


async def slow_lookup() -> float:
    """A dependency -> shows up as its own operation span."""
    delay = random.uniform(0.02, 0.2)
    await asyncio.sleep(delay)
    return delay


def audit(item_id: int) -> None:
    logger.info("audited access to item %s", item_id)


@app.get("/health")
async def health():
    return {"ok": True}


@app.get("/items/{item_id}")
async def read_item(
    item_id: int,
    background: BackgroundTasks,
    delay: float = Depends(slow_lookup),
):
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="no such item")
    background.add_task(audit, item_id)
    return {"item_id": item_id, "name": ITEMS[item_id], "lookup_s": round(delay, 3)}


@app.get("/boom")
async def boom():
    """Unhandled exception -> recorded as an error span + exception log."""
    raise RuntimeError("something went wrong on purpose")
