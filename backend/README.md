# ChipsTalk backend

FastAPI backend for ChipsTalk: REST API, WebSocket API, business logic and
PostgreSQL access.

## Requirements

- Python 3.11+
- A running PostgreSQL instance

## Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

cp .env.example .env
# edit .env with your local PostgreSQL credentials
```

## Run

```bash
uvicorn app.main:app --reload
```

`GET /health` should return `{"status": "ok"}` with HTTP 200.

## Tests

```bash
pytest
```

`tests/test_database.py` exercises the real PostgreSQL connection defined by
your `.env`; it is skipped automatically if no database is reachable.

## Configuration

All configuration is read from environment variables (see `.env.example`).
Never commit a real `.env` file or hardcode credentials.
