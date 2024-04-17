<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;
use App\Models\Suburb;
use App\Models\UserLocation;
use App\Notifications\FireWarningNotifier;
use Illuminate\Support\Facades\Log;
use Illumminate\Support\Facades\Notification;
use Illuminate\Support\Str;

class FireWarningNotifierController extends Controller
{
    /**
     * @param Suburb $affectedSuburbs
     * 
     * sends a notification to user's email if fire rating is 3 or higher
     */
    public function sendFireWarning(array $affectedSuburbs){
        // fetch the users ids from the affected suburbs then use those
        // to obtain the users.
        $affectedSuburbIds = array_map(function($suburb){
            return $suburb->id;
        }, $affectedSuburbs);

        // obtain the names of the suburbs, we'll need to send a list of suburbs for our notification.

        $userIds = [];
        foreach($affectedSuburbIds as $affectedSuburbId){
            $userLocations = UserLocation::where('suburb_id', $affectedSuburbId)->get();
            foreach($userLocations as $userLocation){
                $userIds[] = $userLocation->user_id;
            }
        }
        $users = User::whereIn('id', $userIds)->get();

        // now that we have the users we can then send a notification to these users
        $fireWarningData[
            'warning-content' => 'Fire rating of 3 or higher released for your area'
            'url' => 'for more information on bushfire preparation and response, head to https://www.dfes.wa.gov.au/ '
        ]
        
        // push the fireWarning notification data to the application. 
        // Notification::send($users, new FireWarningNotifier($fireWarningData));
    }
}
