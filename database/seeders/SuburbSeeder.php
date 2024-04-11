<?php

namespace Database\Seeders;

use App\Models\Suburb;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class SuburbSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run()
    {
        $suburbs = [
            ['name' => 'Perth'],
            ['name' => 'Morly'],
            ['name' => 'Bayswater'],
        ];

        // 将数据插入数据库
        foreach ($suburbs as $suburb) {
            Suburb::create($suburb);
        }
    }
}
