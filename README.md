# python_bootcamp

Require Python 3.10+

## Environment build

```bash
python3.10 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

## Service start up

```bash
uvicorn main:app --port 5000 --reload
```

## Docs

FastAPI has utilities to handle OpenAPI automatic UI documentation, including Swagger UI (by default at `/docs`)

http://localhost:5000/docs
