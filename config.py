import os
from dotenv import load_dotenv

load_dotenv()

KOMERCE_BASE_URL = "https://rajaongkir.komerce.id/api/v1"
KOMERCE_API_KEY = os.getenv("KOMERCE_API_KEY")

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret-key-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60

if not KOMERCE_API_KEY:
    print("PERINGATAN: 'KOMERCE_API_KEY' tidak di-set di .env")

if JWT_SECRET_KEY == "your-secret-key-change-this-in-production":
    print("PERINGATAN: 'JWT_SECRET_KEY' menggunakan nilai default.  Ganti di .env untuk production!")