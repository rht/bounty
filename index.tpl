<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
<title>Google Maps JavaScript API v3 Example: Event Closure</title>
<link href="http://code.google.com/apis/maps/documentation/javascript/examples/default.css" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="http://code.jquery.com/jquery-1.4.4.min.js"> </script>

<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script type="text/javascript">
var map;
var startMarker;
var endMarker;
var b= true;
function initialize() {
  var mit = new google.maps.LatLng(42.3584279, -71.0950);
  var myOptions = {
    zoom: 14,
    center: mit,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  }
  map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
 
  
  
  google.maps.event.addListener(map, 'click', function(event) {
    if($('#myloc').attr('checked')){ 
    	placeStartMarker(event.latLng);
    } else{
    	placeEndMarker(event.latLng);
    }
  });
}
  
function placeStartMarker(location) {
  var clickedLocation = new google.maps.LatLng(location);
  console.log(location.lat());
console.log($('#myloc').attr('checked'));
  console.log("startLoc");
  
 // $.get('submit_location',{'lat': location.lat(), 'long':location.long()});
  if(startMarker != null){
  	startMarker.setMap(null);
  }	

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
  console.log(location.lat());
  console.log("endloc");
  
console.log($('#myloc').attr('checked'));

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


function send(){
	if(startMarker.position != null  && endMarker.position != null){
		  console.log("sending lat and lng" );
		  console.log("start:  " + startMarker.position);
		  console.log("end:  " + endMarker.position);
		  console.log("end:  " + endMarker.position.lat());
		  console.log("end:  " + endMarker.position.lng());
          $.get("/submit_location",{
              start_lat: startMarker.position.lat(),
              start_long: startMarker.position.lng(),
              end_lat: endMarker.position.lat(),
              end_long: endMarker.position.lng()
              })
	}
}

</script>
<style>
#map_canvas{
height:500px;
width:500px;
}

</style>


</head>
<body onload="initialize()">
  <div id="map_canvas"></div>
 
  
  <div>
  	<label for="male">Where I am</label>
  	<input type="radio" name="loc" id="myloc" CHECKED= true />
  	<br />
  	<label for="female">Where the Food is</label>
  	<input type="radio" name="loc" id="food"/>

	<input type= "button" value = "submit" onClick = "send()"/> 
 </div>



</body>
</html>
