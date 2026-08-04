import time
import logging
import json
from fastapi import FastAPI, HTTPException, BackgroundTasks, status
from config.settings import settings
from pipeline.validation import TicketIngestionSchema
from worker import queue_triage_job
import redis

# Milestone 4: Structured JSON Telemetry Configurations
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("aetcg_telemetry")

app = FastAPI(
    title="Autonomous Enterprise Triage & Compliance Guard (AETCG)",
    version="1.0.0-rc1"
)

# Milestone 6: Redis Connection Pool for In-Memory Caching
redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

@app.post("/api/v1/triage", status_code=status.HTTP_202_ACCEPTED)
async def ingest_ticket(payload: TicketIngestionSchema):
    start_time = time.time()
    payload_hash = hash(payload.raw_text)
    
    # Milestone 6: Optimization / Query Caching Layer
    cached_result = redis_client.get(f"cache:{payload_hash}")
    if cached_result:
        logger.info(json.dumps({
            "event": "cache_hit", 
            "latency_ms": (time.time() - start_time) * 1000
        }))
        return json.loads(cached_result)

    try:
        # Milestone 4: Enqueue task asynchronously to decouple runtime processing
        job = queue_triage_job(payload.model_dump())
        
        logger.info(json.dumps({
            "event": "ticket_ingested_and_queued",
            "job_id": job.id,
            "latency_ms": (time.time() - start_time) * 1000
        }))
        return {"status": "queued", "job_id": job.id, "message": "Ticket verification initiated."}
        
    except Exception as e:
        logger.error(json.dumps({"event": "ingestion_failure", "error": str(e)}))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal messaging backbone unreached."
        )

# State Check Endpoint
@app.get("/api/v1/state/{job_id}")
async def get_state(job_id: str):
    state_key = f"state:{job_id}"
    ticket_state = redis_client.get(state_key)
    if not ticket_state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="State vector context unrecovered.")

    return json.loads(ticket_state)

# Milestone 5: Human-In-The-Loop Interactive Webhook Routing
@app.put("/api/v1/approve/{job_id}", status_code=status.HTTP_200_OK)
async def administrative_approval_gate(job_id: str, action: str, supervisor_token: str):
    if supervisor_token != "SECURE_GOVERNANCE_TOKEN_XYZ":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized gate access.")
        
    # Simulate loading state container from database/Redis cache and advancing graph
    state_key = f"state:{job_id}"
    cached_state = redis_client.get(state_key)
    if not cached_state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="State vector context unrecovered.")
        
    state = json.loads(cached_state)
    state["human_approval"] = action
    state["status"] = "COMPLETED" if action == "APPROVE" else "REJECTED"
    
    redis_client.set(state_key, json.dumps(state))
    
    logger.info(json.dumps({"event": "human_gate_resolved", "job_id": job_id, "decision": action}))
    return {"status": "state_resumed", "final_disposition": state["status"]}
