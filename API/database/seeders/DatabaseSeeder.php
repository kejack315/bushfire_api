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
        $microserviceBaseEndpoint = config("DANGER_RATING_MICROSERVICE_ENDPOINT", "http://localhost:8000/");
        $allSuburbs = Http::get($microserviceBaseEndpoint."suburb-list");
        foreach($allSuburbs["suburbs"] as $key => $value) {
            Suburb::create([
                "id" => $key,
                "name" => $value
            ]);
        }
    }
}
