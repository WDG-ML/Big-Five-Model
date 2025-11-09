# Big Five Model API

Ini adalah API layanan web (Flask) yang melayani model Machine Learning untuk memprediksi Tipe Kepribadian Big Five (Lima Besar) berdasarkan jawaban kuesioner.

Model ini memprediksi probabilitas untuk masing-masing dari lima sifat:

  * **AGR** (Agreeableness)
  * **CSN** (Conscientiousness)
  * **EST** (Extraversion)
  * **EXT** (Emotional Stability - *mewakili Neuroticism*)
  * **OPN** (Openness)

*(Catatan: Harap sesuaikan nama kelas di atas agar sesuai dengan definisi sebenarnya di `app.py` [AGR, CSN, EST, EXT, OPN])*.

## Fitur

  * Menyediakan endpoint `/predict` untuk prediksi real-time.
  * Menerima 50 input fitur (EXT1-10, EST1-10, AGR1-10, CSN1-10, OPN1-10) dalam format JSON.
  * Mengembalikan probabilitas JSON untuk setiap dari lima tipe kepribadian.
  * Siap untuk di-deploy menggunakan Docker.

## Persiapan dan Instalasi

### 1\. Clone Repositori

```bash
git clone https://github.com/WDG-ML/Big-Five-Model.git
cd Big-Five-Model
```

### 2\. Unduh Model (Penting\!)

File model `model.pkl` tidak disertakan dalam repositori ini (diabaikan oleh `.gitignore`). Anda harus mengunduhnya secara manual agar aplikasi dapat berjalan.

**Unduh `model.pkl` dari tautan berikut dan letakkan di direktori utama (root) proyek ini:**

[**➡️ Unduh model.pkl di sini**](https://drive.usercontent.google.com/download?id=1hUCs40oXeg1Fnz6CxEUebpmLWYH_AOjL&export=download&authuser=0)

Setelah diunduh, struktur direktori Anda akan terlihat seperti ini:

```
/Big-Five-Model
    |-- app.py
    |-- dockerfile
    |-- requirements.txt
    |-- model.pkl   <-- (File yang baru Anda unduh)
    |-- .gitignore
    |-- ... (file lainnya)
```

### 3\. Instal Dependensi

Sangat disarankan untuk menggunakan virtual environment:

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan (Windows)
.\venv\Scripts\activate
# Atau (macOS/Linux)
source venv/bin/activate

# Instal paket yang diperlukan
pip install -r requirements.txt
```

## Menjalankan Aplikasi

Anda dapat menjalankan server dengan dua cara:

### 1\. Lokal (Mode Pengembangan)

Pastikan Anda telah menginstal dependensi dan file `model.pkl` berada di folder yang benar.

```bash
# Jalankan aplikasi Flask
python app.py
```

Server akan berjalan di `http://0.0.0.0:5000/`.

### 2\. Menggunakan Docker

Cara ini direkomendasikan untuk deployment. Pastikan `model.pkl` ada di direktori sebelum membangun (build) image.

```bash
# 1. Bangun (build) Docker image
docker build -t big-five-api .

# 2. Jalankan (run) container
docker run -p 5000:5000 big-five-api
```

Server akan dapat diakses di `http://localhost:5000`.

## Penggunaan API

Kirim permintaan **POST** ke endpoint `/predict` dengan JSON body yang berisi 100 fitur jawaban.

**Endpoint:** `POST /predict`

### Contoh Request Body (JSON)

Anda harus menyediakan 100 kunci, dari `EXT1` hingga `OPN10`. Nilai yang tidak ada atau non-numerik akan diperlakukan sebagai 0.

```json
{
  "EXT1": 5,
  "EXT2": 1,
  "EXT3": 4,
  "EXT4": 2,
  "EXT5": 5,
  "EXT6": 1,
  "EXT7": 5,
  "EXT8": 2,
  "EXT9": 4,
  "EXT10": 1,
  "EST1": 3,
  "EST2": 2,
  "EST3": 4,
  "EST4": 2,
  "EST5": 3,
  "EST6": 2,
  "EST7": 3,
  "EST8": 2,
  "EST9": 3,
  "EST10": 3,
  "AGR1": 2,
  "AGR2": 5,
  "AGR3": 2,
  "AGR4": 4,
  "AGR5": 2,
  "AGR6": 4,
  "AGR7": 2,
  "AGR8": 4,
  "AGR9": 4,
  "AGR10": 3,
  "CSN1": 3,
  "CSN2": 2,
  "CSN3": 5,
  "CSN4": 2,
  "CSN5": 4,
  "CSN6": 1,
  "CSN7": 4,
  "CSN8": 2,
  "CSN9": 5,
  "CSN10": 5,
  "OPN1": 4,
  "OPN2": 1,
  "OPN3": 5,
  "OPN4": 1,
  "OPN5": 5,
  "OPN6": 1,
  "OPN7": 4,
  "OPN8": 3,
  "OPN9": 5,
  "OPN10": 5
}
```

### Contoh Respon Sukses (JSON)

Respon akan mengembalikan probabilitas yang diprediksi untuk setiap kelas.

```json
{
  "success": true,
  "probabilities": {
    "AGR": 0.0489,
    "CSN": 0.152,
    "EST": 0.1001,
    "EXT": 0.6501,
    "OPN": 0.0489
  }
}
```

## Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT.