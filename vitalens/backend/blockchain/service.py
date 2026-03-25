"""VitaLens — blockchain/service.py"""
import hashlib, datetime, os
from web3 import Web3

ABI = [{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_disease","type":"string"},{"internalType":"uint256","name":"_score","type":"uint256"},{"internalType":"string","name":"_city","type":"string"},{"internalType":"bytes32","name":"_hash","type":"bytes32"}],"name":"recordDiagnosis","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_name","type":"string"}],"name":"getRecords","outputs":[{"internalType":"string[]","name":"","type":"string[]"}],"stateMutability":"view","type":"function"}]

class BlockchainService:
    def __init__(self):
        rpc = os.getenv("BLOCKCHAIN_RPC","https://sepolia.infura.io/v3/YOUR_KEY")
        self.w3 = Web3(Web3.HTTPProvider(rpc))
        addr = os.getenv("CONTRACT_ADDRESS","0x0000000000000000000000000000000000000000")
        self.contract = self.w3.eth.contract(address=Web3.to_checksum_address(addr), abi=ABI)
        self.account = os.getenv("WALLET_ADDRESS","")
        self.pk = os.getenv("WALLET_PRIVATE_KEY","")

    def record_prediction(self, name, disease, score, city) -> str:
        if not self.w3.is_connected():
            raw = f"{name}{disease}{score}{city}{datetime.datetime.utcnow().isoformat()}"
            return "0x" + hashlib.sha256(raw.encode()).hexdigest()[:40]
        data_hash = Web3.keccak(text=f"{name}|{disease}|{score}|{city}")
        nonce = self.w3.eth.get_transaction_count(self.account)
        txn = self.contract.functions.recordDiagnosis(name,disease,score,city,data_hash).build_transaction({"chainId":11155111,"gas":200000,"gasPrice":self.w3.to_wei("20","gwei"),"nonce":nonce})
        signed = self.w3.eth.account.sign_transaction(txn, self.pk)
        tx = self.w3.eth.send_raw_transaction(signed.rawTransaction)
        return tx.hex()

    def get_patient_records(self, name: str) -> list:
        if not self.w3.is_connected(): return []
        return self.contract.functions.getRecords(name).call()
