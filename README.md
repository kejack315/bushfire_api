# Fire Danger Rating API Backend

## Overview

This repository contains the Laravel backend and Python microservice for the bushfire
danger rating project.

The Laravel API is responsible for handling all incoming requests, sending notifications to the
mobile application and for handling user accounts and authentication.

The microservice collects current danger rating information from the BOM using a web purpose
built web scraper. If the web scraper fails the microservice will fetch the current information
through BOM's FTP server. The microservice runs a background task to continuously sync up the 
data to ensure that it is up-to-date. This microservice is also responsible for fetching current
weather information from an external API.

## API Endpoints

### Fire Danger  Rating Endpoints

---

**Get a fire danger rating and weather information**
```
GET /api/fire-danger-ratings
```

**Request Body Format**

All location types except for district, will also return the weather forecast for that specified area.

Get current fire ratings by district name:
```json
{
  "district": "Lockwood"
}
```

Get current fire ratings by suburb name:
```json
{
  "suburb": "Perth"
}
```

Get current fire ratings by postal code:
```json
{
  "postal_code": "6010"
}
```

Get current fire ratings by coordinates:
```json
{
  "longitude": "115.7946864264016",
  "latitude": "-31.95038022090634"
}
```
---

**Get the current users primary location fire danger rating and weather information**
```
GET /api/me/fire-danger-ratings
```

---

**Get all fire danger ratings for every district**
```
GET /api/all/fire-danger-ratings
```

---

### Users/Accounts Endpoints & Authentication

**TODO: @Jason Ke ENDPOINTS HERE**

Register a new user account
```
```

Login to user account
```
```

Logout of user account
```
```

**TODO: @Jason Ke AUTH INSTRUCTIONS HERE PLACEHOLDER**

### Push Notifications

**TODO: @Victor Wilson**

## Running Locally

Clone project repository
```
git clone https://github.com/Yannis-S/FireDangerRatingLaravel_New
```

Navigate into project directory
```
cd ./FireDangerRatingLaravel_New
```

### Setup & Run Microservice

Navigate into microservice directory
```
cd ./MICROSERVICE
```
Create a new virtual environment
```
python venv venv
```
Activate the virtual environment
```
./venv/Scripts/activate
```
Install pip packages
```
pip install -r requirements.txt
```
Run the microservice
```
python ./main.py
```

_**Note:** If the default port 8000 is busy on your local machine you can modify, the port of the microservice in the `microservice.port` file._

### Setup & Run Laravel API

Set the project root folder in Laragon to `/FireDangerRatingLaravel_New/API/public` and run the 
Apache & MySQL server

Navigate into the API directory
```
cd ../API
```
Install composer packages 
```
composer install
```
Copy .env.example file into .env
```
cp .env.example .env
```
Add database connection details to .env file and microservice endpoint if it is not running on default
endpoint/port
```dotenv
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=DATABASE_NAME
DB_USERNAME=DATABASE_USERNAME
DB_PASSWORD=DATABASE_PASSWORD
...
DANGER_RATING_MICROSERVICE_ENDPOINT="http://localhost:8000/"
```
Generate new keys
```
php artisan key:generate
```
Run migrations and seeders
```
php artisan migrate:fresh --seed
```
Install and run npm
```
npm install && npm run dev
```

## User Accounts & Authentication

**TODO: @Jason Ke**

## Push Notifications


