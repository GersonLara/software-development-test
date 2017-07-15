####################################################################################
# sdt0714gersonlara.py
# Author: Gerson Jahaziel Lara Bertrand.        Date: 2017-07-14
# Response to Software development test
# This file provides functionality to list the videos of Laureate's Youtube Channel
# A simple search is implemented through use of youtube search API
# The user only needs to type the search term in the text box provided.
# The page automatically updates the list with seach results
# Dynamic list display is achieved by using AngularJS
# CSS styling has been left out due to time restrictions.
####################################################################################
from apiclient.discovery import build
import webapp2
import json

DEVELOPER_KEY = "AIzaSyCmkTeSrIyiPXlLtlR19QsGMHgCzyxatIQ"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
CHANNEL_ID = "UCvS6-K6Ydmb4gH-kim3AmjA"  # Channel ID should be selected from a list or a parameter storage.
MAX_RESULTS = 25              # The API provides means for result pagination. Pagination use has not been implemented in this file.
SEARCH_PART = "id,snippet"
SEARCH_TYPE = "video"

class MainPage(webapp2.RequestHandler):
    def get(self):
        """Handles main page, particularly the implementation of search. Sends the search text so it is handled by the youtube search API."""
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        self.response.out.write('<html>')
        self.response.out.write('<head>')
        self.response.out.write('<title>Software Development Test - Gerson Lara - 0714</title>')
        self.response.out.write('<script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.6.4/angular.min.js"></script>')
        self.response.out.write("""<script>
var app = angular.module('myApp', []);
app.controller('MainController', 
    function($scope, $http, $timeout) {
        $scope.searchText = null;
        $scope.listtitle = "Available videos";
        $http.get('/videos').then( function(result){$scope.videos = result.data.videos;} );
        $scope.change = function(text) {
            valtosend = $scope.searchText;
            $http.get('/videos?q='+valtosend).then( function(result){
               $scope.videos = result.data.videos;
               $scope.listtitle = "Search results (" + result.data.total_results + ")";
            } );
        }
    }
);
</script>""")
        self.response.out.write('</head>')
        self.response.out.write('<body>')
        self.response.out.write('<h1>Software Development Test - Gerson Lara - 0714</h1>')
        self.response.out.write("""<div ng-app="myApp" ng-controller="MainController"> 
<input type="text" ng-model="searchText" ng-change="change(text)" placeholder="Video search text..." />
<h2>{{listtitle}}:</h2>
<li ng-repeat="video in videos">
<span class="{{video.title}}"><a href="https://www.youtube.com/watch?v={{video.id}}"><img src="{{video.thumbnail.url}}">{{video.title}}</a><br>{{video.description}}</span>
</li>
</div>""")
        self.response.out.write('</body>')
        self.response.out.write('</html>')

class VideoList(webapp2.RequestHandler):
    def get(self):
        """Performs a call to youtube search API."""
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
        params = {"part": SEARCH_PART,
           "type": SEARCH_TYPE,
           "channelId":CHANNEL_ID,
           "maxResults":MAX_RESULTS}
        searchText = self.request.get('q')
        if ( searchText != "" ):
           params["q"] = searchText
        search_response = youtube.search().list(**params).execute()
        
        search_videos = []
        for search_result in search_response.get("items", []):            
            search_videos.append(
               {"thumbnail":search_result["snippet"]["thumbnails"]["default"],
               "description":search_result["snippet"]["description"],
               "title":search_result["snippet"]["title"],
               "videoId":search_result["id"]["videoId"]
               }
            )
        page_info = search_response.get("pageInfo")
        response = {"videos":search_videos,"total_results":page_info["totalResults"]}
        self.response.out.write( json.dumps(response) )
        
# Define which class handles each URL
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/videos', VideoList)
], debug=True)