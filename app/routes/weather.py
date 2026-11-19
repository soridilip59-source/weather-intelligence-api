from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import HistoryRecord, WeatherResponse
from app.services.history_service import HistoryService
from app.services.weather_service import WeatherService

router = APIRouter()


@router.get(
    "/weather",
    response_model=WeatherResponse,
    responses={404: {"model": dict}, 502: {"model": dict}, 503: {"model": dict}},
)
async def get_weather(
    city: str = Query(..., min_length=2, max_length=100),
    db: Session = Depends(get_db),
) -> WeatherResponse:
    city = city.strip()
    if not city:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="City name must not be empty.",
        )

    weather = await WeatherService().get_weather(city)
    HistoryService.create(db, weather)
    return weather


@router.get("/history", response_model=list[HistoryRecord])
def get_history(db: Session = Depends(get_db)) -> list[object]:
    return HistoryService.list(db)


@router.get("/history/{record_id}", response_model=HistoryRecord)
def get_history_record(
    record_id: int,
    db: Session = Depends(get_db),
) -> object:
    record = HistoryService.get(db, record_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"History record {record_id} was not found.",
        )
    return record


@router.delete("/history/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_history_record(
    record_id: int,
    db: Session = Depends(get_db),
) -> None:
    record = HistoryService.delete(db, record_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"History record {record_id} was not found.",
        )
    return None
