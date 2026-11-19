import os

import httpx
from fastapi import HTTPException, status

from app.schemas import WeatherResponse

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherService:
    def __init__(self, api_key: str | None = None, timeout: float | None = None):
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        self.timeout = timeout or float(os.getenv("OPENWEATHER_TIMEOUT_SECONDS", "10"))

    async def get_weather(self, city: str) -> WeatherResponse:
        if not self.api_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Weather service is not configured. Set OPENWEATHER_API_KEY.",
            )

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    OPENWEATHER_URL,
                    params={"q": city, "appid": self.api_key, "units": "metric"},
                )
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Weather service request timed out.",
            )
        except httpx.HTTPError:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Could not connect to the weather service.",
            )

        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"City '{city}' was not found.",
            )
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Weather service rejected the configured API key.",
            )
        if response.status_code >= 400:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Weather service returned an unexpected error.",
            )

        try:
            payload = response.json()
            return WeatherResponse(
                city=payload["name"],
                country=payload["sys"]["country"],
                temperature=payload["main"]["temp"],
                feels_like=payload["main"]["feels_like"],
                humidity=payload["main"]["humidity"],
                description=payload["weather"][0]["description"].title(),
                wind_speed=payload["wind"]["speed"],
            )
        except (KeyError, IndexError, TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Weather service returned invalid data.",
            )

