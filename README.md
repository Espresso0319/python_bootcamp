# python_bootcamp

Require Python 3.10+

## Environment build

```bash
python -m venv ./venv
source ./venv/bin/activate
pip3 install --user pipenv
python3 -m pipenv shell
pip install -r requirements.txt
```

## Service start up

```bash
uvicorn main:app --port 5000 --reload
```

## Docs

FastAPI has utilities to handle OpenAPI automatic UI documentation, including Swagger UI (by default at `/docs`)

http://localhost:5000/docs

## Test commands

### Test full request object

```bash
curl -X 'GET' \
  'http://127.0.0.1:5000/full-req-obj?token=mock-token' \
  -H 'accept: application/json' \
  -H "some-header: wtwertfbfdghdfgh" \
  -H "Cookie: cookie1=sdfgsdfgsdxcvbxcvb24234234;cookie2=5634535"
```

### Test getting settings

#### Set env

```bash
APP_NAME="new app" ADMIN_EMAIL="john@aaa.com" ITEMS_PER_USER=34 uvicorn main:app --port 5000 --reload
```

#### With .env

```bash
uvicorn another_app:app --port 5001 --reload
```
