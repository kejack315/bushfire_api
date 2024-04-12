<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use App\Models\UserLocation;

class Suburb extends Model
{
    use HasFactory;
    public function userLocations()
    {
        return $this->hasMany(UserLocation::class);
    }
}
