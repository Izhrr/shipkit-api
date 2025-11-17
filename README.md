# Shipkit API — Layanan Optimasi Biaya Pengiriman (Ringkas)

Shipkit API adalah layanan backend Python (FastAPI) untuk menghitung dan mengoptimalkan biaya pengiriman pada skenario e‑commerce.

Prasyarat
- Python 3.10+
- pip, virtualenv/venv

Instalasi singkat
1. Clone:
   - git clone https://github.com/Izhrr/shipkit-api.git
   - cd shipkit-api
2. Virtual environment & install:
   - python -m venv .venv
   - source .venv/bin/activate  (Windows: .venv\Scripts\activate)
   - pip install --upgrade pip
   - pip install -r requirements.txt

Konfigurasi ENV (penting)
- Variabel yang wajib diset di environment (atau .env):
  - KOMERCE_API_KEY — API key untuk integrasi KOMERCE (wajib)

Menjalankan (FastAPI + Uvicorn)
- Jalankan server development/production menggunakan uvicorn:
  - uvicorn app.main:app --reload


NOTE
- Jangan commit credentials (.env) ke repository publik.

License
- MIT