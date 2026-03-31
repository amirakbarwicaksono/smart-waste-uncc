# ----------- core/blockchain/motoko_client.py -----------
"""
Client untuk blockchain (menggunakan simulator untuk development)
"""

import logging
from typing import Dict, Any, Optional, List

from core.blockchain.simulator import get_simulator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BlockchainClient:
    """
    Blockchain client yang menggunakan simulator untuk development.
    Nanti bisa diganti dengan Motoko client sebenarnya.
    """
    
    def __init__(self):
        self.simulator = get_simulator()
        logger.info("BlockchainClient initialized (simulator mode)")
    
    def submit_transaction(
        self,
        user_hash: str,
        user_id: str,
        waste_type: str,
        bin_type: str,
        weight_status: bool,
        duration: float
    ) -> Dict[str, Any]:
        """
        Submit transaction to blockchain.
        ONLY weight_status = True will be recorded.
        """
        
        # Log untuk debugging
        logger.info(f"📤 Submitting to blockchain: weight_status={weight_status}")
        
        # Panggil simulator (sudah handle filter weight_status)
        result = self.simulator.add_transaction(
            user_hash=user_hash,
            user_id=user_id,
            waste_type=waste_type,
            bin_type=bin_type,
            weight_status=weight_status,
            duration=duration
        )
        
        if result.get("recorded"):
            logger.info(f"✅ Blockchain recorded: {result['transaction']['transaction_id']}")
            logger.info(f"   Points: {result['points_earned']}")
        else:
            logger.info(f"⏭️ Blockchain skipped: {result.get('reason')}")
        
        return result
    
    def get_user_history(self, user_hash: str, limit: int = 50) -> List[Dict]:
        """Get user transaction history"""
        return self.simulator.get_user_transactions(user_hash, limit)
    
    def get_user_stats(self, user_hash: str) -> Dict[str, Any]:
        """Get user statistics"""
        stats = self.simulator.get_user_stats(user_hash)
        return {
            "success": True,
            "stats": stats
        }
    
    def get_user_blockchain_summary(self, user_hash: str) -> Dict[str, Any]:
        """Get user blockchain summary (only hashed transactions)"""
        summary = self.simulator.get_user_blockchain_summary(user_hash)
        return {
            "success": True,
            "summary": summary
        }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system-wide statistics"""
        stats = self.simulator.get_system_stats()
        return {
            "success": True,
            "stats": stats
        }
    
    def verify_integrity(self) -> bool:
        """Verify blockchain integrity"""
        return self.simulator.verify_integrity()


# Singleton client
_client = None

def get_client() -> BlockchainClient:
    """Get singleton blockchain client"""
    global _client
    if _client is None:
        _client = BlockchainClient()
    return _client


def submit_to_blockchain(
    user_hash: str,
    user_id: str,
    waste_type: str,
    bin_type: str,
    weight_status: bool,
    duration: float
) -> Dict:
    """Submit transaction to blockchain (convenience function)"""
    client = get_client()
    return client.submit_transaction(
        user_hash=user_hash,
        user_id=user_id,
        waste_type=waste_type,
        bin_type=bin_type,
        weight_status=weight_status,
        duration=duration
    )