import joblib
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

try:
    model = joblib.load("model.pkl")
    print("✅ Model berhasil dimuat.")
except FileNotFoundError:
    print("❌ Error: File 'model.pkl' tidak ditemukan.")
    model = None
except Exception as e:
    print(f"❌ Error saat memuat model: {e}")
    model = None

traits = ['EXT', 'EST', 'AGR', 'CSN', 'OPN']
answer_cols = [f"{t}{i}" for t in traits for i in range(1, 11)]
FEATURE_COLS = answer_cols 
print(f"Model ini mengharapkan {len(FEATURE_COLS)} fitur.")


CLASS_NAMES = ['AGR', 'CSN', 'EST', 'EXT', 'OPN']
print(f"Nama kelas: {CLASS_NAMES}")

@app.route('/')
def home():
    return "Server Model Big Five Aktif. Gunakan endpoint /predict untuk prediksi."

@app.route('/predict', methods=['POST'])
def predict():
    """
    Menerima data JSON, melakukan prediksi, dan mengembalikan hasil.
    """
    if not model:
        return jsonify({"error": "Model tidak dimuat. Periksa log server."}), 500

    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Request JSON tidak valid."}), 400
    except Exception as e:
        return jsonify({"error": f"Gagal mem-parsing JSON: {e}"}), 400

    try:
        feature_list = [data.get(col, 0) for col in FEATURE_COLS]
        
        input_df = pd.DataFrame([feature_list], columns=FEATURE_COLS)
        
        input_df = input_df.apply(pd.to_numeric, errors='coerce').fillna(0)

    except Exception as e:
        return jsonify({"error": f"Gagal memformat data: {e}. Pastikan JSON berisi 100 kunci fitur."}), 400

    try:
        probabilities_array = model.predict_proba(input_df)[0]
        
    except Exception as e:
        return jsonify({"error": f"Gagal melakukan prediksi: {e}"}), 500

    probabilities = {CLASS_NAMES[i]: round(float(prob), 4) for i, prob in enumerate(probabilities_array)}

    return jsonify({
        "success": True,
        "probabilities": probabilities
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)