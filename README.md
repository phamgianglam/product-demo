# product-demo

## Introduction 
This is product-api endpoint which is responsible for handlinng req uests 
related to product. 

## Design
This services currently have three operation:
- GET /product: which is use for list products base on user's filter. After
  each time it successfully fetch data, it will invoke a function which 
  forward filters to filter api service which will record all filter.

- GET /product/<id>: this will return a single user base on their id
- POST /product: This operation allow user to create a product.

### GET /product:
-   There are four params are designed for filtering data, these are:
    +   price: product 's price range, which are use for request data in specific
        price range. It has format <min-value>-<max-value>
    +   search, df, and order: both search and order have format <key>:<value>.
        df field is used as a keywhen no key is given in search and order field.
        The former two will assume value in df is their key value when only values
        are given. Default, if no data is given, product will be sort by name in asc order.
        Currently, search filed can only search string value, it can search multiple key,
        value pair with pattern <key1>:<value1> + <key2>:<value2> and <value1>:<value2>.
        Search field will assume search by name if no key given.
-   page and size are paging param.

-   Sample return data:
```json
[
  {
    "id": "a997f12f-6918-4209-a2e6-de1f8c878228",
    "name": "sample product",
    "description": "this is sample product",
    "price": 20,
    "date": "2022-01-01T13:40:40.603227"
  }
]
```

### GET /product/<id>:
-   This operation return single product base on its id.
-   Sample return data:
```json
  {
    "id": "a997f12f-6918-4209-a2e6-de1f8c878228",
    "name": "sample product",
    "description": "this is sample product",
    "price": 20,
    "date": "2022-01-01T13:40:40.603227"
  }
```
### GET /product/<id>:
-   Create a product base on json
-   Sample request data:
```json
  {
    "name": "sample product",
    "description": "this is sample product",
    "price": 20,
    "date": "2022-01-01T13:40:40.603227"
  }
```
-   Sample return data:
```json
  {
    "id": "a997f12f-6918-4209-a2e6-de1f8c878228",
    "name": "sample product",
    "description": "this is sample product",
    "price": 20,
    "date": "2022-01-01T13:40:40.603227"
  }
```
### Code Base:
Code base are divided into three part: apis, controller, model.
-   apis: Repesent apis, these will handle the call and return value to user.
-   controller: is the component that will working directly with database and excute
    others task such as update data to other service or validate data.
-   model: these are database model, which represent object in database. 

## Testing 
Due to time constraint, not all function tested.
### Unit test
Controller functions are tested by using a fixture to provide an database
session which is used for communicate with database. Preset data is add 
to db if fixture load_data is used.

### Integration test
Tests are perform by using test client.
