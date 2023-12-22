from fastapi import FastAPI, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import uvicorn
from api import db
import schema

app = FastAPI(debug=True)


@app.get("/city/{city_uuid}")
async def get_city(city_uuid: str,
                         session: Session = Depends(db.get_db)):
    city = db.get_city(session, city_uuid)
    if not city:
        error = schema.error_to_response("conflict",
                                         f"City with UUID {city_uuid} doesn't exist")
        return JSONResponse(content=schema.ErrorResponse(errors=[error]).dict(),
                            status_code=404)
    city_data = schema.city_model_to_power_response(city)
    return schema.CityPowerResponse(data=city_data)

@app.get("/city")
async def get_all_cities(session: Session = Depends(db.get_db)):
    cities = db.get_cities(session)
    cities_data = [schema.city_model_to_response(city)
                   for city in cities]
    return schema.CitiesResponseList(data=cities_data)


@app.post("/city")
async def create_city(city: schema.CityInput,
                      session: Session = Depends(db.get_db)):
    city = db.create_city(session, city)
    if not city:
        error = schema.error_to_response("conflict",
                                         "Ally city with this UUID doesn't exist")
        return JSONResponse(content=schema.ErrorResponse(errors=[error]).dict(),
                            status_code=400)
    city_data = schema.city_model_to_response(city)
    return schema.CityResponse(data=city_data)


@app.patch("/city/{city_uuid}")
async def update_city(city_uuid: str, city: schema.CityUpdateInput,
                      session: Session = Depends(db.get_db)):
    city = db.update_city(session, city, city_uuid)
    if not city:
        error = schema.error_to_response("conflict",
                                         f"City with UUID {city_uuid} doesn't exist")
        return JSONResponse(content=schema.ErrorResponse(errors=[error]).dict(),
                            status_code=404)
    city_data = schema.city_model_to_response(city)
    return schema.CityResponse(data=city_data)


@app.delete("/city/{city_uuid}", status_code=204)
async def delete_city(city_uuid: str,
                      session: Session = Depends(db.get_db)):
    city = db.delete_city(session, city_uuid)
    if not city:
        error = schema.error_to_response("not_found",
                                         f"Requested City with UUID {str(city_uuid)} does not exist")
        return JSONResponse(content=schema.ErrorResponse(errors=[error]).dict(),
                            status_code=404)
    else:
        return status.HTTP_204_NO_CONTENT

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=1337, workers=2)
