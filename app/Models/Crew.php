<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class Crew extends Model
{
  use HasFactory;

  protected $fillable = [
    'name',
    'type',
    'type_emoji',
    'class',
    'atk',
    'def',
    'hp',
    'speed'
  ];
}
