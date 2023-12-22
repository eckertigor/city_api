## Before starting

_Solution is described in SOLUTION.MD file_

### Installation

If you need to install Docker Desktop, go to the [Docker Get Started](https://www.docker.com/get-started/) page.
You will also need [`docker-compose`](https://docs.docker.com/compose/) to run.

To build and run application
```shell
cd city_api
make all
make run
```
The server will start on port 1337. Requests that can be sent (e.g. via Postman)
1. Adding new city
```http
POST
http://localhost:1337/city
```
Request body
```json
{
    "data": {
        "name": "New York",
        "geo_location_latitude": 40.730610,
        "geo_location_longitude": -73.935242,
        "beauty": "Ugly",
        "population": 3000000,
        "allied_cities": []
    }
}
```


Response body 
```json
{
    "data": {
        "city_uuid": "52423516-d224-46a2-8aa1-501f5a9f39b1",
        "name": "New York",
        "geo_location_latitude": 40.73061,
        "geo_location_longitude": -73.935242,
        "beauty": "ugly",
        "population": 3000000,
        "allied_cities": []
    }
}
```

2. Adding new city with ally city (with UUID generated in step 1)
```http
POST
http://localhost:1337/city
```
Request body
```json
{
    "data": {
        "name": "Berlin",
        "geo_location_latitude": 52.520008,
        "geo_location_longitude": 13.404954,
        "beauty": "Ugly",
        "population": 3000000,
        "allied_cities": ["52423516-d224-46a2-8aa1-501f5a9f39b1"]     
    }
}
```

Response body 
```json
{
    "data": {
        "city_uuid": "31bd0d6a-d7fb-4989-b19e-fa21d160a7f6",
        "name": "Berlin",
        "geo_location_latitude": 52.520008,
        "geo_location_longitude": 13.404954,
        "beauty": "average",
        "population": 3000000,
        "allied_cities": [
            "52423516-d224-46a2-8aa1-501f5a9f39b1"
        ]
    }
}
```

3. Getting all cities
```http
GET
http://localhost:1337/city
```
Response body 
```json
{
    "data": [
        {
            "city_uuid": "52423516-d224-46a2-8aa1-501f5a9f39b1",
            "name": "New York",
            "geo_location_latitude": 40.73061,
            "geo_location_longitude": -73.935242,
            "beauty": "ugly",
            "population": 3000000,
            "allied_cities": [
                "31bd0d6a-d7fb-4989-b19e-fa21d160a7f6"
            ]
        },
        {
            "city_uuid": "31bd0d6a-d7fb-4989-b19e-fa21d160a7f6",
            "name": "Berlin",
            "geo_location_latitude": 52.520008,
            "geo_location_longitude": 13.404954,
            "beauty": "average",
            "population": 3000000,
            "allied_cities": [
                "52423516-d224-46a2-8aa1-501f5a9f39b1"
            ]
        }
    ]
}
```


4. Updating city
```http
PATCH
http://localhost:1337/city/52423516-d224-46a2-8aa1-501f5a9f39b1
```
Request body
```json
{
    "data": {
        "beauty": "Gorgeous",
        "population": 8468000
    }
}
```


Response body 
```json
{
    "data": {
        "city_uuid": "52423516-d224-46a2-8aa1-501f5a9f39b1",
        "name": "New York",
        "geo_location_latitude": 40.73061,
        "geo_location_longitude": -73.935242,
        "beauty": "gorgeous",
        "population": 8468000,
        "allied_cities": [
            "31bd0d6a-d7fb-4989-b19e-fa21d160a7f6"
        ]
    }
}
```

5. Retieving city

```http
GET
http://localhost:1337/city/52423516-d224-46a2-8aa1-501f5a9f39b1
```

Response body - STATUS 200
```json
{
    "data": {
        "city_uuid": "52423516-d224-46a2-8aa1-501f5a9f39b1",
        "name": "New York",
        "geo_location_latitude": 40.73061,
        "geo_location_longitude": -73.935242,
        "beauty": "gorgeous",
        "population": 8468000,
        "allied_cities": [
            "31bd0d6a-d7fb-4989-b19e-fa21d160a7f6"
        ],
        "power": 9968000
    }
}
```

6. Deleting city
```http
DELETE
http://localhost:1337/city/52423516-d224-46a2-8aa1-501f5a9f39b1
```
Response 
```http
STATUS 204
```
## Testing
```shell
make all ## if not called at INSTALLATION
make test
```
