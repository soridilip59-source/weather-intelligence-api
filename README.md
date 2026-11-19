# Weather Intelligence API

Weather Intelligence API is a modular Python backend that retrieves real-time weather information from OpenWeather and stores city search history in SQLite.

## Problem Statement

People need reliable, current weather information for travel planning, daily decisions, and general awareness. This project provides a RESTful API that validates city searches, retrieves weather data from an external provider, standardizes the response, and keeps a searchable history of previous requests.

## Technology Stack

- Python 3
- FastAPI
- Uvicorn
- HTTPX
- SQLite
- SQLAlchemy
- Pydantic
- Python-dotenv
- Pytest
- Swagger UI

## Features

- Retrieve current weather by city name
- Use a browser-based dashboard to search weather and view recent searches
- Store weather searches in SQLite
- List, retrieve, and delete search history records
- Validate city names
- Handle missing API keys, network failures, timeouts, and external API errors
- Interactive API documentation through Swagger UI

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

Open `http://127.0.0.1:8000/` for the weather dashboard or `/docs` for Swagger UI.

## PostgreSQL Setup

For local PostgreSQL:

1. Install PostgreSQL and create a database.
2. Add this line to `.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/weather_intelligence
```

3. Install dependencies and start the app:

```powershell
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

For Render or Railway, create a PostgreSQL database and copy its internal or external connection URL into the `DATABASE_URL` environment variable. The app also accepts legacy `postgres://` URLs and converts them automatically.

## Deploy on Render

1. Push the repository to GitHub.
2. Open Render and select **New > Blueprint**.
3. Connect the `weather-intelligence-api` repository.
4. Render will create the free `weather-intelligence-api` web service and `weather-intelligence-db` database using `render.yaml`.
5. Add the `OPENWEATHER_API_KEY` secret in the Render environment settings.
6. Deploy and open `/docs`, for example:

```text
https://weather-intelligence-api.onrender.com/docs
```

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | Weather dashboard |
| `GET` | `/health` | Application health check |
| `GET` | `/api/v1/weather?city=Delhi` | Get current weather for a city |
| `GET` | `/api/v1/history` | Retrieve all search history |
| `GET` | `/api/v1/history/{id}` | Retrieve one history record |
| `DELETE` | `/api/v1/history/{id}` | Delete one history record |

## Sample Responses

### Current Weather

`GET /api/v1/weather?city=Delhi`

```json
{
  "city": "Delhi",
  "country": "IN",
  "temperature": 28.5,
  "feels_like": 30.2,
  "humidity": 65,
  "description": "Clear Sky",
  "wind_speed": 3.5
}
```

### Dashboard

Open `/` in a browser to search for a city and view saved searches.

### Health

`GET /health`

```json
{
  "status": "ok"
}
```

## Screenshots

Add screenshots of the running application and Swagger documentation to this section:

1. Start the server with `uvicorn app.main:app --reload`.
2. Capture the dashboard at `http://127.0.0.1:8000/` and Swagger UI at `/docs`.
3. Save the images in a `screenshots/` directory and link them here.

<!-- Example:
![Swagger UI](screenshots/swagger-ui.png)
![Weather response](screenshots/weather-response.png)
-->

## Tests

```powershell
pytest -q
```
