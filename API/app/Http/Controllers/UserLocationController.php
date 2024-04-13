<?php

namespace App\Http\Controllers;

use App\Models\UserLocation;
use App\Http\Requests\StoreUserLocationRequest;
use App\Http\Requests\UpdateUserLocationRequest;

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
    public function edit(UserLocation $userLocation)
    {
        $user = auth()->user();

        if ($user) {
            return response()->json(['user' => $user], 200);
        } else {
            return response()->json(['error' => 'Unauthorized'], 401);
        }
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(UpdateUserLocationRequest $request, UserLocation $userLocation)
    {
        $user = auth()->user();


        if ($user) {
            $user->suburb = $request->input('suburb');
            $user->save();

            return response()->json(['message' => 'User location updated successfully'], 200);
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
