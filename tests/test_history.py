from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models import WeatherSearch

client = TestClient(app)


def setup_function():
    db = SessionLocal()
    db.query(WeatherSearch).delete()
    db.commit()
    db.add(WeatherSearch(city="Delhi", country="IN", temperature=28.5))
    db.commit()
    db.close()


def test_history_list_and_record():
    list_response = client.get("/api/v1/history")
    assert list_response.status_code == 200
    records = list_response.json()
    assert len(records) == 1

    record_id = records[0]["id"]
    detail_response = client.get(f"/api/v1/history/{record_id}")
    assert detail_response.status_code == 200
    assert detail_response.json()["city"] == "Delhi"


def test_delete_history_record():
    db = SessionLocal()
    record = db.query(WeatherSearch).first()
    record_id = record.id
    db.close()

    response = client.delete(f"/api/v1/history/{record_id}")
    assert response.status_code == 204

    missing_response = client.delete(f"/api/v1/history/{record_id}")
    assert missing_response.status_code == 404
