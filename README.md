# Weather Intelligence API

A modular FastAPI backend that retrieves current weather data from OpenWeather and stores search history in SQLite.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `OPENWEATHER_API_KEY` in `.env`, then start the API:

```powershell
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for Swagger UI.

## Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /api/v1/weather?city=Delhi` - Current weather
- `GET /api/v1/history` - Search history
- `GET /api/v1/history/{id}` - One history record
- `DELETE /api/v1/history/{id}` - Delete a history record

## Tests

```powershell
pytest -q
```
