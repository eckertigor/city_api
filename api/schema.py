from typing import List, Optional, Union
from api.models import City
from pydantic import BaseModel, field_validator, UUID4, Field


class CityData(BaseModel):
    city_uuid: UUID4
    name: str
    geo_location_latitude: float
    geo_location_longitude: float
    beauty: str
    population: int
    allied_cities: List[UUID4]


class CityDataInput(BaseModel):
    name: str
    geo_location_latitude: float
    geo_location_longitude: float
    beauty: str
    population: int
    allied_cities: Optional[List[UUID4]]

    @field_validator('beauty')
    def check_beauty(cls, val: str) -> str:
        if val.lower() not in ['ugly', 'average', 'gorgeous']:
            raise ValueError("beauty field must be one of Ugly, Average or Gorgeous")
        return val.lower()

    @field_validator('allied_cities')
    def check_allied_cities(cls, val) -> list:
        if isinstance(val, List):
            return val
        return []


class CityDataUpdateInput(BaseModel):
    name: Optional[str] = None
    geo_location_latitude: Optional[float] = None
    geo_location_longitude: Optional[float] = None
    beauty: Optional[str] = None
    population: Optional[int] = None
    allied_cities: Optional[List[UUID4]] = [None]

    @field_validator('beauty')
    def check_beauty(cls, val: str):
        if not val:
            return None
        if val.lower() not in ['ugly', 'average', 'gorgeous']:
            raise ValueError("beauty field must be one of Ugly, Average or Gorgeous")
        return val.lower()

    @field_validator('allied_cities')
    def check_allied_cities(cls, val) -> list:
        if isinstance(val, List):
            return val
        return []


class CityInput(BaseModel):
    data: CityDataInput


class CityUpdateInput(BaseModel):
    data: CityDataUpdateInput


class CitiesResponseList(BaseModel):
    data: List[CityData]

    class Config:
        orm_mode = True


class CityResponse(BaseModel):
    data: CityData

    class Config:
        orm_mode = True


def city_model_to_response(city: City) -> CityData:
    data = CityData(
        city_uuid=city.uuid,
        name=city.name,
        geo_location_latitude=city.geo_location_latitude,
        geo_location_longitude=city.geo_location_longitude,
        beauty=city.beauty,
        population=city.population,
        allied_cities=[ally.uuid for ally in city.allied_cities]
    )
    return data


def error_to_response(code, detail):
    return Error(
        code=code,
        detail=detail
    )


class Error(BaseModel):
    code: str
    detail: str


class ErrorResponse(BaseModel):
    errors: List[Error]
