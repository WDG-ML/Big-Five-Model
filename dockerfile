# Gunakan base image Python 3.10 resmi yang ringan
FROM python:3.10-slim

# Tetapkan direktori kerja di dalam container
WORKDIR /app

# Salin file requirements.txt terlebih dahulu untuk caching layer
COPY requirements.txt .

# Instal pip terbaru dan semua dependensi dari requirements.txt
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# Salin sisa kode aplikasi (app.py) dan model (.pkl)
COPY . .

# Beri tahu Docker bahwa aplikasi akan berjalan di port 5000
EXPOSE 5000

# Perintah untuk menjalankan aplikasi saat container dimulai
CMD ["python", "app.py"]