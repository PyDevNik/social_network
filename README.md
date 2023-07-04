# Fast API simple social network API

## API Docs -> `example.com/docs`

## Setup
```sh
pip install -r requirements.txt
```
Next, open `db/config.py` and enter database settings (url, name, etc.)

## Run
```sh
uvicorn api:app
```

## Example
```python
import requests
data = {
    "username": "Example",
    "email": "example@example.com",
    "password": "test"
}
response = requests.post("example.com/api/signup", json=data)
if response.ok:
    print(response.json["token"])
```

## Structure
### db - MongoDB Database
### fast_api - RESTful API