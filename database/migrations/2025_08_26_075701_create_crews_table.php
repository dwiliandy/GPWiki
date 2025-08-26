<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
  /**
   * Run the migrations.
   */
  public function up(): void
  {
    Schema::create('crews', function (Blueprint $table) {
      $table->id();
      $table->string('name');
      $table->string('type');
      $table->string('type_emoji')->nullable();
      $table->string('class');
      $table->integer('atk');
      $table->integer('def');
      $table->integer('hp');
      $table->integer('speed');
      $table->timestamps();
    });
  }

  /**
   * Reverse the migrations.
   */
  public function down(): void
  {
    Schema::dropIfExists('crews');
  }
};
