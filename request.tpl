<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
<title>Google Maps JavaScript API v3 Example: Event Closure</title>
<link href="http://code.google.com/apis/maps/documentation/javascript/examples/default.css" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="http://code.jquery.com/jquery-1.4.4.min.js"> </script>
<script type ="text/javascript" src="http://code.google.com/apis/gears/gears_init.js"> </script>
<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script type="text/javascript">
var map;
var endMarker;
//var initialLocation;
var browserSupportFlag =  new Boolean();
var siberia = new google.maps.LatLng(60, 105);
var newyork = new google.maps.LatLng(40.69847032728747, -73.9514422416687);


function initialize() {
  var mit = new google.maps.LatLng(42.3584279, -71.0950);
  var myOptions = {
    zoom: 14,
    center: mit,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  }
  map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

  
  var initialLocation;
  console.log('start');
  
  
// Try W3C Geolocation (Preferred)
  if(navigator.geolocation) {
    browserSupportFlag = true;
    navigator.geolocation.getCurrentPosition(function(position) {
      initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
      map.setCenter(initialLocation);
      placeStartMarker(initialLocation);
  	console.log("dsfafd"+initialLocation);
    $.get('tasks',{lat:intialLocation.lat,lng:intialLocation.lng},function(data){
            $('html').html(data);
        })
    }, function() {
      handleNoGeolocation(browserSupportFlag);
    });
  // Try Google Gears Geolocation
  } else if (google.gears) {
    browserSupportFlag = true;
    var geo = google.gears.factory.create('beta.geolocation');
    geo.getCurrentPosition(function(position) {
      initialLocation = new google.maps.LatLng(position.latitude,position.longitude);
      map.setCenter(initialLocation);
    }, function() {
      handleNoGeoLocation(browserSupportFlag);
    });
  // Browser doesn't support Geolocation
  } else {
    browserSupportFlag = false;
    handleNoGeolocation(browserSupportFlag);
  }
  
  
  console.log('ends');
    
  google.maps.event.addListener(map, 'click', function(event) {
  placeEndMarker(event.latLng);
  });
   
}



  
function placeStartMarker(location) {
  console.log("startLoc");
  
 // $.get('submit_location',{'lat': location.lat(), 'long':location.long()});


  startMarker = new google.maps.Marker({
      position: location, 
      map: map,
      draggable : true,
      title:"My location",
      icon : "http://www.google.com/intl/en_us/mapfiles/ms/micons/green-dot.png"
  });
  
}

function placeEndMarker(location) {
	
  var clickedLocation = new google.maps.LatLng(location);
  console.log("endloc");
  

  if(endMarker != null){
  	endMarker.setMap(null);
  }	
  endMarker = new google.maps.Marker({
      position: location, 
      map: map,
      draggable : true,
      title:"Location of Task!"

  });
  
}

  function handleNoGeolocation(errorFlag) {
    if (errorFlag == true) {
      alert("Geolocation service failed.");
      initialLocation = newyork;
    } else {
      alert("Your browser doesn't support geolocation. We've placed you in Siberia.");
      initialLocation = siberia;
    }
    map.setCenter(initialLocation);
  }

function send(){

	console.log(document.getElementById("txt1").value);

	if(document.getElementById("txt1").value == "" ){
		alert("you must enter a description for the delivery");
		return;
	}
	if(startMarker == null){
		alert("you must first allow us to see your location");
		return;
	}
	else if (endMarker == null){
		alert("specify the task location");
		return;
	} else{
		console.log("sending lat and lng" );
		console.log("start:  " + startMarker.position);
		console.log("end:  " + endMarker.position);
		console.log("end:  " + endMarker.position.lat());
		console.log("end:  " + endMarker.position.lng());
    	$.get("/submit_location",{
   			start_lat: startMarker.position.lat(),
       		start_long: startMarker.position.lng(),
        	end_lat: endMarker.position.lat(),
        	end_long: endMarker.position.lng(),
        	description: document.getElementById("txt1").value
    	})
	}
}

</script>
<style>
#map_canvas{
height:500px;
width:500px;
}
#txt1{
height:10px;
width:200px;
}

</style>


</head>
<body onload="initialize()">
  <div id="map_canvas"></div>
 
  <div> 
  Description of Delivery: <input type = "text" id = "txt1">  </input>
  </div>
  
  <div>
	<input type= "button" value = "submit" onClick = "send()"/> 
 </div>



</body>
</html>
