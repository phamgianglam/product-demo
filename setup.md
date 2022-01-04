# Setup product service:

## Setup
1.  Create virtual environment
virtualenv -v python3.8 env
2.  Enable environment and install requires package
source env/bin/activate
pip install -r requirements.txt
3.  Create an postgres database product_demo
4.  export following environment variable
export DATABASE_URL=postgresql://<user_name>:<password>@<db_host>/product_demo
export FILTER_RECORD_API=http://localhost:8000/api (filter api service is required)
5.  Migrate database
alembic upgrade heads
6. (Optional) Update database with load data
pytest tests/test_pass.py
7. run server.
uvicorn product_api.app:app --reload --port 9000

## Using curl and swagger.
This project is base on FastAPI framework, as a result it come with interactive swagger page
which allow user to test apis endpoint.
To access swagger page: http://localhost:90000/api

curl command:

filter with name=sample 

curl  -X 'GET' 'localhost:9000/api/product/?search=name:sample' 

filter with name=sample with descinding order

curl  -X 'GET' 'localhost:9000/api/product/?search=name:sample&order=desc' 

filter with name=sample with descending order

get data in price range 20-100, price ascending
curl  -X 'GET' 'localhost:9000/api/product/?price=20-100&order=price:asc' 

create data
curl -X 'POST' \
  'http://localhost:9000/api/product/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "sample product",
  "description": "this is sample product",
  "price": 20,
  "date": "2022-01-01T13:40:40.603227"
}'


## Run test

unit test
pytest tests/unit_test

integration test
pytest test/integration_test