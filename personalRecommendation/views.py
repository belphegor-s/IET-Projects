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
#from sklearn.cluster import DBSCAN, KMeans
from django.http import HttpResponse
from math import pi, sqrt, fabs
#import wikipedia as wiki
#import numpy as np
import googlemaps
import requests
import json
import time

# Personalized Tourism Recommendation API
# Stacks Used : Django v1.11, Django REST Framework, Scikit-Learn, Numpy, Google Maps Geocoding, Reverse Geocoding, Places API, Python v2.7.12.
# Go to http://localhost:8000/api/tourism/ to run the API
# Make a POST request as {"city": "city_name"} to fetch the results

class PersonalRecommendationAPI(APIView):
	permission_class = (AllowAny,)

	def get(self, request, format=None):
		return Response("Rajasthan Hackathon 3.0 : Personalized Tourism Recommendation API (The Incredibles)")

	def post(self, request, format=None):
		city = request.data.get('city')
		city = str(city)
		city = str.title(city)

		radius = 35000
		jdata = json.loads(open ('personalRecommendation/district.json').read())
		for i in jdata:
			if i['district'] == city:
				area = i['area']
				area = int(area.replace(',', ''))
				radius = int(sqrt(area / pi))*1000
				state = i['state']
				state = state.split('(')[0]
				print state

		data=[]
		s=0
		cnt=0
		number=[0]*16
		gmaps = googlemaps.Client(key='AIzaSyAjZ1GH-BUtxWPY2-fIV27CsuHrmDWhWNo')
		geocode_result = gmaps.geocode(state)
		location = geocode_result[0]['geometry']['location']
		latlng = (location['lat'], location['lng'])
		# 0-> arcitecture
		# 1->art
		# 2->adventure
		# 3-> nature
		# 4->shopping
		# 5->safari

		# Collecting data from various places with the help of Google Maps Places API
		places = [ ['historical buildings', 'forts', 'palaces', 'temples', 'castles'],
		['painting', 'crafts', 'museum', 'archeological sites'],
		['camel riding', 'safari', 'camping', 'tiger reserve', 'sanctuary'],
		['lakes', 'zoo', 'waterfall', 'bird sanctuary',],
		 ]
		#architecture', 'art', 'desert', 'museum', 'nature', 'outdoor_recreation', 'safari', 'shopping', 'tiger', 'wildlife']
		# architecture = ['historical buildings', 'forts', 'palaces', 'temples', 'castles']
		# arts = ['painting', 'crafts', 'museum', 'archeological sites']
		# adventure = ['camel riding', 'safari', 'camping', 'tiger reserve', 'sanctuary']
		# nature = ['lakes', 'zoo', 'waterfall', 'bird sanctuary']
		for j in places:
			ct=0
			for i in j:
				d = {'query': i+str(' in ')+city, 'location': latlng, 'radius': 50000,}
				places_result  = gmaps.places(**d)
				for x in places_result.get("results"):
					dt=(x.get("geometry").get("location").get("lat"),x.get("geometry").get("location").get("lng"),x.get("name"),x.get("rating"),x.get("types"))
					if data.count(dt) == 0:
						data.append(dt)
						ct+=1
			print(ct)
		print(len(data))
		# places = ['amusement_park', 'aquarium', 'art_gallery', 'church', 'hindu_temple', 'library', 'mosque', 'museum', 'park', 'zoo', 'lodging', 'restaurant', 'university', 'stadium', 'spa', 'shopping_mall']
		# for i in places:
		# 	d = {'location': latlng, 'radius': radius, 'type': i}
		# 	places_result  = gmaps.places_nearby(**d)	
		# 	for x in places_result.get("results"):
		# 		data.append((x.get("geometry").get("location").get("lat"),x.get("geometry").get("location").get("lng"),x.get("name"),x.get("rating"),x.get("types")))
		# 		try:
		# 			print (wiki.summary(x.get("name"),sentences=1))
		# 		except (wiki.exceptions.PageError, wiki.exceptions.DisambiguationError) as e:
		# 			continue
		# 	number[cnt]=len(data)-s
		# 	s += number[cnt]
		# 	cnt+=1
		return HttpResponse(data)