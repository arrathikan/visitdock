# VisitDock Backend

FastAPI backend service for VisitDock Clinic Appointment Management.

## Development Setup

```bash
# From backend directory:
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running the Development Server

```bash
uvicorn app.main:app --reload --port 8000
```

- API Base: `http://localhost:8000`
- Health check: `http://localhost:8000/health`
- OpenAPI Docs: `http://localhost:8000/docs`

## Tests and Linting

```bash
# Run tests
python -m pytest -q

# Run linter
ruff check .
```
