<?php

namespace App\Http\Controllers\Api;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use App\Http\Controllers\Controller;

class ItemController extends Controller
{
  public function index(Request $request) {}

  public function store(Request $request)
  {
    $text = $request->raw_text;

    return response()->json([
      'status' => 'success',
      'message' => 'Tempat berhasil disimpan'
    ], 201);
  }

  public function show($data)
  {
    // Misal $data = "Bill_S"
    // Pisahkan name dan class
    $parts = explode('_', $data, 3);
    $name = $parts[1] ?? null;
    $class = $parts[2] ?? null;
    if (!$name || !$class) {
      return response()->json([
        'status' => 'error',
        'message' => 'Format data tidak valid'
      ], 400);
    }

    $crew = Crew::where('name', $name)
      ->where('class', $class)
      ->first();

    if (!$crew) {
      return response()->json([
        'status' => 'error',
        'message' => 'Crew tidak ditemukan'
      ], 404);
    }

    return response()->json([
      'status' => 'success',
      'data' => $crew
    ]);
  }

  public function update(Request $request, string $id)
  {
    //
  }

  public function destroy(string $id)
  {
    //
  }
}
