<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\CrewController;
use App\Http\Controllers\Api\PlaceController;

// KRU
Route::get('/crews', [CrewController::class, 'index']);
Route::post('/crews', [CrewController::class, 'store']);
Route::get('/crews/{id}', [CrewController::class, 'show']);

// PLACE
Route::get('/places', [PlaceController::class, 'index']);
Route::post('/places', [PlaceController::class, 'store']);
