"""
VitaLens — routes/hospitals.py
"""
from fastapi import APIRouter, Query
from services.hospital_finder import find_hospitals

router = APIRouter()

@router.get("/nearby")
async def get_hospitals(
    city: str = Query(..., description="User's city"),
    disease: str = Query(..., description="Disease key: diabetes|heart|hypertension|liver"),
    limit: int = Query(4, ge=1, le=10)
):
    hospitals = find_hospitals(city, disease, limit)
    return {"city": city, "disease": disease, "hospitals": hospitals, "count": len(hospitals)}
