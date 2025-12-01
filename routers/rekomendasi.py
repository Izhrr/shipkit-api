from fastapi import APIRouter, Depends
from typing import Any, List

import services
import schemas
from auth import verify_token

router = APIRouter(
    prefix="/api/v1",
    tags=["Rekomendasi (Core Domain)"]
)

# Recommendation Context
@router.post("/rekomendasi/urutkan", response_model=List[schemas.OpsiPengiriman])
async def get_sorted_recommendations(
    request: schemas.PermintaanUrutkan,
    current_user: dict = Depends(verify_token)
):
    """
    Recommendation Context: mengembalikan rekomendasi kurir berdasarkan "waktu" atau "harga", dilindungi JWT.
    """
    print(f"User '{current_user['username']}' mengakses endpoint rekomendasi...")
    print("Memulai proses Optimasi Pengiriman (Core Domain)...")
    
    # 1. Call ACL
    opsi_list = await services.call_komerce_calculate_acl(
        request. origin_district_id,
        request.destination_district_id,
        request.weight_grams
    )
    
    if not opsi_list:
        return []

    # 2.  Sorting
    final_list = services.sort_shipping_options(opsi_list, request.sort_by. value)
    return final_list


# TariffContext
@router.post("/estimasi-ongkir-distrik", response_model=List[schemas.OpsiPengiriman])
async def get_district_cost(
    request: schemas.PermintaanRekomendasi,
    current_user: dict = Depends(verify_token)
):
    """
    Tariff Context: mengembalikan daftar tarif mentah
    """
    opsi_list = await services.call_komerce_calculate_acl(
        request.origin_district_id,
        request.destination_district_id,
        request.weight_grams
    )
    print(f"User '{current_user['username']}' mengakses endpoint ongkir-distrik.")
    print("Sukses! Mengembalikan daftar kurir (TariffContext).")
    return opsi_list