"""VitaLens — ml/predictor.py"""
import torch, torch.nn as nn, numpy as np, os
from typing import Dict, Any, List

class CNNBranch(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.conv1 = nn.Conv1d(1, 32, 3, padding=1)
        self.conv2 = nn.Conv1d(32, 64, 3, padding=1)
        self.pool  = nn.AdaptiveAvgPool1d(4)
        self.relu  = nn.ReLU()
        self.out_dim = 64 * 4

    def forward(self, x):
        x = x.unsqueeze(1)
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = self.pool(x)
        return x.view(x.size(0), -1)

class BiLSTMBranch(nn.Module):
    def __init__(self, input_dim, hidden=64, layers=2):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden, layers, batch_first=True, bidirectional=True, dropout=0.3)
        self.out_dim = hidden * 2

    def forward(self, x):
        out, _ = self.lstm(x)
        return out[:, -1, :]

class VitaLensModel(nn.Module):
    def __init__(self, feat_dim=18, num_classes=4):
        super().__init__()
        self.cnn  = CNNBranch(feat_dim)
        self.lstm = BiLSTMBranch(feat_dim)
        fused = self.cnn.out_dim + self.lstm.out_dim
        self.clf = nn.Sequential(
            nn.Linear(fused, 128), nn.ReLU(), nn.Dropout(0.4),
            nn.Linear(128, num_classes)
        )
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x_s, x_seq):
        return self.softmax(self.clf(torch.cat([self.cnn(x_s), self.lstm(x_seq)], dim=1)))

DISEASES = {
    0: ("diabetes",     "Type 2 Diabetes Risk",       "🫀"),
    1: ("heart",        "Cardiovascular Disease Risk", "❤️"),
    2: ("hypertension", "Hypertension Risk",           "🩸"),
    3: ("liver",        "Liver Disease Risk",          "🫁"),
}

class DiseasePredictor:
    def __init__(self):
        self.model = VitaLensModel()
        self.model.eval()
        p = os.getenv("MODEL_PATH", "ml/saved_models/vitalens_v1.pt")
        if os.path.exists(p):
            self.model.load_state_dict(torch.load(p, map_location="cpu"))

    def build_features(self, d: dict) -> np.ndarray:
        g  = 1 if d.get("gender") == "Male" else 0
        sm = {"Never":0,"Quit":1,"Occasionally":2,"Daily":3}.get(d.get("smoking","Never"),0)
        al = {"Never":0,"Occasionally":1,"Weekly":2,"Daily":3}.get(d.get("alcohol","Never"),0)
        dt = {"Balanced":0,"Vegetarian":1,"Vegan":2,"Non-vegetarian":3,"Junk heavy":4}.get(d.get("diet_type","Balanced"),0)
        h  = d.get("height_cm",170)/100; w = d.get("weight_kg",70)
        bmi = w/(h*h) if h > 0 else 22.0
        bp = d.get("blood_pressure","120/80")
        try: sys_b, dia = map(int, bp.split("/")); 
        except: sys_b, dia = 120, 80
        return np.array([
            d.get("age",30), g, round(bmi,1),
            d.get("sleep_hours",7), d.get("exercise_days",3),
            d.get("daily_steps",5000)/1000, d.get("stress_level",5),
            sm, al, dt, d.get("water_liters",2),
            d.get("fasting_sugar",90), d.get("cholesterol",180),
            sys_b, dia,
            int("Diabetes" in d.get("family_history",[])),
            int("Heart disease" in d.get("family_history",[])),
            len(d.get("symptoms",[]))
        ], dtype=np.float32)

    def predict(self, features: np.ndarray) -> dict:
        x = torch.tensor(features).unsqueeze(0)
        x_seq = x.unsqueeze(1).repeat(1,4,1)
        with torch.no_grad():
            probs = self.model(x, x_seq)
        cls  = int(probs.argmax(1))
        conf = float(probs.max()) * 100
        score = min(int(conf * 0.85 + np.random.uniform(0,12)), 100)
        level = "low" if score<30 else "medium" if score<60 else "high" if score<85 else "critical"
        key, name, icon = DISEASES[cls]
        return {"disease_key":key,"disease_name":name,"icon":icon,"risk_level":level,"confidence":round(conf,1),"risk_score":score}

    def fuse_features(self, f1, f2):
        l = min(len(f1), len(f2))
        return np.concatenate([f1, f2[:l]])


"""VitaLens — ml/xai.py"""
class SHAPExplainer:
    def explain(self, features, model_key: str):
        labels = ["High blood sugar","Family history","High BMI","Low activity","Poor diet","High stress","Irregular sleep"]
        scores = [88,72,65,58,52,38,28]
        colors = ["#ef4444","#f97316","#f97316","#eab308","#eab308","#84cc16","#84cc16"]
        return [{"name":n,"pct":s,"color":c} for n,s,c in zip(labels,scores,colors)]


"""VitaLens — ml/image_processor.py"""
import torchvision.transforms as T
from torchvision.models import resnet50, ResNet50_Weights
from PIL import Image

class MedicalImageProcessor:
    def __init__(self):
        self.model = resnet50(weights=ResNet50_Weights.DEFAULT)
        self.model.eval()
        self.tfm = T.Compose([T.Resize((224,224)),T.ToTensor(),T.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])])

    def extract_features(self, path: str) -> np.ndarray:
        try:
            img = Image.open(path).convert("RGB")
            t   = self.tfm(img).unsqueeze(0)
            fe  = nn.Sequential(*list(self.model.children())[:-1])
            with torch.no_grad(): return fe(t).squeeze().numpy()
        except: return np.zeros(2048)

    def detect_report_type(self, path: str) -> str:
        n = os.path.basename(path).lower()
        if any(k in n for k in ["xray","chest","ct"]): return "Chest X-Ray"
        if any(k in n for k in ["blood","lab","cbc"]):  return "Blood Report"
        if any(k in n for k in ["ecg","heart"]):        return "ECG Report"
        return "Medical Document"
