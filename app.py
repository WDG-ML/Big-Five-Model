import joblib
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify

# -----------------------------------------------------------------
# Inisialisasi Aplikasi Flask
# -----------------------------------------------------------------
app = Flask(__name__)

# -----------------------------------------------------------------
# Muat Model & Variabel Global
# -----------------------------------------------------------------
# 1. Muat model .pkl yang sudah Anda latih
try:
    model = joblib.load("model.pkl")
    print("✅ Model berhasil dimuat.")
except FileNotFoundError:
    print("❌ Error: File 'model.pkl' tidak ditemukan.")
    model = None
except Exception as e:
    print(f"❌ Error saat memuat model: {e}")
    model = None

# Ini harus sama persis dengan urutan kolom 'X' saat Anda melatih model
traits = ['EXT', 'EST', 'AGR', 'CSN', 'OPN']
answer_cols = [f"{t}{i}" for t in traits for i in range(1, 11)]
FEATURE_COLS = answer_cols 
print(f"Model ini mengharapkan {len(FEATURE_COLS)} fitur.")


# 3. Definisikan nama kelas (dari le.classes_ di notebook Anda)
# Urutan ini HARUS sesuai dengan urutan di classification_report
# 0=AGR, 1=CSN, 2=EST, 3=EXT, 4=OPN
CLASS_NAMES = ['AGR', 'CSN', 'EST', 'EXT', 'OPN']
print(f"Nama kelas: {CLASS_NAMES}")

# -----------------------------------------------------------------
# Definisikan Rute API
# -----------------------------------------------------------------
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

    # 1. Ambil data JSON dari request
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Request JSON tidak valid."}), 400
    except Exception as e:
        return jsonify({"error": f"Gagal mem-parsing JSON: {e}"}), 400

    # 2. Ubah JSON menjadi DataFrame yang sesuai
    try:
        # Buat list berisi nilai-nilai fitur sesuai urutan FEATURE_COLS
        # data.get(col, 0) akan mengambil nilai (cth: data['EXT1'])
        # Jika tidak ada, gunakan 0 sebagai default (meniru .fillna(0) di notebook)
        feature_list = [data.get(col, 0) for col in FEATURE_COLS]
        
        # Buat DataFrame dari list tersebut
        # Model mengharapkan input 2D, jadi kita bungkus dengan list lagi
        input_df = pd.DataFrame([feature_list], columns=FEATURE_COLS)
        
        # Konversi ke numerik untuk keamanan (meniru .apply(pd.to_numeric))
        input_df = input_df.apply(pd.to_numeric, errors='coerce').fillna(0)

    except Exception as e:
        return jsonify({"error": f"Gagal memformat data: {e}. Pastikan JSON berisi 100 kunci fitur."}), 400

    # 3. Lakukan Prediksi
    try:
        # model.predict() mengembalikan array (cth: [2])
        prediction_index = model.predict(input_df)[0]
        
        # model.predict_proba() mengembalikan array probabilitas (cth: [[0.1, 0.2, 0.5, 0.1, 0.1]])
        probabilities_array = model.predict_proba(input_df)[0]
        
    except Exception as e:
        return jsonify({"error": f"Gagal melakukan prediksi: {e}"}), 500

    # 4. Format Hasil
    # Ambil nama kelas dari index prediksi
    prediction_name = CLASS_NAMES[prediction_index]
    
    # Buat dictionary untuk probabilitas
    probabilities = {CLASS_NAMES[i]: round(float(prob), 4) for i, prob in enumerate(probabilities_array)}

    # 5. Kembalikan hasil sebagai JSON
    return jsonify({
        "success": True,
        "probabilities": probabilities
    })

# -----------------------------------------------------------------
# Jalankan Server
# -----------------------------------------------------------------
if __name__ == '__main__':
    # host='0.0.0.0' agar bisa diakses dari luar localhost (jika diperlukan)
    app.run(host='0.0.0.0', port=5000, debug=True)