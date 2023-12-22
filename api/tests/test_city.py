import pytest
from fastapi.testclient import TestClient
from api.main import app
from api import db
from api import models
import json

client = TestClient(app)


def test_create_city(mocker):
    db_city = models.City(
        uuid='778b98a5-6482-4856-b812-17039ded49a9',
        name='Berlin',
        geo_location_latitude=52.520008,
        geo_location_longitude=13.404954,
        beauty='average',
        population=3000000,
        allied_cities=[]
    )
    mocker.patch("api.db.create_city", return_value=db_city)
    city_data = {
        "data": {
            "name": "Berlin",
            "geo_location_latitude": 52.520008,
            "geo_location_longitude": 13.404954,
            "beauty": "average",
            "population": 3000000,
            "allied_cities": []
        }
    }
    response = client.post("/city", json=city_data)
    assert response.status_code == 200
    assert response.json()['data']['population'] == city_data['data']['population']
    assert response.json()['data']['name'] == city_data['data']['name']
    assert response.json()['data']['geo_location_latitude'] == city_data['data']['geo_location_latitude']
    assert response.json()['data']['allied_cities'] == city_data['data']['allied_cities']


def test_create_city_with_ally(mocker):
    db_city_berlin = models.City(
        uuid='778b98a5-6482-4856-b812-17039ded49a9',
        name='Berlin',
        geo_location_latitude=52.520008,
        geo_location_longitude=13.404954,
        beauty='average',
        population=3000000,
        allied_cities=[]
    )
    db_city = models.City(
        uuid='18db3e9a-7a77-4996-9182-7d95585e6715',
        name='New York',
        geo_location_latitude=40.730610,
        geo_location_longitude=-73.935242,
        beauty='gorgeous',
        population=15000000,
        allied_cities=[db_city_berlin]
    )
    mocker.patch("api.db.create_city", return_value=db_city)
    city_data = {
        "data": {
            "name": "New York",
            "geo_location_latitude": 40.730610,
            "geo_location_longitude": -73.935242,
            "beauty": "gorgeous",
            "population": 15000000,
            "allied_cities": ['778b98a5-6482-4856-b812-17039ded49a9']
        }
    }
    response = client.post("/city", json=city_data)
    assert response.status_code == 200
    assert response.json()['data']['population'] == city_data['data']['population']
    assert response.json()['data']['name'] == city_data['data']['name']
    assert response.json()['data']['geo_location_latitude'] == city_data['data']['geo_location_latitude']
    assert response.json()['data']['allied_cities'] == city_data['data']['allied_cities']


def test_get_all_cities(mocker):
    db_city = models.City(
        uuid='18db3e9a-7a77-4996-9182-7d95585e6715',
        name='New York',
        geo_location_latitude=40.730610,
        geo_location_longitude=-73.935242,
        beauty='gorgeous',
        population=15000000,
        allied_cities=[]
    )
    mocker.patch("api.db.get_cities", return_value=[db_city
                                                       for i in range(3)])
    response = client.get("/city")
    assert response.status_code == 200
    assert len(response.json()['data']) == 3


def test_get_city(mocker):
    db_city_berlin = models.City(
        uuid='778b98a5-6482-4856-b812-17039ded49a9',
        name='Berlin',
        geo_location_latitude=52.520008,
        geo_location_longitude=13.404954,
        beauty='average',
        population=3000000,
        allied_cities=[]
    )
    db_city_ny = models.City(
        uuid='18db3e9a-7a77-4996-9182-7d95585e6715',
        name='New York',
        geo_location_latitude=40.730610,
        geo_location_longitude=-73.935242,
        beauty='gorgeous',
        population=15000000,
        allied_cities=[db_city_berlin]
    )
    db_city_barcelona = models.City(
        uuid='43fda7ec-2f69-41cf-a160-5286edb6bb49',
        name='Barcelona',
        geo_location_latitude=41.390205,
        geo_location_longitude=2.154007,
        beauty='ugly',
        population=2000000,
        allied_cities=[db_city_berlin, db_city_ny]
    )
    mocker.patch("api.db.get_city", return_value=db_city_barcelona)
    response = client.get("/city/43fda7ec-2f69-41cf-a160-5286edb6bb49")
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "city_uuid": "43fda7ec-2f69-41cf-a160-5286edb6bb49",
            "name": "Barcelona",
            "geo_location_latitude": 41.390205,
            "geo_location_longitude": 2.154007,
            "beauty": "ugly",
            "population": 2000000,
            "allied_cities": [
                "778b98a5-6482-4856-b812-17039ded49a9",
                "18db3e9a-7a77-4996-9182-7d95585e6715"
            ],
            "power": 11000000
        }
    }
    mocker.patch("api.db.get_city", return_value=None)
    response = client.get("/city/123")
    assert response.status_code == 404


def test_update_city(mocker):
    db_city_berlin = models.City(
        uuid='778b98a5-6482-4856-b812-17039ded49a9',
        name='Berlin',
        geo_location_latitude=52.520008,
        geo_location_longitude=13.404954,
        beauty='average',
        population=3000000,
        allied_cities=[]
    )
    db_city_ny = models.City(
        uuid='18db3e9a-7a77-4996-9182-7d95585e6715',
        name='New York',
        geo_location_latitude=40.730610,
        geo_location_longitude=-73.935242,
        beauty='gorgeous',
        population=15000000,
        allied_cities=[db_city_berlin]
    )
    db_city_barcelona = models.City(
        uuid='43fda7ec-2f69-41cf-a160-5286edb6bb49',
        name='Warsaw',
        geo_location_latitude=41.390205,
        geo_location_longitude=2.154007,
        beauty='ugly',
        population=2000000,
        allied_cities=[]
    )
    mocker.patch("api.db.update_city", return_value=db_city_barcelona)
    city_data = {
        "data": {
            "name": "Warsaw",
            "allied_cities": []
        }
    }
    response = client.patch("/city/43fda7ec-2f69-41cf-a160-5286edb6bb49", json=city_data)
    assert response.status_code == 200
    assert response.json()['data']['name'] == city_data['data']['name']
    assert response.json()['data']['allied_cities'] == city_data['data']['allied_cities']
    mocker.patch("api.db.update_city", return_value=None)
    response = client.patch("/city/123", json=city_data)
    assert response.status_code == 404


def test_delete_city(mocker):
    mocker.patch("api.db.delete_city", return_value=True)
    response = client.delete("/city/1")
    assert response.status_code == 204
    mocker.patch("api.db.delete_city", return_value=None)
    response = client.get("/test")
    assert response.status_code == 404