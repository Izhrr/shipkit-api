import os
from dotenv import load_dotenv

load_dotenv()

KOMERCE_BASE_URL = "https://rajaongkir.komerce.id/api/v1"
KOMERCE_API_KEY = os.getenv("KOMERCE_API_KEY")

if not KOMERCE_API_KEY:
    print("PERINGATAN: 'KOMERCE_API_KEY' tidak di-set di .env")