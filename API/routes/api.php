<?php

use App\Http\Controllers\FireDangerRatingController;
use App\Http\Controllers\UserLocationController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\API\AuthController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/


Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

Route::post('/register', [AuthController::class, 'register']);
Route::post('/login', [AuthController::class, 'login'])->name('login');

Route::middleware(['auth:sanctum'])->group(function () {
    Route::controller(AuthController::class)->group(function () {
        Route::get('/logout', 'logout');
    });
    Route::post('/fire-danger-ratings', [FireDangerRatingController::class,
        'getFireDangerRating'])->name('fire-danger-rating.show');
    Route::get('/me/fire-danger-ratings', [FireDangerRatingController::class,
        'getUsersPrimaryLocationFireDangerRating'])->name('fire-danger-rating.me.show');
    Route::get('/all/fire-danger-ratings', [FireDangerRatingController::class,
        'getFireDangerRatings'])->name('fire-danger-rating.all');
});
Route::middleware(['auth:sanctum'])->group(function () {
    Route::put('/user-location/update', [UserLocationController::class, 'update']);
    Route::get('/user-location', [UserLocationController::class, 'edit']);
});
