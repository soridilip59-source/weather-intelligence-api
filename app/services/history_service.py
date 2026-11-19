from sqlalchemy.orm import Session

from app.models import WeatherSearch
from app.schemas import WeatherResponse


class HistoryService:
    @staticmethod
    def create(db: Session, weather: WeatherResponse) -> WeatherSearch:
        record = WeatherSearch(
            city=weather.city,
            country=weather.country,
            temperature=weather.temperature,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def list(db: Session) -> list[WeatherSearch]:
        return db.query(WeatherSearch).order_by(WeatherSearch.searched_at.desc()).all()

    @staticmethod
    def get(db: Session, record_id: int) -> WeatherSearch | None:
        return db.query(WeatherSearch).filter(WeatherSearch.id == record_id).first()

    @staticmethod
    def delete(db: Session, record_id: int) -> WeatherSearch | None:
        record = HistoryService.get(db, record_id)
        if record:
            db.delete(record)
            db.commit()
        return record

