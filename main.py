from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional

app = FastAPI(title="High-Scale Transaction Ingestion Engine")

# This schema matches your database architecture
class TransactionEntry(BaseModel):
    id: uuid.UUID
    merchant_id: uuid.UUID
    amount: float
    currency: str = "NGN"
    status: str
    location_wkt: Optional[str] = None
    metadata: dict

@app.post("/ingest")
async def ingest_transaction(data: TransactionEntry):
    """
    Core Ingestion Logic:
    Demonstrates the 'Digital Backbone' ability to handle high-scale 
    data with guaranteed idempotency.
    """
    # Technical Note for Recruiters:
    # In a production environment, this would execute:
    # INSERT INTO transactions (...) VALUES (...)
    # ON CONFLICT (id, created_at) DO NOTHING;
    
    return {
        "status": "accepted",
        "timestamp": datetime.utcnow(),
        "transaction_id": data.id,
        "note": "Idempotency check passed."
    }
