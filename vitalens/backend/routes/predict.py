"""
VitaLens — rule-based disease prediction engine
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class AssessmentInput(BaseModel):
    name: str = "User"
    city: str = ""
    activity_text: str = ""
    symptoms: List[str] = []

@router.post("")
@router.post("/")
@router.post("/analyze")
async def analyze(data: AssessmentInput):
    # Local Rule-Based Engine
    text = data.activity_text.lower()
    symptoms = [s.lower() for s in data.symptoms]
    
    # 1. Scoring logic for Diabetes
    diabetes_score = 0
    diab_keywords = ["sugar", "sweet", "soda", "thirsty", "pizza", "junk", "sit", "desk", "lazy", "couch", "eat a lot", "fast food"]
    for kw in diab_keywords:
        if kw in text:
            diabetes_score += 1
            
    if "frequent urination" in symptoms or "high thirst" in symptoms or "blurred vision" in symptoms:
        diabetes_score += 3
        
    # 2. Scoring logic for Heart Disease
    heart_score = 0
    heart_keywords = ["smoke", "alcohol", "beer", "drink", "stress", "chest", "fat", "fried", "sit", "desk", "no exercise", "lazy"]
    for kw in heart_keywords:
        if kw in text:
            heart_score += 1
            
    if "chest pain" in symptoms or "palpitations" in symptoms or "breathlessness" in symptoms:
        heart_score += 3

    # 3. Hypertension
    hyp_score = 0
    hyp_keywords = ["salt", "stress", "smoke", "alcohol", "obese", "sit", "desk", "lazy", "fast food"]
    for kw in hyp_keywords:
        if kw in text:
            hyp_score += 1
    if "headache" in symptoms or "dizziness" in symptoms or "fatigue" in symptoms:
        hyp_score += 3
        
    # 4. Liver Disease
    liver_score = 0
    liver_keywords = ["alcohol", "beer", "drink", "fat", "fried", "junk", "medicine"]
    for kw in liver_keywords:
        if kw in text:
            liver_score += 1
    if "nausea" in symptoms or "weight loss" in symptoms or "indigestion" in symptoms:
        liver_score += 3

    # 5. Kidney Disease
    kidney_score = 0
    kidney_keywords = ["salt", "smoke", "diabetes", "blood pressure", "pain killer", "supplements"]
    for kw in kidney_keywords:
        if kw in text:
            kidney_score += 1
    if "frequent urination" in symptoms or "fatigue" in symptoms or "nausea" in symptoms:
        kidney_score += 3

    # Prediction decision
    scores = {
        "diabetes": diabetes_score, 
        "heart": heart_score, 
        "hypertension": hyp_score, 
        "liver": liver_score, 
        "kidney": kidney_score
    }
    
    key = max(scores, key=scores.get)
    if scores[key] == 0:
        key = "diabetes"
    
    return {
        "status": "success",
        "disease_key": key,
        "diabetes_score": diabetes_score,
        "heart_score": heart_score,
        "patient_name": data.name,
        "city": data.city
    }
