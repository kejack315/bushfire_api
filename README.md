#  🔥 Fire Danger Rating API Backend

## Table of Contents

[**1.** Overview](#1-overview)
- [**1.1** Project Overview](#11-project-overview)

[**2.** Laravel API](#2-laravel-api)
- [**2.1** Overview](#21-overview)
- [**2.2** Installation & Dependencies](#22-installation--dependencies)
- [**2.3** Endpoints & Usage](#23-endpoints--usage)
- [**2.4** User Accounts & Authentication](#24-user-accounts--authentication)
- [**2.5** End User Application Push Notifications](#25-end-user-application-push-notifications)

[**3.** Data Microservice API](#3-data-microservice-api)
- [**3.1** Overview](#31-overview)
- [**3.2** Installation & Dependencies](#32-installation--dependencies)

## 1. Overview

### 1.1 Project Overview

This repository contains the Laravel backend and Python microservice for the bushfire danger rating project.

## 2. Laravel API

### 2.1 Overview

The Laravel API is responsible for handling all incoming requests, sending notifications to the mobile application and for handling user accounts and authentication.

### 2.2 Installation & Dependencies

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

### 2.3 Endpoints & Usage

**Get a fire danger rating and weather information**
```
GET /api/fire-danger-ratings
```

Request Body Format:

_All location types except for district, will also return the weather forecast for that specified area._

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

**Get the current users primary location fire danger rating and weather information**
```
GET /api/me/fire-danger-ratings
```

**Get all fire danger ratings for every district**
```
GET /api/all/fire-danger-ratings
```
**API documentation - swagger**

Install composer packages
```
composer require darkaonline/l5-swagger
php artisan vendor:publish --provider "L5Swagger\L5SwaggerServiceProvider"
php artisan l5-swagger:generate
```
Test API
```
Go to http://your_api_url/api/documentation
```
**Register for User Account**
```
POST /api/register
```
Request Body Format:
```json
{
  "name": "AAA",
  "email": "AAA@gmail.com",
  "password": "a123456",
  "confirm_password": "a123456",
  "suburb": "PERTH"
}
```
**Log In to User Account**
```
POST /api/login
```

**Log Out of User Account**
```
GET /api/logout
```



**End User Push Notifications**
```
TODO @Victor
```

### 2.4 User Accounts & Authentication

**TODO: WRITE DOCUMENTATION FOR USER ACCOUNTS & AUTHENTICATION @JASON**

### 2.5 End User Application Push Notifications

**TODO: WRITE DOCUMENTATION FOR END USER APPLICATION PUSH NOTIFICATIONS @JASON**

## 3. Data Microservice API

### 3.1 Overview

A simple, microservice built to serve fire danger ratings for Western Australia. This microservice is built
on-top of the asynchronous FastAPI framework.

The microservice collects current danger rating information from the BOM using a web purpose
built web scraper. If the web scraper fails the microservice will fetch the current information
through BOM's FTP server. The microservice runs a background task to continuously sync up the 
data to ensure that it is up-to-date. This microservice is also responsible for fetching current
weather information from an external API.

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

### 3.2 Installation & Dependencies

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

**MacOS:** When runnning this project on MacOS you will need to have gdal ( Geospatial Data Abstraction Library) installed on your local machine before running. To install gdal using cask run the following.

```
brew install gdal
```

**Note:** If the default port 8000 is busy on your local machine you can modify, the port of the microservice in the `microservice.port` file.

