# Shipkit API — Layanan Optimasi Biaya Pengiriman

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
  - JWT_SECRET_KEY - Key untuk JWT (wajib)

Menjalankan (FastAPI + Uvicorn)
- Jalankan server development/production menggunakan uvicorn:
  - uvicorn app.main:app --reload


NOTE
- Jangan commit credentials (.env) ke repository publik.

License
- MIT

# Shipkit API — Layanan Optimasi Biaya Pengiriman

[![CI](https://github.com/Izhrr/shipkit-api/actions/workflows/ci.yml/badge.svg)](https://github.com/Izhrr/shipkit-api/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/Izhrr/shipkit-api/branch/main/graph/badge.svg)](https://codecov.io/gh/Izhrr/shipkit-api)

Ringkasan:  
Shipkit API adalah backend Python (FastAPI) untuk menghitung dan mengoptimalkan biaya pengiriman pada skenario e‑commerce. README ini diperluas sehingga penguji/kontributor tahu cara menjalankan aplikasi, menjalankan unit tests (TDD), dan memicu/memverifikasi CI.

Checklist status:
- [ ] CI: Linting & Tests (GitHub Actions)
- [ ] Coverage >= 95%
- [ ] Docker image build (GHCR) — optional
- [ ] Service runs di Docker & melewati health checks

Prasyarat
- Python 3.10+
- pip
- (Opsional untuk CLI) GitHub CLI (gh)
- Docker (opsional jika ingin build/run image)

Struktur repo singkat
- main.py — FastAPI app entrypoint
- auth.py — JWT auth helpers
- config.py — konfigurasi env + var
- services.py — logika optimalisasi / wrapper Komerce
- schemas.py — pydantic models
- routers/ — routers untuk auth, lokasi, rekomendasi
- tests/ — kumpulan unit tests (pytest)
- .github/workflows/ci.yml — workflow CI
- requirements.txt
- requirements-dev.txt (dev dependencies; pytest, respx, dll)

Instalasi & menjalankan lokal
1. Clone repo:
   git clone https://github.com/Izhrr/shipkit-api.git
   cd shipkit-api

2. Virtual environment:
   python -m venv .venv
   source .venv/bin/activate         # Linux/Mac
   # .venv\Scripts\activate          # Windows

3. Install dependencies:
   pip install --upgrade pip
   pip install -r requirements.txt


4. Menjalankan server (development):
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   Akses: http://localhost:8000
   Dokumentasi interaktif: http://localhost:8000/docs

Environment variables (secrets)
Jangan commit .env ke repo. Tambahkan secrets di GitHub Settings → Secrets and variables → Actions.

Minimal variables yang dibutuhkan:
- JWT_SECRET_KEY — kunci untuk membuat dan mem-verifikasi JWT (contoh: test-secret-key)
- KOMERCE_API_KEY — (opsional) API key Komerce untuk ambil data dari API RajaOngkir

Gunakan .env untuk dev lokal (contoh .env):
KOMERCE_API_KEY=your_komerce_api_key_here
JWT_SECRET_KEY=your_jwt_secret_here

Menjalankan tests (panduan lengkap untuk penguji)
Testing di sini berprinsip TDD: unit tests lengkap, mocking panggilan eksternal, coverage >= 95%.

1. Pastikan dev deps terinstal:
   pip install -r requirements.txt

2. Struktur tests:
   - tests/conftest.py — fixture TestClient & env deterministic
   - tests/test_services.py — parsing ETD + mocking call_komerce_calculate_acl
   - tests/test_auth.py — authenticate_user, create_access_token, login endpoint
   - tests/test_routers.py — routers: lokasi, rekomendasi (melalui TestClient)

3. Menjalankan tests lokal:
   pytest -q

CI (GitHub Actions) — cara menjalankan & memeriksa
Workflow utama: .github/workflows/ci.yml — melakukan:
- checkout
- setup python 3.10
- install requirements + dev deps
- lint (ruff)
- run pytest (coverage enforced)
- upload artifact coverage.xml
- build & push Docker image ke GHCR (opsional, hanya pada push to main)

Menjalankan workflow manual (workflow_dispatch)
1. Buka repo → tab Actions → pilih workflow CI
2. Klik “Run workflow”.
3. Pilih branch (biasanya main) → Run workflow.
4. Buka run → lihat job “Lint & Test” → expand steps → periksa output pytest.
5. Artifact coverage: di halaman run ada link Artifacts → download coverage-report.

Melihat logs via CLI (opsional)
- Pastikan gh CLI terinstal & login.
- Jalankan workflow:
  gh workflow run ci.yml --ref main
- Cek run list:
  gh run list
- Lihat logs:
  gh run view <run-id> --log

Kontributor & Lisensi
- License: MIT
