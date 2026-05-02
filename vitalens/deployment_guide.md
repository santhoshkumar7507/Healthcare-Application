# 🚀 AuraHealth — Full-Stack Deployment Guide

This guide provides a comprehensive, step-by-step walkthrough to deploy **AuraHealth** from your local machine to the cloud.

---

## 1. Backend Deployment (FastAPI)
We recommend using **Render** for its seamless integration with Python and FastAPI.

### Steps:
1.  **Create a Render Account**: Sign up at [render.com](https://render.com).
2.  **New Web Service**: Click `New` -> `Web Service`.
3.  **Connect GitHub**: Connect the [Healthcare-Application](https://github.com/santhoshkumar7507/Healthcare-Application) repository.
4.  **Configure Service**:
    *   **Runtime**: `Python 3.10+`
    *   **Build Command**: `pip install -r backend/requirements.txt`
    *   **Start Command**: `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
    *   **Working Directory**: `backend`
5.  **Environment Variables**: Go to the `Environment` tab and add:
    *   `DATABASE_URL`: Your PostgreSQL URL (Render provides a free PostgreSQL database).
    *   `JWT_SECRET`: A long random string.
    *   `BLOCKCHAIN_RPC`: Your Infura/Alchemy Sepolia URL.
    *   `ALLOWED_ORIGINS`: Your eventual Frontend URL (e.g., `https://aurahealth.vercel.app`).

---

## 2. Smart Contract Deployment (Solidity)
Deploy your logic to the **Ethereum Sepolia Testnet** to ensure data immutability.

### Steps:
1.  **Get an RPC Key**: Create an account on [Alchemy](https://alchemy.com) and get a **Sepolia RPC URL**.
2.  **Get Test ETH**: Use a faucet like [sepoliafaucet.com](https://sepoliafaucet.com) to get free test Ether.
3.  **Configure Hardhat/Truffle**:
    *   Navigate to the `contracts/` directory.
    *   Ensure your `.env` contains your `PRIVATE_KEY` and `RPC_URL`.
4.  **Deploy**:
    ```bash
    npx hardhat run scripts/deploy.js --network sepolia
    ```
5.  **Save Address**: Copy the deployed contract address and update it in your backend's `.env` file.

---

## 3. Frontend Deployment (Static JS)
The frontend is built with vanilla JS and HTML, making it perfect for **Vercel** or **Netlify**.

### Steps:
1.  **Create a Vercel Account**: Sign up at [vercel.com](https://vercel.com).
2.  **New Project**: Select the `Healthcare-Application` repository.
3.  **Configure Project**:
    *   **Root Directory**: `frontend`
    *   **Build Command**: (Leave empty, as it's static)
    *   **Output Directory**: `.` (Current folder)
4.  **Update API URL**: 
    *   In `frontend/login.html` and `frontend/index.html`, ensure the `API_URL` points to your Render backend URL (e.g., `https://aurahealth-backend.onrender.com`).
5.  **Deploy**: Click `Deploy`.

---

## 4. Final Integration Check
1.  **CORS Settings**: Ensure your Backend's `ALLOWED_ORIGINS` includes your Vercel URL.
2.  **Blockchain Records**: Verify that the `CONTRACT_ADDRESS` in your backend matches the one you deployed to Sepolia.
3.  **Live Test**:
    *   Register a new user on the live Vercel URL.
    *   Perform a health assessment.
    *   Verify the transaction on [Sepolia Etherscan](https://sepolia.etherscan.io).

---

> [!TIP]
> **Production Security**: For a real production environment, replace the SQLite database in the backend with a managed PostgreSQL instance provided by Render.

> [!IMPORTANT]
> **API Keys**: Never commit your `.env` file or private keys to GitHub. Always use the deployment platform's Environment Variables dashboard.
