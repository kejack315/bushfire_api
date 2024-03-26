<?php
namespace App\Traits;

trait ApiResponser
{
    protected function success($data, string $message = null)
    {
        return response()->json([
            'status' => 'Success',
            'message' => $message,
            'data' => $data
        ]);
    }

    protected function error(string $message = null, $data = null)
    {
        return response()->json([
            'status' => 'Error',
            'message' => $message,
            'data' => $data
        ]);
    }
}
