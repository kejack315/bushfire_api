<?php

namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use App\Models\UserLocation;
use Illuminate\Http\Request;

class UserLocationController extends Controller
{
    public function create(Request $request)
    {
        $request->validate([
            'user_id' => 'required|exists:users,id',
            'suburb_id' => 'required|exists:suburbs,id',
            'last_seen' => 'required|date',
        ]);

        $userLocation = UserLocation::create([
            'user_id' => $request->user_id,
            'suburb_id' => $request->suburb_id,
            'last_seen' => $request->last_seen,
        ]);

        return response()->json(['message' => 'User location created successfully', 'user_location' => $userLocation], 201);
    }

    public function delete($id)
    {
        $userLocation = UserLocation::find($id);

        if (!$userLocation) {
            return response()->json(['message' => 'User location not found'], 404);
        }

        $userLocation->delete();

        return response()->json(['message' => 'User location deleted successfully'], 200);
    }
}
