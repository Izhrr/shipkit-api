import re
import httpx
from typing import List, Tuple
from fastapi import HTTPException
from config import KOMERCE_BASE_URL, KOMERCE_API_KEY
from schemas import OpsiPengiriman, SortType

# Helper parse ETD
def parse_etd_to_float(etd_str: str) -> float:
    """
    Helper untuk mengubah string ETD yang tidak konsisten menjadi angka float.
    (Bagian dari 'Logika Optimasi' Anda)
    """
    if not etd_str:
        return float('inf')
    match = re.search(r'(\d+)', etd_str)
    if match:
        return float(match.group(1))
    return float('inf')

def parse_etd_to_tuple(etd_str: str) -> Tuple[float, float]:
    """
    Helper untuk mengubah string ETD yang tidak konsisten menjadi
    tuple (min_hari, max_hari) agar bisa di-sort.
    - "1 day"   -> (1.0, 1.0)
    - "1-2 day" -> (1.0, 2.0)
    - "0-0 day" -> (0.0, 0.0)
    """
    if not etd_str:
        return (float('inf'), float('inf'))
    nums = re.findall(r'(\d+)', etd_str)
    
    if len(nums) == 0:
        # Null
        return (float('inf'), float('inf'))
    elif len(nums) == 1:
        # Kasus detail hari: "1 day" atau "2 day"
        val = float(nums[0])
        return (val, val)
    else:
        # Kasus rentang hari: "1-2 day" atau "0-0 day"
        min_val = float(nums[0])
        max_val = float(nums[1])
        return (min_val, max_val)

# ACL
async def call_komerce_calculate_acl(
    origin_id: str, 
    dest_id: str, 
    weight: int
) -> List[OpsiPengiriman]:
    """
    1. Memanggil 'TariffContext' (RajaOngkir).
    2. Menerjemahkan data mentah (raw) menjadi 'OpsiPengiriman'.
    """
    calculate_url = f"{KOMERCE_BASE_URL}/calculate/district/domestic-cost"
    headers = {
        'key': KOMERCE_API_KEY,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    courier_list = "jne:sicepat:ide:sap:jnt:ninja:tiki:lion:anteraja:pos:ncs:rex:rpx:sentral:star:wahana:dse"
    payload = {
        "origin": origin_id,
        "destination": dest_id,
        "weight": weight,
        "courier": courier_list
    }
    
    print(f"Memanggil Komerce Calculate (ACL) dengan data: {payload}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                calculate_url,
                headers=headers,
                data=payload
            )
            response.raise_for_status()
            
            raw_data = response.json().get("data")
            if not raw_data:
                print("Komerce Calculate berhasil, tapi data kurir kosong.")
                return []
            
            opsi_list = [OpsiPengiriman(**opsi) for opsi in raw_data]
            return opsi_list
    
    except httpx.HTTPStatusError as exc:
        print(f"Error Komerce Calculate: {exc.response.status_code} - {exc.response.text}")
        raise HTTPException(status_code=exc.response.status_code, detail=f"Error Komerce Calculate: {exc.response.text}")
    except Exception as e:
        print(f"Error internal di ACL: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error internal ACL: {str(e)}")

# Core domain
def sort_shipping_options(
    opsi_list: List[OpsiPengiriman], 
    sort_by: str
) -> List[OpsiPengiriman]:
    """
    Mengurutkan daftar kurir untuk optimasi pengiriman (Core Algorithm)
    """
    # sort by price
    if sort_by == SortType.HARGA_TERENDAH:
        print("Mengurutkan berdasarkan HARGA (termurah), lalu WAKTU...")
        sorted_list = sorted(
            opsi_list, 
            key=lambda opsi: (
                opsi.cost, 
                parse_etd_to_tuple(opsi.etd)[0], # min_hari
                parse_etd_to_tuple(opsi.etd)[1]  # max_hari
            )
        )
    else: # sort by time
        print("Mengurutkan berdasarkan WAKTU (tercepat), lalu HARGA...")
        # Urutkan berdasarkan min_hari, lalu max_hari, lalu harga (cost)
        sorted_list = sorted(
            opsi_list, 
            key=lambda opsi: (
                parse_etd_to_tuple(opsi.etd)[0], # min_hari
                parse_etd_to_tuple(opsi.etd)[1], # max_hari
                opsi.cost
            )
        )
    
    return sorted_list