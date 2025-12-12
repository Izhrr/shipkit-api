import pytest
from httpx import Response
import respx
from fastapi.testclient import TestClient
from main import app
from auth import create_access_token
import services

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "message" in r.json()

def test_lokasi_get_provinces_happy(monkeypatch):
    url = "https://rajaongkir.komerce.id/api/v1/destination/province"
    sample = {"data": [{"id": 1, "name": "Jawa Barat"}]}
    with respx.mock:
        respx.get(url).mock(return_value=Response(200, json=sample))
        r = client.get("/api/v1/provinsi")
        assert r.status_code == 200
        assert isinstance(r.json(), list)
        assert r.json()[0]["name"] == "Jawa Barat"

def test_lokasi_get_provinces_komerce_404():
    url = "https://rajaongkir.komerce.id/api/v1/destination/province"
    with respx.mock:
        respx.get(url).mock(return_value=Response(404, json={"message": "Not found"}))
        r = client.get("/api/v1/provinsi")
        assert r.status_code == 404

def test_lokasi_get_provinces_komerce_500():
    url = "https://rajaongkir.komerce.id/api/v1/destination/province"
    with respx.mock:
        respx.get(url).mock(return_value=Response(500, json={"error": "server error"}))
        r = client.get("/api/v1/provinsi")
        assert r.status_code == 500

def test_lokasi_get_provinces_not_found(monkeypatch):
    url = "https://rajaongkir.komerce.id/api/v1/destination/province"
    with respx.mock:
        respx.get(url).mock(return_value=Response(200, json={"data": []}))
        r = client.get("/api/v1/provinsi")
        assert r.status_code == 404

def test_lokasi_get_cities_happy():
    url = "https://rajaongkir.komerce.id/api/v1/destination/city/1"
    with respx.mock:
        respx.get(url).mock(return_value=Response(200, json={"data": [{"id": 10, "name": "Bandung"}]}))
        r = client.get("/api/v1/kota/1")
        assert r.status_code == 200

def test_lokasi_get_cities_not_found():
    url = "https://rajaongkir.komerce.id/api/v1/destination/city/1"
    with respx.mock:
        respx.get(url).mock(return_value=Response(200, json={"data": []}))
        r = client.get("/api/v1/kota/1")
        assert r.status_code == 404

def test_lokasi_get_cities_komerce_500():
    url = "https://rajaongkir.komerce.id/api/v1/destination/city/1"
    with respx.mock:
        respx.get(url).mock(return_value=Response(500, json={"error": "server error"}))
        r = client.get("/api/v1/kota/1")
        assert r.status_code == 500

def test_lokasi_get_districts_happy():
    url = "https://rajaongkir.komerce.id/api/v1/destination/district/100"
    with respx.mock:
        respx.get(url).mock(return_value=Response(200, json={"data": [{"id": 1000, "name": "Sukasari"}]}))
        r = client.get("/api/v1/distrik/100")
        assert r.status_code == 200

def test_lokasi_get_districts_not_found():
    url = "https://rajaongkir.komerce.id/api/v1/destination/district/100"
    with respx.mock:
        respx.get(url).mock(return_value=Response(200, json={"data": []}))
        r = client.get("/api/v1/distrik/100")
        assert r.status_code == 404

def test_lokasi_get_districts_komerce_500():
    url = "https://rajaongkir.komerce.id/api/v1/destination/district/100"
    with respx.mock:
        respx.get(url).mock(return_value=Response(500, json={"error": "server error"}))
        r = client.get("/api/v1/distrik/100")
        assert r.status_code == 500


def test_estimasi_ongkir_empty(monkeypatch):
    async def fake_call(_, __, ___):
        return []
    monkeypatch.setattr(services, "call_komerce_calculate_acl", fake_call)

    token = create_access_token({"sub": "admin"})
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "origin_district_id": "1",
        "destination_district_id": "2",
        "weight_grams": 500,
    }

    r = client.post("/api/v1/estimasi-ongkir-distrik", json=payload, headers=headers)
    assert r.status_code == 200
    assert r.json() == []


def test_rekomendasi_protected_and_happy(monkeypatch):
    # Mock services.call_komerce_calculate_acl to return sample opsi
    sample_opsi = [
        {
            "name": "A",
            "service": "S",
            "cost": 10000,
            "code": "a_s",
            "description": "desc",
            "etd": "1 day"
        },
        {
            "name": "B",
            "service": "S",
            "cost": 5000,
            "code": "b_s",
            "description": "desc",
            "etd": "2-3 day"
        }
    ]
    async def fake_call(origin, dest, weight):
        from schemas import OpsiPengiriman
        return [OpsiPengiriman(**o) for o in sample_opsi]

    monkeypatch.setattr(services, "call_komerce_calculate_acl", fake_call)

    token = create_access_token({"sub": "admin"})
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "origin_district_id": "1391",
        "destination_district_id": "1376",
        "weight_grams": 1000,
        "sort_by": "harga"
    }
    r = client.post("/api/v1/rekomendasi/urutkan", json=payload, headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)