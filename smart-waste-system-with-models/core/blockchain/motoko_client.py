
# ----------- core/blockchain/motoko_client.py -----------
def send_to_blockchain(timestamp, barcode, waste_type, bin_type):
    payload = {
        "timestamp": timestamp,
        "barcode_id": barcode,
        "waste_type": waste_type,
        "bin_type": bin_type
    }
    print("[BLOCKCHAIN STUB]", payload)

