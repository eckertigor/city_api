import os
from sqlalchemy import create_engine, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.orm import sessionmaker, Session
from api import settings
import models
import schema

POSTGRES_URL = f"postgresql://{os.environ.get('POSTGRES_USER', settings.DEFAULT_POSTGRES_USER)}:" \
               f"{os.environ.get('POSTGRES_PASSWORD', settings.DEFAULT_POSTGRES_PASSWORD)}" \
               f"@{os.environ.get('POSTGRES_HOST', settings.DEFAULT_POSTGRES_HOSTNAME)}:" \
               f"{os.environ.get('POSTGRES_POST', settings.DEFAULT_POSTGRES_PORT)}/" \
               f"{os.environ.get('POSTGRES_DB', settings.DEFAULT_POSTGRES_DB)}"

engine = create_engine(
    POSTGRES_URL, echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_cities(session: Session):
    return session.query(models.City).all()


def get_city(session: Session, uuid: str):
    try:
        res = session.query(models.City).get(uuid)
    except (MultipleResultsFound, NoResultFound):
        res = None
    return res


def create_city(session: Session, city: schema.CityInput):
    db_city = models.City(
        name=city.data.name,
        geo_location_latitude=city.data.geo_location_latitude,
        geo_location_longitude=city.data.geo_location_longitude,
        beauty=city.data.beauty,
        population=city.data.population
    )
    for ally in city.data.allied_cities:
        ally_db = get_city(session, ally)
        db_city.allied_cities.append(ally_db)
        ally_db.allied_cities.append(db_city)
    session.add(db_city)
    session.commit()
    session.refresh(db_city)
    return db_city


def update_city(session: Session,
                    city_input: schema.CityUpdateInput,
                    city_uuid: str):
    city = get_city(session=session, uuid=city_uuid)
    if city is None:
        return None
    city_dict = city_input.model_dump().get('data')
    allied_cities_input = city_dict.pop('allied_cities')
    for field, value in city_dict.items():
        if value is not None:
            setattr(city, field, value)
    if allied_cities_input != [None]:
        allied_city = [ally.uuid for ally in city.allied_cities]
        allies_diff = list(set(allied_city).difference(allied_cities_input))
        allied_update_diff = list(set(allied_cities_input).difference(allied_city))
        for ally in allies_diff:
            ally_db = get_city(session, ally)
            ally_db.allied_cities.remove(city)
            city.allied_cities.remove(ally_db)
        for ally in allied_update_diff:
            ally_db = get_city(session, ally)
            city.allied_cities.append(ally_db)
            ally_db.allied_cities.append(city)
    elif allied_cities_input == [] or allied_cities_input is None:
        city.allied_cities[:] = []
    session.add(city)
    session.commit()
    session.refresh(city)
    return city


def delete_city(session: Session, city_uuid: str):
    city = get_city(session=session, uuid=city_uuid)
    allied_cities = [ally.uuid for ally in city.allied_cities]
    for ally in allied_cities:
        ally_db = get_city(session, ally)
        ally_db.allied_cities.remove(city)
        city.allied_cities.remove(ally_db)
    session.commit()
    session.delete(city)
    session.commit()
    return True
