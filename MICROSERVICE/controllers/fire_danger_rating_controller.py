import os
import json
import sqlite3
import geopandas
from utils.log import log
from shapely.geometry import Point
from controllers.weather_controller import get_weather_forecast_for_coordinates


async def handle_fire_danger_rating_request(req_body):
    connection = sqlite3.connect("bushfire_warnings.db")
    db_cursor = connection.cursor()
    validate_res, loc_type = await validate_request(req_body)
    if not validate_res:
        if connection:
            connection.close()
        return {"status": 400, "error": "bad request"}
    req_body = json.loads(req_body)
    if loc_type == "district":
        # No weather info for district
        res_body = await get_ratings_by_district_name(req_body["district"], db_cursor)
        res_body["district"] = req_body["district"]
    elif loc_type == "suburb":
        res_body = await get_ratings_by_suburb_name(req_body["suburb"], db_cursor)
        res_body["suburb"] = req_body["suburb"]
    elif loc_type == "postal_code":
        res_body = await get_ratings_by_postal_code(req_body["postal_code"], db_cursor)
        res_body["postal_code"] = req_body["postal_code"]
    else:
        res_body = await get_ratings_by_coordinates(req_body["longitude"], req_body["latitude"], db_cursor)
        res_body["longitude"] = req_body["longitude"]
        res_body["latitude"] = req_body["latitude"]
    if not res_body:
        res_body = "No fire danger ratings found"
    if connection:
        connection.close()
    return {"status": 200, **res_body}


async def validate_request(req_body):
    req_body = json.loads(req_body)
    param_count = 0
    is_latitude = is_longitude = False
    loc_type = None
    if "suburb" in req_body:
        param_count += 1
        loc_type = "suburb"
    if "district" in req_body:
        param_count += 1
        loc_type = "district"
    if "postal_code" in req_body:
        param_count += 1
        loc_type = "postal_code"
    if "latitude" in req_body:
        is_latitude = True
    if "longitude" in req_body:
        is_longitude = True
    if is_latitude and is_longitude and param_count == 0:
        return True, "coordinates"
    elif param_count == 1 and not is_longitude and not is_latitude:
        return True, loc_type
    return False, None


async def get_ratings_by_district_id(district_id, db_cursor):
    db_cursor.execute(f"""SELECT rating_level, rating_name, rating_date, issued_at, created_at, 
                    updated_at FROM fire_danger_ratings WHERE district_id = {district_id}""")
    ratings = db_cursor.fetchall()
    res = {}
    if ratings:
        for row in ratings:
            rating_level = row[0]
            rating_name = row[1]
            rating_date = row[2]
            issued_at = row[3]
            created_at = row[4]
            updated_at = row[5]
            res[rating_date] = {
                "rating_level": rating_level,
                "rating_name": rating_name,
                "issued_at": issued_at,
                "created_at": created_at,
                "updated_at": updated_at
            }
        return res
    else:
        return {"message": "no fire danger ratings found for the location specified"}


async def get_ratings_by_suburb_name(suburb_name, db_cursor):
    db_cursor.execute(f"""SELECT longitude, latitude FROM suburbs WHERE 
                            name = '{suburb_name.upper()}'""")
    coordinates = db_cursor.fetchone()
    if not coordinates:
        return None
    long = coordinates[0]
    lat = coordinates[1]
    res_body = await get_ratings_by_coordinates(long, lat, db_cursor)
    return res_body


async def get_ratings_by_postal_code(postal_code, db_cursor):
    db_cursor.execute(f"""SELECT longitude, latitude FROM suburbs WHERE 
                        postal_code = '{postal_code}'""")
    coordinates = db_cursor.fetchone()
    if not coordinates:
        return None
    long = coordinates[0]
    lat = coordinates[1]
    res_body = await get_ratings_by_coordinates(long, lat, db_cursor)
    return res_body


async def get_ratings_by_coordinates(longitude, latitude, db_cursor):
    district_name = await translate_coords_to_district_name(longitude, latitude)
    if not district_name:
        return None
    district_id = await get_district_id_from_district_name(district_name, db_cursor)
    if not district_id:
        return None
    weather_forecast = await get_weather_for_coords(latitude=latitude, longitude=longitude)
    ratings = await get_ratings_by_district_id(district_id, db_cursor)
    return {"fire_danger_ratings": ratings, "weather_forecast": weather_forecast}


async def get_district_id_from_district_name(district_name, db_cursor):
    db_cursor.execute(f"""SELECT id FROM districts WHERE name = '{district_name.upper()}'""")
    district_id = db_cursor.fetchone()
    if not district_id:
        return None
    return district_id[0]


async def get_ratings_by_district_name(district_name, db_cursor):
    district_id = await get_district_id_from_district_name(district_name, db_cursor)
    if not district_id:
        return None
    return await get_ratings_by_district_id(district_id, db_cursor)


async def translate_coords_to_district_name(longitude, latitude):
    shapefile_path = os.path.join(os.getcwd(), "data", "geo_data", "IDM00007.shp")
    shapefile = geopandas.read_file(shapefile_path)
    point = Point(longitude, latitude)
    for index, row in shapefile.iterrows():
        if point.within(row["geometry"]):
            return row['DIST_NAME']
    return None


async def get_weather_for_coords(latitude, longitude):
    try:
        return get_weather_forecast_for_coordinates(latitude=latitude, longitude=longitude)
    except Exception as e:
        log('error', f"Failed to fetch weather forecast {e}")
    return None


async def get_all_current_fire_danger_ratings():
    connection = sqlite3.connect("bushfire_warnings.db")
    db_cursor = connection.cursor()
    db_cursor.execute(f"""SELECT districts.name as district_name, rating_level, rating_name, rating_date, issued_at, 
        fire_danger_ratings.created_at as created_at, fire_danger_ratings.updated_at as updated_at FROM 
        fire_danger_ratings INNER JOIN districts ON fire_danger_ratings.district_id = districts.id""")
    ratings = db_cursor.fetchall()
    res = {}
    for row in ratings:
        res[row[0]] = {}
    for row in ratings:
        rating_level = row[1]
        rating_name = row[2]
        rating_date = row[3]
        issued_at = row[4]
        created_at = row[5]
        updated_at = row[6]
        res[row[0]][rating_date] = {
            "rating_level": rating_level,
            "rating_name": rating_name,
            "issued_at": issued_at,
            "created_at": created_at,
            "updated_at": updated_at
        }
    connection.close()
    return res
