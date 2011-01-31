<!DOCTYPE html>

<html lang="en">
<head>
<meta name="viewport" content="initial-scale=1.0" user-scalable="no" />	
<link rel="stylesheet" href="style.css" />
<script src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script src="https://github.com/douglascrockford/JSON-js/raw/master/json2.js"></script>
<script src="js/jquery-1.4.4.min.js"></script>

<style type="text/css">
	html { height: 100% }
	body { height: 100%; margin: 0px; padding: 0px }
</style>
		
<script>

var map;
var infowindow;
var geocoder;
var markersArray= [];
var infowindows=[];
var eventdata;

var mit = new google.maps.LatLng(42.3584279, -71.0950);

var roadVintageStyles = [
  {
    featureType: "road.highway",
    elementType: "geometry",
    stylers: [
      { hue: "#882200" },
      { saturation: 60 },
      { lightness: 20 }
    ]
  },{
    featureType: "road.arterial",
    elementType: "all",
    stylers: [
      { hue: "#882200" },
      { visibility: "on" },
      { saturation: 30 },
      { lightness: 40 }
    ]
  },{
		featureType: "poi.school",
		elementType: "all",
		stylers: [
	        { hue: "#442200" },
	        { lightness: -50 },
	        { visibility: "simplified" },
	        { saturation: -50 }
		]
	},{
		featureType: "poi.park",
		elementType: "geometry",
		stylers: [
	        { lightness: -40 },
	        { visibility: "simplified" },
	        { saturation: -30 }
		]
	},{
		featureType: "poi.sports_complex",
		elementType: "geometry",
		stylers: [
	        { lightness: -40 },
	        { visibility: "simplified" },
	        { saturation: -80 }
		]
	},{
    featureType: "water",
    elementType: "geometry",
    stylers: [
      { hue: "#000055" },
      { saturation: -50 },
      { lightness: -50 }
    ]
  },{
    featureType: "road.highway",
    elementType: "labels",
    stylers: [
      { visibility: "off" },
      { saturation: 98 }
    ]
  },{
    featureType: "road.local",
    elementType: "geometry",
    stylers: [
      { hue: "#00ff00" },
      { saturation: 100 },
      { lightness: 20 }
    ]
  },{
    featureType: "road.local",
    elementType: "label",
    stylers: [
      { hue: "#ffaa00" },
      { saturation: 100 },
      { lightness: 0 }
    ]
  },
	{
    featureType: "landscape",
    elementType: "geometry",
    stylers: [
      { hue: "#882200" },
      { saturation: -50 },
      { lightness: -50 }
    ]
  },{
    featureType: "administrative.locality",
    elementType: "geometry",
    stylers: [
      { hue: "#9b6631" },
      { saturation: 50 },
      { lightness: -10 },
      { gamma: 0.90 }
    ]
  },{
    featureType: "transit.line",
    elementType: "geometry",
    stylers: [
      { hue: "#ff0000" },
      { visibility: "on" },
      { lightness: -70 }
    ]
  },{
    featureType: "all",
    elementType: "geometry",
    stylers: [
		{gamma:0.8}
    ]
  }
];

var mapOptions = {
  zoom: 16,
  center: mit,
  mapTypeControlOptions: {
     mapTypeIds: [ 'usrvintage' ,google.maps.MapTypeId.ROADMAP]
  }
};


var styledMapOptions = {
name: "Game Map"
};

var myType = new google.maps.StyledMapType(
  roadVintageStyles, styledMapOptions);


function getEventContent(eventEntry) {
  var event_id = eventEntry['event_id'];
  if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp=new XMLHttpRequest();
  }
  else
  {// code for IE6, IE5
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
  var url = "ajax/get_event_info_ajax.php?event_id=" + event_id;
  xmlhttp.open("GET",url,false);
  xmlhttp.send();
  xmlDoc=xmlhttp.responseText; 
  htmlText='<div class = "mmwrap">' + xmlDoc + '</div>';
  return htmlText;
}

function addEventMarker(iter) {
	eventEntry = eventdata[iter];
	var address = eventEntry['street_address'];
	console.log(address);
	(function(i, eventEntry) {
	geocoder.geocode({'address':address}, function(results, geoStatus) {
		if (geoStatus == google.maps.GeocoderStatus.OK) {
			map.setCenter(results[0].geometry.location);
			markersArray.push(new google.maps.Marker({
				map: map,
				position: results[0].geometry.location,
				draggable: false,
				animation: google.maps.Animation.DROP
			}));
		} else {
			alert("Couldn't find the address for the following reason: "+geoStatus);
		}
		console.log(eventEntry['event_name']);
		markersArray[i].setTitle(eventEntry['event_name']);
		
	//	var eventdescription= getEventContent(eventEntry);
//			{content:  eventdescription,
	//		 size: new google.maps.Size(100, 100)
		//	});
//		infowindows.push(infowindow);
		google.maps.event.addListener(markersArray[i], 'click', function() {
		//	map.setZoom(15);
		  infowindow.setContent(getEventContent(eventEntry));
		  infowindow.setPosition(markersArray[i].position);
			infowindow.open(map);

		});

	})
	})(iter, eventEntry);
}

function addEventMarkers(data) {
	eventdata=data;
	for (var i=0;i<eventdata.length;i++) {
		//setTimeout(function() {
			addEventMarker(i);
		//}, i*200);
	}		
}

function clearMarkers() {
	for (i in markersArray){
		markersArray[i].setMap(null);
	}
	markersArray.length=0;
}



function searchEvents() {
	console.log('enter search events');
	clearMarkers();
	var url = "ajax/get_user_event_ajax.php";
	var userID = parseInt($("#userID").val());
	var input = { 'user_id' : userID};
	console.log(input);
	console.log(url);
	$.post(url, input, addEventMarkers, "json");
}


function initialize() {
	geocoder = new google.maps.Geocoder();
	map = new google.maps.Map(document.getElementById("map_canvas"),
			mapOptions);
	map.mapTypes.set('usrvintage', myType);
	map.setMapTypeId('usrvintage');
  infowindow = new google.maps.InfoWindow({
        maxWidth: 400
  });
  
  forcedrop();
	<?php
	if(isset($_COOKIE['id']) ) {
	  echo "autodrop(".$_COOKIE['id'].");";
	  }?>
}

function forcedrop(){
autodrop(563);

}

function autodrop(user){
  console.log('enter search events');
  clearMarkers();
  var url = "ajax/get_user_event_ajax.php";
 var input = { 'user_id' : user};
  console.log(input);
  console.log(url);
  $.post(url, input, addEventMarkers, "json");
}

</script>
</head>
<body onload="initialize()">
	
			<div id="map_canvas"></div>

</body>
		
</html>

