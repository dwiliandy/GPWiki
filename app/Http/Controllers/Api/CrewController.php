<?php

namespace App\Http\Controllers\Api;

use App\Models\Crew;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use App\Http\Controllers\Controller;

class CrewController extends Controller
{
  public function index(Request $request)
  {

    // Ambil query params
    $page     = $request->query('page', 1);       // default page 1
    $perPage  = $request->query('per_page', 20); // default 20
    $sortBy   = $request->query('sort_by', 'name'); // default sort by name
    $order    = $request->query('order', 'asc'); // default ascending

    // Ambil filter dari query params
    $query = Crew::query();

    // Contoh filter: type dan class
    if ($request->has('type')) {
      $query->where('type', $request->query('type'));
    }
    if ($request->has('class')) {
      $query->where('class', $request->query('class'));
    }

    // Sorting
    $query->orderBy($sortBy, $order);

    // Pagination
    $crews = $query->paginate($perPage, ['*'], 'page', $page);

    // Buat array string /kru_name_class
    $result = $crews->map(function ($crew) {
      return '/kru_' . $crew->name . '_' . $crew->class;
    });

    return response()->json([
      'data' => $result,
      'current_page' => $crews->currentPage(),
      'last_page' => $crews->lastPage(),
      'total' => $crews->total()
    ]);
  }

  public function store(Request $request)
  {
    $text = $request->raw_text;
    if (preg_match('/📖 Level:\s*(\d+)/u', $text, $matches)) {
      $level = (int) $matches[1]; // Ambil angka level dan konversi ke integer
      log::info("Level kru: " . $level);
      if ($level !== 1) {
        return response()->json([
          'status' => 'error',
          'message' => 'Kru yang dikirim bukan level 1'
        ], 400);
      } else {
        // ----------------- Ambil Nama Kru -----------------
        if (preg_match('/^(.)(.*?)\[(.*?)\]/um', $text, $matches_name)) {
          $emoji_type = $matches_name[1];
          $name = $matches_name[2];
          $name = preg_replace('/[\x{200B}-\x{200F}\x{202A}-\x{202E}\x{2060}-\x{206F}\x{FE0F}]/u', '', $name);
          $name = trim($name);
        }

        // ----------------- Ambil Type -----------------
        preg_match('/📖 Type:\s*(.+)/u', $text, $matches_type);
        $type = $matches_type[1] ?? null;

        // ----------------- Ambil Class -----------------
        preg_match('/📖 Class:\s*(\w+)/u', $text, $matches_class);
        $class = $matches_class[1] ?? null;

        // ----------------- Ambil Level -----------------
        preg_match('/📖 Level:\s*(\d+)/u', $text, $matches_level);
        $level = isset($matches_level[1]) ? (int)$matches_level[1] : null;

        // ----------------- Ambil Tier -----------------
        preg_match('/📖 Tier:\s*(\w+)/u', $text, $matches_tier);
        $tier = $matches_tier[1] ?? null;

        // ----------------- Ambil Stats -----------------
        preg_match('/➕ ATK:\s*([\d,]+)/u', $text, $matches_atk);
        preg_match('/➕ DEF:\s*([\d,]+)/u', $text, $matches_def);
        preg_match('/➕ HP:\s*([\d,]+)/u', $text, $matches_hp);
        preg_match('/➕ SPEED:\s*([\d,]+)/u', $text, $matches_speed);

        $atk = isset($matches_atk[1]) ? (int) str_replace(',', '', $matches_atk[1]) : null;
        $def = isset($matches_def[1]) ? (int) str_replace(',', '', $matches_def[1]) : null;
        $hp = isset($matches_hp[1]) ? (int) str_replace(',', '', $matches_hp[1]) : null;
        $speed = isset($matches_speed[1]) ? (int) str_replace(',', '', $matches_speed[1]) : null;
        $checkData = Crew::where('name', $name)->where('class', $class)->count();
        if ($checkData == 0) {
          Crew::create([
            'name' => $name,
            'type' => $type,
            'type_emoji' => $emoji_type,
            'class' => $class,
            'atk' => $atk,
            'def' => $def,
            'hp' => $hp,
            'speed' => $speed
          ]);
          return response()->json([
            'status' => 'success',
            'message' => 'Kru level 1 berhasil disimpan'
          ], 201);
        } else {
          return response()->json([
            'status' => 'error',
            'message' => 'Kru sudah ada di database'
          ], 400);
        }
      }
    } else {
      return response()->json([
        'status' => 'error',
        'message' => 'Data Tidak Valid'
      ], 400); // <-- HTTP 400
    }
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
