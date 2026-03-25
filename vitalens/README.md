# VitaLens — Health Intelligence Platform

AI-powered lifestyle disease risk prediction with personalized hospital recommendations and blockchain-secured health records.

---

## Project Structure

```
vitalens/
├── frontend/          # React app (HTML/CSS/JS)
│   └── index.html     # Single-page application
├── backend/           # FastAPI Python backend
│   ├── main.py        # App entry point
│   ├── routes/        # API route handlers
│   │   ├── predict.py
│   │   ├── records.py
│   │   ├── hospitals.py
│   │   └── auth.py
│   ├── ml/            # Machine learning models
│   │   ├── predictor.py
│   │   ├── xai.py
│   │   └── image_processor.py
│   ├── blockchain/    # Ethereum integration
│   │   └── service.py
│   ├── services/      # Business logic
│   │   └── hospital_finder.py
│   ├── models/        # DB models
│   │   └── schemas.py
│   ├── database.py
│   ├── requirements.txt
│   └── .env.example
├── contracts/         # Solidity smart contracts
│   └── PatientRecord.sol
└── README.md
```

---

## How to Run

### Prerequisites
- Python 3.10+
- Node.js 18+ (optional, for React build)
- PostgreSQL (or use SQLite for local dev)
- MetaMask wallet (for blockchain features)

---

### Step 1 — Clone / Extract the project

```bash
cd vitalens
```

---

### Step 2 — Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### Step 3 — Configure Environment

```bash
cp .env.example .env
# Edit .env with your values (see .env.example)
```

---

### Step 4 — Run Backend

```bash
# From backend/ folder
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API will be live at: `http://localhost:8000`
Swagger docs at:    `http://localhost:8000/api/docs`

---

### Step 5 — Run Frontend

Simply open `frontend/index.html` in your browser.

Or serve it with Python:
```bash
cd frontend
python -m http.server 5500
# Open http://localhost:5500
```

---

### Step 6 — Deploy Smart Contract (Optional)

```bash
cd contracts
npm install -g hardhat
npx hardhat compile
npx hardhat run scripts/deploy.js --network sepolia
# Copy contract address to .env → CONTRACT_ADDRESS
```

---

## Hospital Recommendation

Hospitals are suggested dynamically based on the user's entered city/location.

- User enters city (e.g., Mumbai, Delhi, Bangalore, Hyderabad...)
- Backend matches city to hospital database
- Falls back to nearest major city if exact city not found
- Google Places API integration available for live results

Supported cities (built-in): Coimbatore, Chennai, Mumbai, Delhi, Bangalore, Hyderabad, Kolkata, Pune, Ahmedabad, Jaipur, Lucknow, Kochi, Surat, Nagpur, Visakhapatnam, Madurai, Trichy, Salem, Mysore, Chandigarh

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/predict/analyze | Predict disease from lifestyle data |
| POST | /api/predict/analyze-with-report | Predict + upload medical report |
| GET  | /api/hospitals/nearby?city=X&disease=Y | Get hospitals by city + disease |
| GET  | /api/records/{patient_id} | Get blockchain health records |
| POST | /api/auth/register | Register new user |
| POST | /api/auth/login | Login and get JWT token |

---

## Tech Stack (Internal Reference)

- Frontend: HTML5, CSS3, Vanilla JS (or React)
- Backend: FastAPI, Python 3.10+
- ML: PyTorch (CNN + BiLSTM), SHAP, scikit-learn
- Blockchain: Solidity, Web3.py, Ethereum Sepolia
- Database: PostgreSQL + SQLAlchemy
- Image: ResNet-50 (torchvision)
