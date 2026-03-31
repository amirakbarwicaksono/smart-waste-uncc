# ----------- core/blockchain/payload_formatter.py -----------
"""
Format data untuk blockchain (mendukung simulator dan Motoko)
"""

import json
import hashlib
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List


class BlockchainPayloadFormatter:
    """Format data untuk blockchain"""
    
    @staticmethod
    def format_transaction(
        user_hash: str,
        user_id: Optional[str],
        waste_type: str,
        bin_type: str,
        weight_status: bool,
        timestamp: str,
        duration: float,
        transaction_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Format single transaction"""
        if not transaction_id:
            transaction_id = str(uuid.uuid4())
        
        return {
            "transaction_id": transaction_id,
            "timestamp": timestamp,
            "user": {
                "hash": user_hash,
                "display_name": user_id if user_id else user_hash[:16]
            },
            "waste": {
                "type": waste_type,
                "bin_type": bin_type
            },
            "verification": {
                "weight_detected": weight_status,
                "is_valid": weight_status
            },
            "metrics": {
                "duration_seconds": duration,
                "points_earned": 0  # Will be calculated by blockchain
            }
        }
    
    @staticmethod
    def format_batch(transactions: List[Dict], batch_id: Optional[str] = None) -> Dict:
        """Format batch of transactions"""
        if not batch_id:
            batch_id = str(uuid.uuid4())
        
        return {
            "batch_id": batch_id,
            "timestamp": datetime.now().isoformat(),
            "transaction_count": len(transactions),
            "transactions": transactions
        }


# Convenience functions
def format_transaction(**kwargs):
    return BlockchainPayloadFormatter.format_transaction(**kwargs)


def format_batch(transactions, batch_id=None):
    return BlockchainPayloadFormatter.format_batch(transactions, batch_id)