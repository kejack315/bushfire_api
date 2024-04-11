<?php

use App\Http\Controllers\API\UserLocationController;
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

//
//Route::controller(AuthController::class)->group(function () {
//    Route::post('/register', 'register');
//    Route::post('/login', 'login')->name('login');
//    Route::get('/logout', 'logout');
//});
Route::post('/register', [AuthController::class, 'register']);
Route::post('/login', [AuthController::class, 'login'])->name('login');

Route::middleware(['auth:sanctum'])->group(function () {
    Route::controller(AuthController::class)->group(function () {
        Route::get('/logout', 'logout');
    });
});

Route::middleware(['auth:sanctum'])->group(function () {
    Route::post('/user-locations', [UserLocationController::class, 'create']);
    Route::delete('/user-locations/{id}', [UserLocationController::class, 'delete']);
});
