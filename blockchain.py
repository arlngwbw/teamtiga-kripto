import hashlib
import json
from datetime import datetime

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        block = {
            "block_id": 0,
            "student_id": "GENESIS",
            "nama_mahasiswa": "-",
            "mata_kuliah": "-",
            "nilai": "-",
            "semester": "-",
            "tanggal": str(datetime.now()),
            "dosen_pengampu": "-",
            "prev_hash": "0"
        }
        block["current_hash"] = self.calculate_hash(block)
        self.chain.append(block)

    def reset_chain(self):
        self.chain = []
        self.create_genesis_block()

    def calculate_hash(self, block):
        block_copy = block.copy()
        block_copy.pop("current_hash", None)
        block_string = json.dumps(block_copy, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def add_block(self, data):
        last_block = self.chain[-1]

        block = {
            "block_id": len(self.chain),
            "student_id": data["student_id"],
            "nama_mahasiswa": data["nama_mahasiswa"],
            "mata_kuliah": data["mata_kuliah"],
            "nilai": data["nilai"],
            "semester": data["semester"],
            "tanggal": str(datetime.now()),
            "dosen_pengampu": data["dosen_pengampu"],
            "prev_hash": last_block["current_hash"]
        }

        block["current_hash"] = self.calculate_hash(block)
        self.chain.append(block)
        return block

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            recalculated_hash = self.calculate_hash(current)

            if current["current_hash"] != recalculated_hash:
                return False

            if current["prev_hash"] != previous["current_hash"]:
                return False

        return True
