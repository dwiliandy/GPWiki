<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\CrewController;

Route::get('/crews', [CrewController::class, 'index']);
Route::post('/crews', [CrewController::class, 'store']);
Route::get('/crew/{id}', [CrewController::class, 'show']);
