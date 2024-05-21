<?php

namespace App\Http\Controllers;

use App\Models\Suburb;
use App\Models\UserLocation;
use App\Http\Requests\StoreUserLocationRequest;
use App\Http\Requests\UpdateUserLocationRequest;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;


class UserLocationController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        //
    }

    /**
     * Show the form for creating a new resource.
     */
    public function create()
    {
        //
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(StoreUserLocationRequest $request)
    {
        //
    }

    /**
     * Display the specified resource.
     */
    public function show(UserLocation $userLocation)
    {
        //
    }

    /**
     * Show the form for editing the specified resource.
     */
    /**
     * @OA\Get(
     *     path="/api/user-location",
     *     summary="Edit user location",
     *     tags={"UserLocationSuburb"},
     *     description="Edit user location page",
     *     security={{"bearerAuth": {}}},
     *     @OA\Response(response="200", description="Logout successful"),
     *     @OA\Response(response="401", description="Unauthorized")
     * )
     */
    public function edit()
    {
        $user = Auth::user();
        if ($user) {
            $userSuburbID = $user->primary_location_suburb_id;
            $userSuburbName = Suburb::where('id', '=', $userSuburbID)->value('name');

            return response()->json(['user' => $user, 'suburb_name' => $userSuburbName], 200);
        } else {
            return response()->json(['error' => 'Unauthorized'], 401);
        }
    }

    /**
     * Update the specified resource in storage.
     */
    /**
     * @OA\Put(
     *     path="/api/user-location/update",
     *     summary="Update user location",
     *     tags={"UserLocationSuburb"},
     *     description="Update user location",
     *     security={{"bearerAuth": {}}},
     *     @OA\Parameter(
     *         name="suburb",
     *         in="query",
     *         description="User's suburb",
     *         required=true,
     *         @OA\Schema(type="string")
     *     ),
     *     @OA\Response(response="200", description="Update successful"),
     *     @OA\Response(response="401", description="Unauthorized")
     * )
     */
    public function update(Request $request)
    {
        $user = Auth::user();

        if ($user) {
            $request->validate([
                'suburb' => 'required|exists:suburbs,name',
            ]);

            $suburbName = $request->input('suburb');
            $suburb = Suburb::where('name', $suburbName)->first();

            $user->primary_location_suburb_id = $suburb->id;
            $user->save();

            return response()->json(['message' => 'Primary suburb updated successfully', 'suburb_name' => $suburbName], 200);
        } else {
            return response()->json(['error' => 'Unauthorized'], 401);
        }
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(UserLocation $userLocation)
    {
        //
    }
}
