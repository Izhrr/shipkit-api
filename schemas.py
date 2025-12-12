from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class SortType(str, Enum):
    HARGA_TERENDAH = "harga"
    WAKTU_TERCEPAT = "waktu"
    REKOMENDASI_UTAMA = "utama"

class OpsiPengiriman(BaseModel):
    name: str
    service: str
    cost: int
    code: Optional[str] = None
    description: Optional[str] = None
    etd: Optional[str] = ""

class PermintaanRekomendasi(BaseModel):
    origin_district_id: str = Field(..., example="1391")
    destination_district_id: str = Field(..., example="1376")
    weight_grams: int = Field(..., example=1000)

class PermintaanUrutkan(PermintaanRekomendasi):
    sort_by: SortType = Field(
        SortType.HARGA_TERENDAH,
        example="harga",
        description="Urutkan berdasarkan 'harga' (termurah) atau 'waktu' (tercepat)."
    )

class LoginRequest(BaseModel):
    username: str = Field(..., example="admin")
    password: str = Field(..., example="password123")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    username: Optional[str] = None