# ShipKit API — Quick Start & Setup

Project singkat: backend FastAPI untuk optimasi biaya pengiriman (core domain: recommendation + tariff context). README ini to-the-point untuk initial setup, menjalankan lokal, testing, Docker, dan cara akses API yang sudah dideploy.

DEMO (deployed)
- Swagger / docs: https://shipkit-api-production.up.railway.app/docs

Ringkasan singkat
- Bahasa: Python 3.10+
- Framework: FastAPI
- Test: pytest (+ pytest-asyncio, respx), coverage enforced >= 95%
- Docker: Dockerfile (multi-stage) sudah disediakan
- CI: GitHub Actions workflow di `.github/workflows/ci.yml`

Struktur repository (penting)
- main.py — entrypoint FastAPI
- auth.py — autentikasi JWT, helper token
- config.py — env config (KOMERCE_API_KEY, JWT_SECRET_KEY, ...)
- services.py — logika optimasi & pemanggilan Komerce
- schemas.py — pydantic models
- routers/
  - auth.py
  - lokasi.py
  - rekomendasi.py
- tests/ — unit tests (pytest)
- Dockerfile — multi-stage Dockerfile
- .github/workflows/ci.yml — CI pipeline

Prasyarat (singkat)
- Python 3.10+
- pip
- (opsional) Docker (jika ingin build/run container)
- (opsional) gh (GitHub CLI) untuk menjalankan workflow dari CLI

Environment variables (yang WAJIB/sering dipakai)
- JWT_SECRET_KEY — kunci JWT (contoh dev: `test-secret-key`)
- KOMERCE_API_KEY — API key Komerce (opsional untuk integrasi nyata; tests menggunakan mocking)
CATATAN: Jangan commit .env ke repo. Tambahkan secrets di GitHub → Settings → Secrets and variables → Actions.

Quick local setup
1. Clone:
   git clone https://github.com/Izhrr/shipkit-api.git
   cd shipkit-api

2. Buat virtualenv & aktifkan:
   python -m venv .venv
   source .venv/bin/activate    # Linux/macOS
   .venv\Scripts\activate     # Windows

3. Install dependencies:
   pip install --upgrade pip
   pip install -r requirements.txt

Menjalankan aplikasi lokal
- Jalankan:
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
- Buka:
  http://localhost:8000/docs  (Swagger UI)

API penting & contoh cepat:
- POST /api/v1/login
  - Body:
    {
      "username": "admin",
      "password": "admin123"
    }
  - Default test creds tersedia:
    - admin / admin123
    - user / user123
  - Response: access_token (Bearer)

- POST /api/v1/rekomendasi/urutkan (protected)
  - Header: Authorization: Bearer <token>
  - Body contoh:
    {
      "origin_district_id": "1391",
      "destination_district_id": "1376",
      "weight_grams": 1000,
      "sort_by": "harga"
    }

- POST /api/v1/estimasi-ongkir-distrik (protected)
  - Sama format request tanpa sort_by; mengembalikan daftar opsi mentah

Testing (TDD) — bagaimana penguji harus jalanin
1. Pastikan dev deps terinstall (lihat di atas)
2. Jalankan tests:
   pytest -q
3. Coverage:
   pytest --cov=./ --cov-report=term-missing --cov-report=xml
   Catatan: pytest.ini di repo sudah mengatur `--cov-fail-under=95` sehingga CI akan gagal bila coverage <95%.
4. Mocking eksternal:
   - Tests memmock semua panggilan httpx ke Komerce menggunakan `respx`. Jangan jalankan tests yang memanggil API publik nyata.

CI (singkat)
- File workflow: `.github/workflows/ci.yml`
- Apa yang dilakukan: lint (ruff), install deps, run pytest (coverage enforced), build Docker (on push to main).
- Manual trigger: Actions → pilih workflow → Run workflow (workflow_dispatch supported).

Docker — build & run (singkat & aman)
- Dockerfile multi-stage sudah ada di repo.
- Build lokal:
  docker build -t shipkit-api:local .
- Jalankan (gunakan .env, jangan commit .env):
  docker run --rm -p 8000:8000 --env-file .env shipkit-api:local
- Dev (reload dengan mount):
  docker run --rm -p 8000:8000 -v "$(pwd)":/app --env-file .env shipkit-api:local uvicorn main:app --reload --host 0.0.0.0 --port 8000
- Push ke registry:
  - GHCR direkomendasikan: tag ghcr.io/<owner>/<repo>:<tag> lalu push (CI workflow dapat push menggunakan GITHUB_TOKEN).
  - Untuk Docker Hub, siapkan DOCKERHUB_USERNAME & DOCKERHUB_TOKEN secrets.

Notes & best-practices (singkat)
- Tests harus mocking semua external calls — CI juga mengharapkan itu.
- Jangan commit .env / credentials. Gunakan GitHub Secrets untuk CI.
- Health/Smoke: akses `/` atau `/docs` untuk memastikan service running.
