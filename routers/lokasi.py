import httpx
from fastapi import APIRouter, HTTPException
from typing import List
from config import KOMERCE_BASE_URL, KOMERCE_API_KEY

router = APIRouter(
    prefix="/api/v1",
    tags=["Lokasi (TariffContext)"]
)

# Endpoint 1: Daftar Provinsi
@router.get("/provinsi", response_model=List[dict])
async def get_all_provinces():
    endpoint_url = f"{KOMERCE_BASE_URL}/destination/province"
    headers = {'key': KOMERCE_API_KEY}
    
    print("Memanggil Komerce API: Get Provinsi...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint_url, headers=headers)
            response.raise_for_status()
            data = response.json().get("data")
            if not data:
                raise HTTPException(status_code=404, detail="Data provinsi tidak ditemukan")
            return data
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Data provinsi tidak ditemukan")
        raise HTTPException(status_code=exc.response.status_code, detail="Error Komerce API")

# Endpoint 2: Daftar Kota (by Provinsi)
@router.get("/kota/{province_id}", response_model=List[dict])
async def get_cities_by_province(province_id: int):
    endpoint_url = f"{KOMERCE_BASE_URL}/destination/city/{province_id}"
    headers = {'key': KOMERCE_API_KEY}
    
    print(f"Memanggil Komerce API: Get Kota untuk Provinsi ID: {province_id}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint_url, headers=headers)
            response.raise_for_status()
            data = response.json().get("data")
            if not data:
                raise HTTPException(status_code=404, detail="Data kota tidak ditemukan")
            return data
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Data kota tidak ditemukan")
        raise HTTPException(status_code=exc.response.status_code, detail="Error Komerce API")

# Endpoint 3: Daftar Distrik (by Kota)
@router.get("/distrik/{city_id}", response_model=List[dict])
async def get_districts_by_city(city_id: int):
    endpoint_url = f"{KOMERCE_BASE_URL}/destination/district/{city_id}"
    headers = {'key': KOMERCE_API_KEY}
    
    print(f"Memanggil Komerce API: Get Distrik untuk Kota ID: {city_id}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint_url, headers=headers)
            response.raise_for_status()
            data = response.json().get("data")
            if not data:
                raise HTTPException(status_code=404, detail="Data distrik tidak ditemukan")
            return data
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Data distrik tidak ditemukan")
        raise HTTPException(status_code=exc.response.status_code, detail="Error Komerce API")