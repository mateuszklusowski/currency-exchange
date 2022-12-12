import datetime
import pytest
from app.main import check_api_call, get_currencies_mid

URL = "http://api.nbp.pl/api/exchangerates/rates/A/"
DATE = datetime.datetime(2022, 12, 12)


@pytest.mark.asyncio
async def test_call():
    response = await check_api_call(DATE, "USD")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_currencies_mid():
    result = await get_currencies_mid(DATE, "USD", "USD")
    assert type(result) == dict
    assert "USD" in result.keys()
    assert "date" in result.keys()
