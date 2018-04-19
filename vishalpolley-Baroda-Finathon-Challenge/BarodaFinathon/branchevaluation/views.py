# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
	AllowAny,
	)
from sklearn.cluster import DBSCAN, KMeans
from django.http import HttpResponse
from math import pi, sqrt, fabs
import numpy as np
import googlemaps
import requests
import json
import time

# New Branch Evaluation API
# Stacks Used : Django v1.11, Django REST Framework, Scikit-Learn, Numpy, Google Maps Geocoding, Reverse Geocoding, Places API, Python v2.7.12.
# Go to http://localhost:8000/api/branch/ to run the API
# Make a POST request as {"city": "city_name"} to fetch the results

class BranchEvaluationAPI(APIView):
	permission_class = (AllowAny,)

	def get(self, request, format=None):
		return Response("Baroda Finathon Challenge : New Branch Evaluation and Tender Filling API (The Capitalists)")

	def post(self, request, format=None):
		city = request.data.get('city')
		city = str(city)
		city = str.title(city)

		radius = 35000
		jdata = json.loads(open ('district.json').read())
		for i in jdata:
			if i['district'] == city:
				area = i['area']
				area = int(area.replace(',', ''))
				radius = int(sqrt(area / pi))*1000

		data=[]
		s=0
		cnt=0
		number=[0]*6
		gmaps = googlemaps.Client(key='AIzaSyDPLRH4a8cunU3eRt67BNss90ej_VdYSVk')
		geocode_result = gmaps.geocode(city)
		location = geocode_result[0]['geometry']['location']
		latlng = (location['lat'], location['lng'])

		# Collecting data from various places with the help of Google Maps Places API
		places = ['post_office', 'hospital', 'bank', 'bus_station', 'atm', 'school']
		for i in places:
			d = {'location': latlng, 'radius': radius, 'type': i}
			places_result  = gmaps.places_nearby(**d)	
			for x in places_result.get("results"):
				data.append((x.get("geometry").get("location").get("lat"),x.get("geometry").get("location").get("lng")))
			token = places_result.get("next_page_token")
			while token:
				time.sleep(2)
				d['page_token'] = token
				places_result = gmaps.places_nearby(**d)
				for x in places_result.get("results"):
					data.append((x.get("geometry").get("location").get("lat"),x.get("geometry").get("location").get("lng")))
				token = places_result.get("next_page_token")
			number[cnt]=len(data)-s
			s += number[cnt]
			cnt+=1

		# Applying DBSCAN Algorithm over the collected coordinates points to detect the number of clusters formed
		kms_per_radian = 6371.0088
		epsilon = 1.15 / kms_per_radian
		db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(data))
		core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
		core_samples_mask[db.core_sample_indices_] = True
		labels = db.labels_
		n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
		print (n_clusters_)

		# Applying KMeans Algorithm over the points to find out centroid points
		kmeans = KMeans(n_clusters=n_clusters_)
		kmeans.fit(data)
		labels = kmeans.labels_
		centroids = kmeans.cluster_centers_.tolist()
		centroids = [[round(x,7) for x in y] for y in centroids]
		print (len(centroids))
		print (centroids)

		# Getting Banks location from Bank of Baroda City Wise Search API
		api_search = requests.post("http://104.211.176.248:8080/bob/bobuat/api/CitywiseSearch", headers={"apikey":"Kf1L7J1jQ0dFasC","content-type":"application/json"}, json={"city":city}).json()
		api_data = []
		for x in api_search:
			api_data.append([x.get("latitude"),x.get("longitude")])
		print (len(api_data))
		print (api_data)

		# Subtracting Nearby banks locations from the clustering data
		tempList=[]
		for x in centroids:
			add=True
			for y in api_data:
				if fabs(x[0]-y[0])< 0.02 and fabs(x[1]-y[1])<0.02:
					add = False
					break
			if add:
				tempList.append(x)
		result = [x for x in tempList if x not in api_data]
		print (len(result))
		print (result)

		# Output Code

		output='''
		<!DOCTYPE html>
		<html> 
		<head> 
		  <meta http-equiv="content-type" content="text/html; charset=UTF-8"> 
		  <title>Branch Evaluation Api – Django REST framework</title> 
		  <script src="http://maps.google.com/maps/api/js?key=AIzaSyDPLRH4a8cunU3eRt67BNss90ej_VdYSVk&sensor=false"></script>
		</head> 
		<style>
	    #info
		{
		  position: fixed;
		  color: #fff;
		  background: rgba(0,0,0,0.5);
		  border-radius: 25px;
		  padding: 10px;
		  right:0;
		  top:10px;
		  z-index: 1;
		}
		table, th, td
		{
		  border :1px solid black;
		  border-collapse : collapse;
	      text-align: center;
		  padding: 10px;
		}
		</style>
		<body>
		  <div id="info">
		  <p align="left">City: <b>'''+city+'''</b></p>
		  <p align="left">Location: <b>'''+str(location['lat'])+''','''+str(location['lng'])+'''</b></p>
		  <p>1. Number of Cluster points dectected by our analysis: <b>'''+str(len(centroids))+'''</b>. Denoted by marker <img src="http://maps.google.com/mapfiles/ms/icons/red-dot.png" alt="red marker" /></p>
		  <p>2. Number of Bank locations returned by Bank API: <b>'''+str(len(api_data))+'''</b>. Denoted by marker <img src="http://maps.google.com/mapfiles/ms/icons/green-dot.png" alt="green marker" /></p>
		  <p>3. Number of New Bank locations predicted by us: <b>'''+str(len(result))+'''</b>. Denoted by marker <img src="http://maps.google.com/mapfiles/ms/icons/blue-dot.png" alt="blue marker" /></p>
		  </div>
		  <div id="map1" style="width: 900px; height: 800px;"></div>
		  <br>
		  <div id="map2" style="width: 900px; height: 800px;"></div>
		  <br>
		  <table>
		  <thead>
		  <th>S No.</th>
		  <th>Latitude</th>
		  <th>Longitude</th>
		  <th>New Banks to be opened nearby these addresses</th>
		  </thead>
		  <tbody>
		  '''
		count=0
		for latlng in result:
			d = {'latlng': latlng}
			rg = gmaps.reverse_geocode(**d)
			rg = rg[0]
			count+=1
			output+='<tr><td>'+str(count)+'</td><td>'+(str(rg.get("geometry").get("location").get("lat"))+'</td><td>'+str(rg.get("geometry").get("location").get("lng"))+'</td><td>'+rg.get("formatted_address"))+'</td></tr>'

		output+='''
		  </tbody>
		  </table>
		  <script>
		    // Define your locations: HTML content for the info window, latitude, longitude
		    var locations1 = '''+json.dumps(centroids)+''';
		    var locations2 = '''+json.dumps(api_data)+''';
			var locations3 = '''+json.dumps(result)+''';
		    // Setup the different icons and shadows
		    var iconURLPrefix = 'http://maps.google.com/mapfiles/ms/icons/';

		    var icons = [
		      iconURLPrefix + 'red-dot.png',
		      iconURLPrefix + 'green-dot.png',
		      iconURLPrefix + 'blue-dot.png',
		    ]
		    var iconsLength = icons.length;

		    var map1 = new google.maps.Map(document.getElementById('map1'), {
		      zoom: 11,
		      center: new google.maps.LatLng('''+str(location['lat'])+''','''+str(location['lng'])+'''),
		      mapTypeId: google.maps.MapTypeId.ROADMAP,
		      mapTypeControl: false,
		      streetViewControl: false,
		      panControl: false,
		      zoomControlOptions: {
		         position: google.maps.ControlPosition.LEFT_BOTTOM
		      }
		    });

		    var map2 = new google.maps.Map(document.getElementById('map2'), {
		      zoom: 11,
		      center: new google.maps.LatLng('''+str(location['lat'])+''','''+str(location['lng'])+'''),
		      mapTypeId: google.maps.MapTypeId.ROADMAP,
		      mapTypeControl: false,
		      streetViewControl: false,
		      panControl: false,
		      zoomControlOptions: {
		         position: google.maps.ControlPosition.LEFT_BOTTOM
		      }
		    });

		    var markers = new Array();

		    var iconCounter = 0;

		    // Add the markers to the map
		    for (var i = 0; i < locations1.length; i++) {  
		      var marker = new google.maps.Marker({
		        position: new google.maps.LatLng(locations1[i][0], locations1[i][1]),
		        map: map1,
		        icon: icons[iconCounter]
		      });

		      markers.push(marker);
		    }

		    iconCounter++;

		    for (var i = 0; i < locations2.length; i++) {  
		      var marker = new google.maps.Marker({
		        position: new google.maps.LatLng(locations2[i][0], locations2[i][1]),
		        map: map2,
		        icon: icons[iconCounter]
		      });

		      markers.push(marker);
		    }

		    iconCounter++;

		    for (var i = 0; i < locations3.length; i++) {  
		      var marker = new google.maps.Marker({
		        position: new google.maps.LatLng(locations3[i][0], locations3[i][1]),
		        map: map2,
		        icon: icons[iconCounter]
		      });

		      markers.push(marker);
		    }

		    function autoCenter() {
		      //  Create a new viewpoint bound
		      var bounds = new google.maps.LatLngBounds();
		      //  Go through each...
		      for (var i = 0; i < markers.length; i++) {  
		                bounds.extend(markers[i].position);
		      }
		      //  Fit these bounds to the map
		      map1.fitBounds(bounds);
		      map2.fitBounds(bounds);
		    }
		    autoCenter();
		  </script> 
		</body>
		</html>
		'''
		return HttpResponse(output)