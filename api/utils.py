from geopy.distance import geodesic
from typing import Tuple


def get_ally_power(origin: Tuple, dist: Tuple, population: int):
    distance = get_distance(origin, dist)
    if distance > float(10000):
        return int(population * 0.25)
    elif distance > float(1000):
        return int(population * 0.5)
    else:
        return int(population)


def get_distance(origin, dist):
    return geodesic(origin, dist).kilometers