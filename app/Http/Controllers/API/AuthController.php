<?php
namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use App\Models\Suburb;
use App\Models\User;
use App\Traits\ApiResponser;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Facades\Auth;

class AuthController extends Controller
{
    use ApiResponser;

    public function register(Request $request)
    {
        $request->validate([
            'name' => 'required|string|max:50',
            'email' => 'required|string|email|unique:users,email',
            'password' => 'required|string|min:6',
            'confirm_password' => 'required_with:password|string|min:6|same:password',
            'suburb' => 'required|string|max:50'
        ]);

        $suburb = Suburb::where('name', $request->suburb)->first();

        if (!$suburb) {
            return response()->json(['error' => 'Suburb not found'], 404);
        }

        $user = User::create([
            'name' => $request->name,
            'password' => bcrypt($request->password),
            'email' => $request->email,
            'primary_location_suburb_id' => $suburb->id
        ]);

        return $this->success([
            'token' => $user->createToken('API Token')->plainTextToken
        ], 'User registration successful!!');
    }

    public function login(Request $request)
    {
        $attr = $request->validate([
            'email' => 'required|string|email|',
            'password' => 'required|string|min:6'
        ]);

        if (! Auth::attempt($attr)) {

            return $this->error('Credentials did\'t not matched');
        }

        return $this->success([
            'token' => auth()->user()->createToken('API Token')->plainTextToken
        ], 'Login successfulY');
    }

    public function users()
    {
        $users = User::select('name', 'email')->get();

        return $this->success([
            'users' => $users
        ], 'User list featched successfully!!');
    }

    public function logout()
    {
        auth()->user()->tokens()->delete();

        return response()->json([
            'message' => 'Logout successfully!!'
        ]);
    }
}
