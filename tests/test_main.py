import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(app=app, base_url="https://www.google.com/") as google:
        response = await google.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}


# @pytest
def test_passing():
    assert (1, 2, 3) == (1, 2, 3)


def test_passing_negative():
    assert (1, 2, 3) == (3, 2, 1)
