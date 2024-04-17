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
    /**
     * @OA\Post(
     *     path="/api/register",
     *     summary="Register a new user",
     *     tags={"Authentication"},
     *     @OA\Parameter(
     *         name="name",
     *         in="query",
     *         description="User's name",
     *         required=true,
     *         @OA\Schema(type="string")
     *     ),
     *     @OA\Parameter(
     *         name="email",
     *         in="query",
     *         description="User's email",
     *         required=true,
     *         @OA\Schema(type="string")
     *     ),
     *     @OA\Parameter(
     *         name="password",
     *         in="query",
     *         description="User's password",
     *         required=true,
     *         @OA\Schema(type="string")
     *     ),
     *     @OA\Parameter(
     *         name="confirm_password",
     *         in="query",
     *         description="confirm User's password",
     *         required=true,
     *         @OA\Schema(type="string")
     *     ),
     *     @OA\Parameter(
     *         name="suburb",
     *         in="query",
     *         description="User's suburb",
     *         required=true,
     *         @OA\Schema(type="string")
     *     ),
     *     @OA\Response(response="201", description="User registered successfully"),
     *     @OA\Response(response="422", description="Validation errors")
     * )
     */
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

    /**
     * @OA\Post(
     *     path="/api/login",
     *     summary="Authenticate user and generate JWT token",
     *     tags={"Authentication"},
     *     @OA\Parameter(
     *         name="email",
     *         in="query",
     *         description="User's email",
     *         required=true,
     *         @OA\Schema(type="string")
     *     ),
     *     @OA\Parameter(
     *         name="password",
     *         in="query",
     *         description="User's password",
     *         required=true,
     *         @OA\Schema(type="string")
     *     ),
     *     @OA\Response(response="200", description="Login successful"),
     *     @OA\Response(response="401", description="Invalid credentials")
     * )
     */
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

    /**
     * @OA\Get(
     *     path="/api/logout",
     *     summary="Log out current user",
     *     tags={"Authentication"},
     *     description="Log out the currently authenticated user and invalidate the JWT token",
     *     security={{"bearerAuth": {}}},
     *     @OA\Response(response="200", description="Logout successful"),
     *     @OA\Response(response="401", description="Unauthorized")
     * )
     */
    public function logout()
    {
        auth()->user()->tokens()->delete();

        return response()->json([
            'message' => 'Logout successfully!!'
        ]);
    }
}
