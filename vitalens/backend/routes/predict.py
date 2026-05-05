"""
AuraHealth — rule-based disease prediction engine
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
    age: Optional[str] = None
    gender: Optional[str] = None
    bmi: Optional[str] = None
    sugar: Optional[str] = None
    bp: Optional[str] = None
    chol: Optional[str] = None
    family_history: List[str] = []

@router.post("")
@router.post("/")
@router.post("/analyze")
async def analyze(data: AssessmentInput):
    # Local Rule-Based Engine
    text = data.activity_text.lower()
    symptoms = [s.lower() for s in data.symptoms]
    family = [f.lower() for f in data.family_history]
    
    # 1. Scoring logic for Diabetes
    diabetes_score = 0
    diab_keywords = ["sugar", "sweet", "soda", "thirsty", "pizza", "junk", "sit", "desk", "lazy", "couch", "eat a lot", "fast food"]
    for kw in diab_keywords:
        if kw in text:
            diabetes_score += 1
            
    if "frequent urination" in symptoms or "high thirst" in symptoms or "blurred vision" in symptoms:
        diabetes_score += 3
    
    if "diabetes" in family:
        diabetes_score += 2

    # Numerical metrics for Diabetes
    try:
        if data.sugar and float(data.sugar) > 120:
            diabetes_score += 5
        if data.bmi and float(data.bmi) > 25:
            diabetes_score += 2
    except: pass
        
    # 2. Scoring logic for Heart Disease
    heart_score = 0
    heart_keywords = ["smoke", "alcohol", "beer", "drink", "stress", "chest", "fat", "fried", "sit", "desk", "no exercise", "lazy"]
    for kw in heart_keywords:
        if kw in text:
            heart_score += 1
            
    if "chest pain" in symptoms or "palpitations" in symptoms or "breathlessness" in symptoms:
        heart_score += 3

    if "heart disease" in family:
        heart_score += 2
    
    try:
        if data.chol and float(data.chol) > 200:
            heart_score += 4
        if data.age and int(data.age) > 50:
            heart_score += 2
    except: pass

    # 3. Hypertension
    hyp_score = 0
    hyp_keywords = ["salt", "stress", "smoke", "alcohol", "obese", "sit", "desk", "lazy", "fast food"]
    for kw in hyp_keywords:
        if kw in text:
            hyp_score += 1
    if "headache" in symptoms or "dizziness" in symptoms or "fatigue" in symptoms:
        hyp_score += 3
    
    if "hypertension" in family:
        hyp_score += 2
        
    # 4. Liver Disease
    liver_score = 0
    liver_keywords = ["alcohol", "beer", "drink", "fat", "fried", "junk", "medicine"]
    for kw in liver_keywords:
        if kw in text:
            liver_score += 1
    if "nausea" in symptoms or "weight loss" in symptoms or "indigestion" in symptoms:
        liver_score += 3
    
    if "liver disease" in family:
        liver_score += 2

    # 5. Kidney Disease
    kidney_score = 0
    kidney_keywords = ["salt", "smoke", "diabetes", "blood pressure", "pain killer", "supplements"]
    for kw in kidney_keywords:
        if kw in text:
            kidney_score += 1
    if "frequent urination" in symptoms or "fatigue" in symptoms or "nausea" in symptoms:
        kidney_score += 3

    if "kidney disease" in family:
        kidney_score += 2

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
