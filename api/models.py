from sqlalchemy import Column, Float, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID, TEXT, ENUM
from sqlalchemy.orm import relationship

Base = declarative_base()

beauty_enum = ['ugly', 'average', 'gorgeous']


class CityAlly(Base):
    __tablename__ = "city_ally"

    city = Column(UUID, ForeignKey('city.uuid'), primary_key=True)
    ally = Column(UUID, ForeignKey('city.uuid'), primary_key=True)


class City(Base):
    __tablename__ = "city"

    uuid = Column(UUID, primary_key=True, index=True, server_default='uuid_generate_v4()')
    name = Column(TEXT, nullable=False)
    geo_location_latitude = Column(Float, nullable=False)
    geo_location_longitude = Column(Float, nullable=False)
    beauty = Column(ENUM(*beauty_enum, name='beauty_enum'), nullable=False)
    population = Column(BigInteger, nullable=False)
    allied_cities = relationship('City', secondary='city_ally',
                             back_populates='allied_cities',
                             primaryjoin=uuid==CityAlly.city,
                             secondaryjoin=uuid==CityAlly.ally,
                             collection_class=list)
