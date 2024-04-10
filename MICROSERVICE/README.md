# FireDangerRatingAPI-FastAPI Microservice

A simple, microservice built to serve fire danger ratings for Western Australia. This microservice is built
on-top of the asynchronous FastAPI framework.

## 🔥 Features

**💾 Multiple Data Sources** - This microservice can collect data through the BOM FTP server as well as through
the BOM's website with a web scraper. The web scraper, although faster, is considerably more unreliable than
collecting data through the FTP server. The data sync process that runs in the background will attempt to use
the web scraper and if that fails it will fall back and use the FTP data source.

**🔁 Background Data Syncing** - The data sources are queried once a minute to ensure the data currently stored
in the local DB instance is up-to-date. The data will only be updated if there are changes to the current fire
warnings stored in the table. In the unlikely event that a request hits the endpoint while a data sync is in progress.
The request will be delayed until the sync is completed.

**🌞 Weather Forecast** - The current and upcoming weather forecast is included in the response payload to provide
the end user with more thorough information about fire conditions for a given area. *Not included when retrieving
by district name.

## 💻 Running Locally

To run the microservice locally outside a container run these commands (or equivalent commands for your device) from
the root of the project directory:

```
python venv venv
```

```
./venv/Scripts/activate
```

```
pip install -r requirements.txt
```

```
python ./main.py
```


## ❔ Usage

The fire danger warnings are served through a single API POST endpoint.

`/fire-danger-ratings`

### Request Body

All location types except for district, will also return the weather forecast for that specified area.

**Get current fire ratings by district name:**
```json
{
  "district": "Lockwood"
}
```

**Get current fire ratings by suburb name:**
```json
{
  "suburb": "Perth"
}
```

**Get current fire ratings by postal code:**
```json
{
  "postal_code": "6010"
}
```

**Get current fire ratings by coordinates:**
```json
{
  "longitude": "115.7946864264016",
  "latitude": "-31.95038022090634"
}
```

### Response Format

**Example response:**
```json
{
    "status": 200,
    "fire_danger_ratings": {
        "2024-03-13": {
            "rating_level": 28,
            "rating_name": "High",
            "issued_at": "2024-03-13 16:10:00",
            "created_at": "2024-03-13 17:27:23.426977",
            "updated_at": "2024-03-13 17:27:23.426977"
        },
        "2024-03-14": {
            "rating_level": 20,
            "rating_name": "Moderate",
            "issued_at": "2024-03-13 16:10:00",
            "created_at": "2024-03-13 17:27:23.426977",
            "updated_at": "2024-03-13 17:27:23.426977"
        },
        "2024-03-15": {
            "rating_level": 18,
            "rating_name": "Moderate",
            "issued_at": "2024-03-13 16:10:00",
            "created_at": "2024-03-13 17:27:23.426977",
            "updated_at": "2024-03-13 17:27:23.426977"
        },
        "2024-03-16": {
            "rating_level": 20,
            "rating_name": "Moderate",
            "issued_at": "2024-03-13 16:10:00",
            "created_at": "2024-03-13 17:27:23.426977",
            "updated_at": "2024-03-13 17:27:23.426977"
        }
    },
    "weather_forecast": {
        "2024-03-13": {
            "temp_max": 31.27400016784668,
            "temp_min": 21.02400016784668,
            "precipitation_sum": 0.0,
            "rain_sum": 0.0,
            "showers_sum": 0.0,
            "wind_speed_max": 18.03236961364746,
            "wind_gusts_max": 41.39999771118164,
            "wind_direction": 104.81594848632812
        },
        "2024-03-14": {
            "temp_max": 33.7239990234375,
            "temp_min": 21.674001693725586,
            "precipitation_sum": 0.0,
            "rain_sum": 0.0,
            "showers_sum": 0.0,
            "wind_speed_max": 18.94024085998535,
            "wind_gusts_max": 43.19999694824219,
            "wind_direction": 86.31632995605469
        },
        "2024-03-15": {
            "temp_max": 34.2239990234375,
            "temp_min": 23.124000549316406,
            "precipitation_sum": 0.0,
            "rain_sum": 0.0,
            "showers_sum": 0.0,
            "wind_speed_max": 15.844088554382324,
            "wind_gusts_max": 34.91999816894531,
            "wind_direction": 65.98249816894531
        },
        "2024-03-16": {
            "temp_max": 24.924001693725586,
            "temp_min": 19.974000930786133,
            "precipitation_sum": 0.0,
            "rain_sum": 0.0,
            "showers_sum": 0.0,
            "wind_speed_max": 16.676977157592773,
            "wind_gusts_max": 41.03999710083008,
            "wind_direction": 209.22628784179688
        }
    },
    "suburb": "mosman park"
}
```

---

_Developed by **Yannis Seimenis**_ 











