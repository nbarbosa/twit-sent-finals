'use strict';
angular.module('clientApp')
  .controller('MainCtrl', function ($scope, $http, $rootScope, $timeout, $window) {
 	$scope.tweets = [];
 	$rootScope.total = $scope.tweets.length;

  	$scope.newTweets = [];

 	$scope.refresh = function () {
	 		for (var i = 0; i < $scope.newTweets.length; i++) {
	 			console.log($scope.newTweets[i]);	
	 			$scope.tweets.unshift($scope.newTweets[i]);
	 		}
	 		$scope.newTweets = []
 	};

 	$scope.scrollTweets = function () {
		if ($scope.tweets.length == 0 || $scope.busy) return;
		$scope.loadTweets()
 	};

 	$scope.loadStats = function () {
 		$http({
		  method: 'GET',
		  url: 'http://twtsentfinals-server.natabarbosa.com/stats'
		}).then(function successCallback(response) {	
		    $rootScope.positiveCount = response.data.positive;
		    $rootScope.negativeCount = response.data.negative;
		    $rootScope.hasLoadedStats = true;
		  }, function errorCallback(response) {
		    console.log(response);
		  });
 	};
  	$scope.loadTweets = function (when, cb) {
		$scope.busy = true;  		
  		when = when || 'before';
  		var ts = ''

  		if ($scope.tweets.length > 0) {
  			if (when == 'before') {
  				ts = $scope.tweets[$scope.tweets.length - 1].ts_created;
  			} else {
  				if ($scope.newTweets.length == 0) {
  					ts = $scope.tweets[0].ts_created;
  				} else {
  					ts = $scope.newTweets[$scope.newTweets.length - 1].ts_created
  				}
  			}
  		}

  	    $http({
		  method: 'GET',
		  url: 'http://twtsentfinals-server.natabarbosa.com/tweets?ts=' + ts + '&when=' + when
		}).then(function successCallback(response) {	

		    	for (var i = 0; i < response.data.length; i++) {
		    		if (when == 'before') {
		    			$scope.tweets.push(response.data[i])
		    		} else {
		    			if ($window.scrollY == 0 && $scope.newTweets.length == 0) {
		    				$scope.tweets.unshift(response.data[i]);		    
		    			} else {
		    				$scope.newTweets.push(response.data[i]);
		    			}
					}
				}
		    $rootScope.total = $scope.tweets.length;
		    cb()
		    $scope.busy = false;
		  }, function errorCallback(response) {
		  	console.log(response);
		  });	
  	};

  	$scope.loadTweets();

  	(function tick() {
  		$scope.loadStats();
        $scope.loadTweets('after', function (){
        	$timeout(tick, 3000);
        });
    })();

    
  });
