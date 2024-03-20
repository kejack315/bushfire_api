# FireDangerRatingLaravel_New

This is a blank Laravel project with the user, user locations and suburb models.

- User and Fire Danger Ratings Endpoints need to be implemented as well as 
relevant controllers, etc..

- Send notifications to end users

Example microservice fetch 

```
// Example microservice call
$userSuburbId = 1111;
$userSuburb = Suburb::where('id', '=', $userSuburbId)->get()->first();
echo $userSuburb;
$microserviceResponse = Http::post('http://localhost:8000/fire-danger-ratings', [
    'suburb' => $userSuburb->name,
]);
echo $microserviceResponse;
```
