"""VitaLens — routes/records.py"""
from fastapi import APIRouter, HTTPException
from blockchain.service import BlockchainService

router = APIRouter()

@router.get("/{patient_id}")
async def get_records(patient_id: str):
    bc = BlockchainService()
    records = bc.get_patient_records(patient_id)
    return {"patient_id": patient_id, "records": records}

@router.get("/{patient_id}/latest")
async def get_latest(patient_id: str):
    bc = BlockchainService()
    records = bc.get_patient_records(patient_id)
    if not records:
        raise HTTPException(404, "No records found")
    return records[-1]
