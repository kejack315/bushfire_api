<?php

namespace App\Http\Controllers;

use App\Models\Suburb;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Http;

class FireDangerRatingController extends Controller
{

    private string $microserviceBaseEndpoint;

    public function __construct() {
        $this->microserviceBaseEndpoint = config(
            "DANGER_RATING_MICROSERVICE_ENDPOINT", "http://localhost:8000/");
    }
    /**
     * @OA\Get(
     *     path="/api/fire-danger-ratings",
     *     summary="Get FireDangerRating",
     *     tags={"FireDangerRating"},
     *     description="Get FireDangerRating",
     *     security={{"bearerAuth": {}}},
     *     @OA\Response(response="200", description="Logout successful"),
     *     @OA\Response(response="401", description="Unauthorized")
     * )
     */
    public function getUsersPrimaryLocationFireDangerRating()
    {
        $userSuburbID = Auth::user()["primary_location_suburb_id"];
        $userSuburbName = Suburb::where('id', '=', $userSuburbID)->get()->first();
        return Http::post($this->microserviceBaseEndpoint.'fire-danger-ratings', [
            'suburb' => $userSuburbName->name,
        ])->json();
    }
    /**
     * @OA\Get(
     *     path="/api/me/fire-danger-ratings",
     *     summary="Get FireDangerRating",
     *     tags={"FireDangerRating"},
     *     description="Get FireDangerRating",
     *     security={{"bearerAuth": {}}},
     *     @OA\Response(response="200", description="Get successful"),
     *     @OA\Response(response="401", description="Unauthorized")
     * )
     */
    public function getFireDangerRating(Request $request) {
        return Http::post($this->microserviceBaseEndpoint.'fire-danger-ratings', $request->all())->json();
    }
    /**
     * @OA\Get(
     *     path="/api/all/fire-danger-ratings",
     *     summary="Get FireDangerRating",
     *     tags={"FireDangerRating"},
     *     description="Get FireDangerRating",
     *     security={{"bearerAuth": {}}},
     *     @OA\Response(response="200", description="Get successful"),
     *     @OA\Response(response="401", description="Unauthorized")
     * )
     */
    public function getFireDangerRatings()
    {
        return Http::get($this->microserviceBaseEndpoint.'fire-danger-ratings/all', [])->json();
    }

}
