from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WeatherResponse(BaseModel):
    city: str
    country: str
    temperature: float
    feels_like: float
    humidity: int
    description: str
    wind_speed: float


class HistoryRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city: str
    country: str
    temperature: float
    searched_at: datetime


class ErrorResponse(BaseModel):
    detail: str

