import pandas as pd
import requests_cache
import openmeteo_requests
from utils.log import log
from retry_requests import retry


cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


def get_weather_forecast_for_coordinates(longitude, latitude):
    log("info", f"Fetching weather forecast for {latitude}, {longitude}")
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "rain_sum", "showers_sum",
                  "snowfall_sum", "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant"],
        "timezone": "Asia/Singapore"
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(2).ValuesAsNumpy()
    daily_rain_sum = daily.Variables(3).ValuesAsNumpy()
    daily_showers_sum = daily.Variables(4).ValuesAsNumpy()
    daily_snowfall_sum = daily.Variables(5).ValuesAsNumpy()
    daily_wind_speed_10m_max = daily.Variables(6).ValuesAsNumpy()
    daily_wind_gusts_10m_max = daily.Variables(7).ValuesAsNumpy()
    daily_wind_direction_10m_dominant = daily.Variables(8).ValuesAsNumpy()
    daily_data = {"date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    ), "temperature_2m_max": daily_temperature_2m_max, "temperature_2m_min": daily_temperature_2m_min,
        "precipitation_sum": daily_precipitation_sum, "rain_sum": daily_rain_sum, "showers_sum": daily_showers_sum,
        "snowfall_sum": daily_snowfall_sum, "wind_speed_10m_max": daily_wind_speed_10m_max,
        "wind_gusts_10m_max": daily_wind_gusts_10m_max,
        "wind_direction_10m_dominant": daily_wind_direction_10m_dominant}
    daily_dataframe = pd.DataFrame(data=daily_data)
    res_dict = {}
    count = 0
    for _, row in daily_dataframe.iterrows():
        if count != 0 and count < 5:
            res_dict[str(row["date"])[:str(row["date"]).index(" ")]] = {
                "temp_max": row["temperature_2m_max"],
                "temp_min": row["temperature_2m_min"],
                "precipitation_sum": row["precipitation_sum"],
                "rain_sum": row["rain_sum"],
                "showers_sum": row["showers_sum"],
                "wind_speed_max": row["wind_speed_10m_max"],
                "wind_gusts_max": row["wind_gusts_10m_max"],
                "wind_direction": row["wind_direction_10m_dominant"]
            }
        count += 1
    return res_dict
