from apiclient.discovery import build
import webapp2
import json

DEVELOPER_KEY = "AIzaSyBLFaS5nuS6vOadTeIaKzVukphHxBQh6yY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
CHANNEL_ID = "UCvS6-K6Ydmb4gH-kim3AmjA"
MAX_RESULTS = 25
SEARCH_PART = "id,snippet"
SEARCH_TYPE = "video"

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        self.response.out.write('<html>')
        self.response.out.write('<head>')
        self.response.out.write('<title>AngularJS Tutorial</title>')
        self.response.out.write('<script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.6.4/angular.min.js"></script>')
        self.response.out.write("""<script>
var app = angular.module('myApp', []);
app.controller('MainController', 
    function($scope, $http, $timeout) {
        $scope.searchText = null;
        $scope.listtitle = "Videos disponibles";
        $http.get('/videos').then( function(result){$scope.videos = result.data.videos;} );
        $scope.change = function(text) {
            valtosend = $scope.searchText;
            $http.get('/videos?q='+valtosend).then( function(result){
               $scope.videos = result.data.videos;
               $scope.listtitle = "Resultados de la busqueda";
            } );
        }
    }
);
</script>""")
        self.response.out.write('</head>')
        self.response.out.write('<body>')
        self.response.out.write('<h1>Resarch test - Gerson Lara</h1>')
        self.response.out.write("""<div ng-app="myApp" ng-controller="MainController"> 
<input type="text" ng-model="searchText" ng-change="change(text)" placeholder="Texto a buscar..." /><span>{{searchText}}</span>
<h2>{{listtitle}}:</h2>
<li ng-repeat="video in videos">
<span class="{{video.title}}"><a href="https://www.youtube.com/watch?v={{video.id}}"><img src="{{video.thumbnail.url}}">{{video.title}}</a><br>{{video.description}}</span>
</li>
Videosearch: <p ng-bind="videosearch"></p>
</div>""")
        self.response.out.write('</body>')
        self.response.out.write('</html>')

class VideoList(webapp2.RequestHandler):
    def get(self):
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
            #self.response.out.write(search_result["snippet"]["title"] + '\r\n')
            search_videos.append(
               {"videoId":search_result["id"]["videoId"],
               "title":search_result["snippet"]["title"],
               "description":search_result["snippet"]["description"],
               "thumbnail":search_result["snippet"]["thumbnails"]["default"]
               }
            )
        response = {"videos":search_videos}
        self.response.out.write( json.dumps(response) )
        
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/videos', VideoList)
], debug=True)