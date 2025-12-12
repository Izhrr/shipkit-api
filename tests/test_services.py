import pytest
import respx
from httpx import Response
from services import parse_etd_to_float, parse_etd_to_tuple, call_komerce_calculate_acl
from fastapi import HTTPException
import httpx
from schemas import OpsiPengiriman, SortType

def test_parse_etd_to_float_basic():
    assert parse_etd_to_float("1 day") == 1.0
    assert parse_etd_to_float("2-3 day") == 2.0  # first number extracted
    assert parse_etd_to_float("") == float('inf')
    assert parse_etd_to_float(None) == float('inf')

def test_parse_etd_to_tuple_basic():
    assert parse_etd_to_tuple("1 day") == (1.0, 1.0)
    assert parse_etd_to_tuple("1-2 day") == (1.0, 2.0)
    assert parse_etd_to_tuple("") == (float('inf'), float('inf'))
    assert parse_etd_to_tuple("no digits here") == (float('inf'), float('inf'))

@pytest.mark.asyncio
async def test_call_komerce_calculate_acl_happy_path(monkeypatch):
    sample_response = {"data": [
        {
            "name": "JNE",
            "service": "REG",
            "cost": 15000,
            "code": "jne_reg",
            "description": "Regular",
            "etd": "2-3 day"
        }
    ]}
    url = "https://rajaongkir.komerce.id/api/v1/calculate/district/domestic-cost"
    with respx.mock:
        respx.post(url).mock(return_value=Response(200, json=sample_response))
        result = await call_komerce_calculate_acl("1391", "1376", 1000)
        assert isinstance(result, list)
        assert len(result) == 1
        opsi = result[0]
        assert isinstance(opsi, OpsiPengiriman)
        assert opsi.name == "JNE"
        assert opsi.cost == 15000

@pytest.mark.asyncio
async def test_call_komerce_calculate_acl_empty_data(monkeypatch):
    # Simulate 200 with empty data -> function should return []
    url = "https://rajaongkir.komerce.id/api/v1/calculate/district/domestic-cost"
    with respx.mock:
        respx.post(url).mock(return_value=Response(200, json={"data": []}))
        result = await call_komerce_calculate_acl("0", "0", 0)
        assert result == []

@pytest.mark.asyncio
async def test_call_komerce_calculate_acl_komerce_404():
    url = "https://rajaongkir.komerce.id/api/v1/calculate/district/domestic-cost"
    with respx.mock:
        respx.post(url).mock(return_value=Response(404, json={"error": "not found"}))
        with pytest.raises(HTTPException) as exc:
            await call_komerce_calculate_acl("1", "2", 100)
        assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_call_komerce_calculate_acl_internal_error(monkeypatch):
    async def fake_post(*args, **kwargs):
        raise RuntimeError("unexpected error")

    class FakeClient:
        async def __aenter__(self): return self
        async def __aexit__(self, *args): pass
        post = fake_post

    monkeypatch.setattr(httpx, "AsyncClient", lambda: FakeClient())

    with pytest.raises(HTTPException) as exc:
        await call_komerce_calculate_acl("1", "2", 100)

    assert exc.value.status_code == 500

def test_sort_shipping_options_by_harga():
    opsi = [
        OpsiPengiriman(name="A", cost=20000, etd="2-3 day", service="", code="", description=""),
        OpsiPengiriman(name="B", cost=10000, etd="1 day", service="", code="", description=""),
    ]
    from services import sort_shipping_options
    result = sort_shipping_options(opsi, SortType.HARGA_TERENDAH)
    assert result[0].name == "B"

def test_sort_shipping_options_by_waktu():
    opsi = [
        OpsiPengiriman(name="A", cost=20000, etd="3 day", service="", code="", description=""),
        OpsiPengiriman(name="B", cost=15000, etd="1 day", service="", code="", description=""),
    ]
    from services import sort_shipping_options
    result = sort_shipping_options(opsi, SortType.WAKTU_TERCEPAT)
    assert result[0].name == "B"

def test_sort_shipping_options_rekomendasi_utama():
    opsi = [
        OpsiPengiriman(name="A", cost=20000, etd="3 day", service="", code="", description=""),
        OpsiPengiriman(name="B", cost=10000, etd="1 day", service="", code="", description=""),
    ]
    from services import sort_shipping_options
    result = sort_shipping_options(opsi, SortType.REKOMENDASI_UTAMA)
    assert result[0].name == "B"
