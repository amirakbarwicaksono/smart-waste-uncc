# ----------- core/blockchain/simulator.py -----------
"""
Simulasi blockchain untuk development.
Menyimpan transaksi ke file JSON seperti "ledger".
"""

import json
import hashlib
import time
import uuid
import threading
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Konfigurasi
BASE_DIR = Path(__file__).resolve().parent.parent.parent
LEDGER_FILE = BASE_DIR / "logs" / "blockchain_ledger.json"
BLOCKCHAIN_DIR = BASE_DIR / "logs" / "blockchain_blocks"

# Pastikan folder ada
LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)
BLOCKCHAIN_DIR.mkdir(parents=True, exist_ok=True)


class BlockchainSimulator:
    """
    Simulator blockchain untuk development.
    Menyimpan transaksi dan memverifikasi integritas data.
    """
    
    def __init__(self):
        self._lock = threading.Lock()
        self._initialize_ledger()
    
    def _initialize_ledger(self):
        """Initialize ledger file if not exists"""
        if not LEDGER_FILE.exists():
            initial_ledger = {
                "genesis": {
                    "timestamp": datetime.now().isoformat(),
                    "block_height": 0,
                    "previous_hash": "0" * 64,
                    "transactions": []
                },
                "transactions": [],
                "stats": {
                    "total_transactions": 0,
                    "total_users": 0,
                    "total_points_earned": 0.0
                },
                "users": {}
            }
            self._save_ledger(initial_ledger)
    
    def _save_ledger(self, ledger: Dict):
        """Save ledger to file"""
        with self._lock:
            with open(LEDGER_FILE, 'w') as f:
                json.dump(ledger, f, indent=2, default=str)
    
    def _load_ledger(self) -> Dict:
        """Load ledger from file"""
        with self._lock:
            if LEDGER_FILE.exists():
                with open(LEDGER_FILE, 'r') as f:
                    return json.load(f)
        return {"transactions": [], "stats": {}, "users": {}}
    
    def _calculate_hash(self, data: Dict) -> str:
        """Calculate SHA256 hash of transaction data"""
        data_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def add_transaction(
        self,
        user_hash: str,
        user_id: str,
        waste_type: str,
        bin_type: str,
        weight_status: bool,
        duration: float,
        transaction_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add transaction to blockchain ONLY if weight_status is True.
        Returns transaction record or None if not recorded.
        """
        
        # ⚠️ KRUSIAL: HANYA JIKA weight_status = True
        if not weight_status:
            logger.info(f"⏭️ Transaction NOT recorded to blockchain (weight_status=False)")
            return {
                "success": False,
                "recorded": False,
                "reason": "weight_status_false",
                "message": "Weight not detected - transaction not hashed to blockchain"
            }
        
        # ========================================
        # HANYA KODE DI BAWAH INI YANG DIJALANKAN
        # JIKA weight_status = True
        # ========================================
        
        if not transaction_id:
            transaction_id = str(uuid.uuid4())
        
        # Points hanya diberikan jika weight_status = True
        points = 0.5  # Fixed reward
        
        # Create transaction record
        transaction = {
            "transaction_id": transaction_id,
            "timestamp": datetime.now().isoformat(),
            "user": {
                "hash": user_hash,
                "display_name": user_id if user_id else user_hash[:16]
            },
            "waste": {
                "type": waste_type,
                "bin_type": bin_type
            },
            "verification": {
                "weight_detected": True,
                "is_valid": True
            },
            "metrics": {
                "duration_seconds": duration,
                "points_earned": points,
                "reward_reason": "weight_confirmed"
            },
            "hash": None
        }
        
        # Calculate hash
        transaction["hash"] = self._calculate_hash(transaction)
        
        # Load existing ledger
        ledger = self._load_ledger()
        
        # Add transaction
        ledger["transactions"].append(transaction)
        ledger["stats"]["total_transactions"] = len(ledger["transactions"])
        
        # Update user stats
        user_stats = self._get_user_stats(ledger, user_hash)
        user_stats["total_transactions"] = user_stats.get("total_transactions", 0) + 1
        user_stats["total_points"] = user_stats.get("total_points", 0) + points
        user_stats["last_active"] = datetime.now().isoformat()
        user_stats["display_name"] = user_id or user_hash[:16]
        
        ledger["users"] = ledger.get("users", {})
        ledger["users"][user_hash] = user_stats
        
        # Update total points
        ledger["stats"]["total_points_earned"] = ledger["stats"].get("total_points_earned", 0) + points
        ledger["stats"]["total_users"] = len(ledger["users"])
        
        # Save ledger
        self._save_ledger(ledger)
        
        logger.info(f"✅ Transaction recorded to blockchain: {transaction_id} (+{points} points)")
        
        return {
            "success": True,
            "recorded": True,
            "transaction": transaction,
            "points_earned": points,
            "message": f"Transaction hashed to blockchain! Earned {points} points"
        }
    
    def get_transaction(self, transaction_id: str) -> Optional[Dict]:
        """Get transaction by ID"""
        ledger = self._load_ledger()
        for tx in ledger.get("transactions", []):
            if tx.get("transaction_id") == transaction_id:
                return tx
        return None
    
    def get_user_transactions(self, user_hash: str, limit: int = 50) -> List[Dict]:
        """Get all transactions for a user"""
        ledger = self._load_ledger()
        transactions = [
            tx for tx in ledger.get("transactions", [])
            if tx.get("user", {}).get("hash") == user_hash
        ]
        # Return most recent first
        return sorted(transactions, key=lambda x: x.get("timestamp", ""), reverse=True)[:limit]
    
    def get_user_stats(self, user_hash: str) -> Dict:
        """Get user statistics"""
        ledger = self._load_ledger()
        return ledger.get("users", {}).get(user_hash, {
            "total_transactions": 0,
            "total_points": 0,
            "display_name": user_hash[:16],
            "last_active": None
        })
    
    def get_system_stats(self) -> Dict:
        """Get system-wide statistics"""
        ledger = self._load_ledger()
        return ledger.get("stats", {
            "total_transactions": 0,
            "total_users": 0,
            "total_points_earned": 0
        })
    
    def get_transaction_status(self, transaction_id: str) -> Dict:
        """Check if transaction exists in blockchain"""
        ledger = self._load_ledger()
        for tx in ledger.get("transactions", []):
            if tx.get("transaction_id") == transaction_id:
                return {
                    "exists": True,
                    "transaction": tx,
                    "blockchain_status": "hashed"
                }
        return {
            "exists": False,
            "blockchain_status": "not_hashed"
        }
    
    def get_user_blockchain_summary(self, user_hash: str) -> Dict:
        """
        Get summary of user's blockchain activity
        Returns total points and count of hashed transactions
        """
        ledger = self._load_ledger()
        user_stats = ledger.get("users", {}).get(user_hash, {})
        
        # Hitung hanya transaksi yang dihash (weight_status = True)
        user_transactions = [
            tx for tx in ledger.get("transactions", [])
            if tx.get("user", {}).get("hash") == user_hash
            and tx.get("verification", {}).get("weight_detected", False) == True
        ]
        
        return {
            "total_hashed_transactions": len(user_transactions),
            "total_points": user_stats.get("total_points", 0),
            "last_active": user_stats.get("last_active"),
            "display_name": user_stats.get("display_name", user_hash[:16])
        }
    
    def _get_user_stats(self, ledger: Dict, user_hash: str) -> Dict:
        """Helper to get user stats from ledger"""
        return ledger.get("users", {}).get(user_hash, {
            "total_transactions": 0,
            "total_points": 0,
            "last_active": None
        })
    
    def verify_integrity(self) -> bool:
        """Verify blockchain integrity by checking all hashes"""
        ledger = self._load_ledger()
        
        for tx in ledger.get("transactions", []):
            # Remove hash for verification
            stored_hash = tx.pop("hash", None)
            calculated_hash = self._calculate_hash(tx)
            tx["hash"] = stored_hash
            
            if stored_hash != calculated_hash:
                logger.error(f"Integrity check failed for transaction: {tx.get('transaction_id')}")
                return False
        
        logger.info("✅ Blockchain integrity verified")
        return True
    
    def export_ledger(self, filepath: Optional[Path] = None) -> str:
        """Export entire ledger to JSON file"""
        if not filepath:
            filepath = BLOCKCHAIN_DIR / f"ledger_export_{int(time.time())}.json"
        
        ledger = self._load_ledger()
        with open(filepath, 'w') as f:
            json.dump(ledger, f, indent=2, default=str)
        
        logger.info(f"✅ Ledger exported to: {filepath}")
        return str(filepath)


# Singleton instance
_simulator = None

def get_simulator() -> BlockchainSimulator:
    """Get singleton blockchain simulator instance"""
    global _simulator
    if _simulator is None:
        _simulator = BlockchainSimulator()
    return _simulator