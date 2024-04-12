<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Http;
use App\Models\Suburb;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the suburbs with response from microservice
     */
    public function run(): void
    {
        # TODO: Store microservice endpoint in .env file...
        $allSuburbs = Http::get('http://localhost:8000/suburb-list');
        foreach($allSuburbs["suburbs"] as $key => $value) {
            $newSuburb = Suburb::create([
                "id" => $key,
                "name" => $value
            ]);
        }

    }
}
