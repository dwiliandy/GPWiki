<?php

namespace App\Http\Controllers\Api;

use App\Models\Crew;
use App\Models\Place;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use App\Http\Controllers\Controller;

class PlaceController extends Controller
{
  public function index(Request $request)
  {

    // Ambil query params
    $page     = $request->query('page', 1);       // default page 1
    $perPage  = $request->query('per_page', 20); // default 20

    // Ambil filter dari query params
    $query = Place::query();
    // Pagination
    $places = $query->paginate($perPage, ['*'], 'page', $page);

    // Buat array string /kru_name_class
    $result = $places->map(function ($place) {
      return '/visit_' . $place->name;
    });

    return response()->json([
      'data' => $result,
      'current_page' => $places->currentPage(),
      'last_page' => $places->lastPage(),
      'total' => $places->total()
    ]);
  }

  public function store(Request $request)
  {
    $text = $request->raw_text;
    $allLocations = [];

    // Ambil semua /travel_XXX
    if (preg_match_all('/\/travel_([^\s]+)|🎰 ([^\s]+) \(lokasi saat ini\)/', $text, $matches, PREG_SET_ORDER)) {
      $allLocations = [];
      foreach ($matches as $m) {
        // cek group mana yang ketemu
        $allLocations[] = $m[1] ?: $m[2];
      }
    }
    foreach ($allLocations as $loc) {
      // Cek apakah lokasi sudah ada di DB
      $existing = Place::where('name', $loc)->first();
      if (!$existing) {
        $place = new Place();
        $place->name = $loc;
        $place->save();
        Log::info("Simpan lokasi baru: " . $loc);
      } else {
        Log::info("Lokasi sudah ada: " . $loc);
      }
    }
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
