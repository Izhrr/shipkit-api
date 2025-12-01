from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import lokasi, rekomendasi, auth

app = FastAPI(
    title="ShipKit API",
    description="Layanan Optimasi Pengiriman E-commerce (Implementasi Core Domain) dengan JWT Authentication",
    version="1.0.0"
)

# Konfigurasi CORS (implement later)
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router
app.include_router(auth.router)       
app.include_router(lokasi.router)        
app.include_router(rekomendasi.router) 

@app.get("/")
def read_root():
    return {
        "message": "Selamat datang di ShipKit API (Core Domain: RecommendationContext)",
        "authentication": "JWT Token Required for protected endpoints",
        "login_endpoint": "/api/v1/login"
    }