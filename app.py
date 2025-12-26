import requests
from flask import Flask, request, jsonify
from blockchain import Blockchain
from sheets import send_to_sheets

app = Flask(__name__)
blockchain = Blockchain()

#mencoba
@app.route("/add_data", methods=["POST"])
def add_data():
    data = request.json

    required_fields = [
        "student_id",
        "nama_mahasiswa",
        "mata_kuliah",
        "nilai",
        "semester",
        "dosen_pengampu"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    block = blockchain.add_block(data)
    send_to_sheets(block)

    return jsonify({
    "message": "Data berhasil ditambahkan ke blockchain & Google Sheets",
    "block": block
    })

@app.route("/reset_blockchain", methods=["POST"])
def reset_blockchain():
    blockchain.reset_chain()
    return jsonify({
        "status": "RESET SUCCESS",
        "message": "Blockchain berhasil di-reset ke genesis block"
    })

@app.route("/get_chain", methods=["GET"])
def get_chain():
    return jsonify({
        "length": len(blockchain.chain),
        "chain": blockchain.chain
    })

@app.route("/verify_chain", methods=["GET"])
def verify_chain():
    is_valid = blockchain.verify_chain()
    if is_valid:
        return jsonify({
            "status": "VALID",
            "message": "Blockchain aman dan tidak dimanipulasi"
        })
    else:
        return jsonify({
            "status": "INVALID",
            "message": "Blockchain telah dimanipulasi"
        })

@app.route("/detect_cloud_tampering", methods=["GET"])
def detect_cloud_tampering():
    GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwS5KkKUQhmdVqLmetZZjAg8sO_lqA2bqCJLPWgyQzCHOB0NYViMDkEAKV7sEKwJiOf/exec"

    response = requests.get(GOOGLE_SCRIPT_URL)

    try:
        cloud_data = response.json()
    except Exception:
        return jsonify({
            "status": "ERROR",
            "message": "Google Sheets tidak mengembalikan JSON"
        }), 500

    tampered = []

    for local_block in blockchain.chain[1:]:  # skip genesis
        match = next(
            (row for row in cloud_data if int(row["block_id"]) == local_block["block_id"]),
            None
        )

        if not match:
            tampered.append({
                "block_id": local_block["block_id"],
                "issue": "Data tidak ditemukan di cloud"
            })
            continue

        if match["nilai"] != local_block["nilai"]:
            tampered.append({
                "block_id": local_block["block_id"],
                "blockchain_nilai": local_block["nilai"],
                "cloud_nilai": match["nilai"]
            })

    if tampered:
        return jsonify({
            "status": "TAMPERING DETECTED",
            "details": tampered
        })

    return jsonify({
        "status": "SAFE",
        "message": "Tidak ada manipulasi data cloud"
    })

if __name__ == "__main__":
    app.run(debug=True)
