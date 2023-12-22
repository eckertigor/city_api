# City-api task solution

_INSTALLATION, app run and API is described in README.MD file_

## Solution

1. Firstly, I created the database structure and SQL script (db/001_init_db.sql) to generate the initial database. I decided to create many-to-many relation because it helps us to manage all the ally-city relations. Additionally, I added an INDEX on the city field in the city_ally table to enhance retrieval speed for GET requests.
2. Then I created an endpoints for retrieving city, adding new cities, updating city, deleting city (including adding and removing allied cities in case of updating allied_cities)
3. Then I created schemas for validation city input (api/schema.py) and CityModel and CityAlly models to use SQLAlchemy (api/db.py and api/models.py)
4. I also added validation for the 'beauty' field, ensuring it can only contain one of three possible values. 
5. On updating city requests I'm also updating the whole allied list if the 'allied_list' was passed as [] or null. In case of allied_list is not empty I decided to find difference between current allied cities and input of the new allied_cities list (to not updating allied_cities that already allies of City and exists in Update request).
6. Afterward, I implemented the calculation of a city's power during retrieval. I utilized the geopy library (api/utils.py) to compute the distance between ally coordinates and determine the power of allied cities.
7. At the end, I added a tests on city enpoints (using pytest) with mocking db methods. 
8. The application can accept environment variables for database connection settings (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB) in api/db.py. In case values don't provided, the default settings will be retrieved from api/settings.py.

### Installation

If you need to install Docker Desktop, go to the [Docker Get Started](https://www.docker.com/get-started/) page.
You will also need [`docker-compose`](https://docs.docker.com/compose/) to run.

To build and run application
```shell
cd city_api
make all
make run
```
The server will start on port 1337. Requests that can be sent (e.g. via Postman) (read about all API requests in README.md)


### Testing
```shell
make all ## if not called at INSTALLATION
make test
```