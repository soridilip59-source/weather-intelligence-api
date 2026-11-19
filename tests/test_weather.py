from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_homepage_serves_weather_dashboard():
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Weather Intelligence" in response.text
    assert 'id="search-form"' in response.text


@pytest.fixture(autouse=True)
def clear_history():
    from app.database import SessionLocal
    from app.models import WeatherSearch

    db = SessionLocal()
    db.query(WeatherSearch).delete()
    db.commit()
    db.close()
    yield


@patch("app.routes.weather.WeatherService")
def test_get_weather_success(mock_service):
    from app.schemas import WeatherResponse

    mock_service.return_value.get_weather = AsyncMock(
        return_value=WeatherResponse(
            city="Delhi",
            country="IN",
            temperature=28.5,
            feels_like=30.2,
            humidity=65,
            description="Clear Sky",
            wind_speed=3.5,
        )
    )

    response = client.get("/api/v1/weather", params={"city": "Delhi"})

    assert response.status_code == 200
    assert response.json()["city"] == "Delhi"
    assert response.json()["temperature"] == 28.5


def test_get_weather_rejects_short_city_name():
    response = client.get("/api/v1/weather", params={"city": "A"})
    assert response.status_code == 422
