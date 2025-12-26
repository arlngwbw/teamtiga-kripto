import requests

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzwsQsbX5ZaSvTdArivnIU6scE0KCMowLM41xv2DcNbpOgpwZaFZdmxgii_38S8JKc/exec"

def send_to_sheets(block):
    payload = {
        "block_id": block["block_id"],
        "student_id": block["student_id"],
        "nama_mahasiswa": block["nama_mahasiswa"],
        "mata_kuliah": block["mata_kuliah"],
        "nilai": block["nilai"],
        "semester": block["semester"],
        "dosen_pengampu": block["dosen_pengampu"],
        "current_hash": block["current_hash"]
    }

    response = requests.post(GOOGLE_SCRIPT_URL, json=payload)
    print("Sheets response:", response.text)