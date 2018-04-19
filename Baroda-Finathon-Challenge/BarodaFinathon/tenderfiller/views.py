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
import requests
import json

# Tender Filling API
# Stacks Used : Django v1.11, Django REST Framework, Nestoria API, Python v2.7.12.
# Go to http://localhost:8000/api/tender/ to run the API
# Make a POST request as {"city": "city_name"} to fetch the results

class TenderFillingAPI(APIView):
	permission_class = (AllowAny,)

	def get(self, request, format=None):
		return Response("Baroda Finathon Challenge : New Branch Evaluation and Tender Filling API (The Capitalists)")


	def post(self, request, format=None):
		i=0
		# Adding css and scripts files
		jq="<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js'></script>"
		jq+="<script src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js'></script>"
		hd="<head><link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'>"
		sc='''<script>
				$('[data-toggle="tooltip"]').tooltip({
    				animated: 'fade',
    				placement: 'auto',
    				html: true
				});
				</script>'''
		style = '<style>tr:nth-child(even){background-color:#f2f2f2;}thead>tr{background-color:#4CAF50!important;color:white;}tr:hover{background-color:#ddd;}'
		css2 = 'width:100%;min-width:1024px;'
		css = 'border-width:1px;border-style:solid;border-color:#ddd;border-collapse:collapse;text-align:center;padding:10px;'
		style+="th,td{"+css+"}</style>"
		output="<html>"+hd+jq+style+"</head><body><div><table style="+css+css2+">"

		# Getting Input from the User
		place_name = request.data.get('city')

		# Fetching results from the Nestoria API
		url = 'https://api.nestoria.in/api?'
		data = {'encoding': 'json', 'pretty': '1', 'action': 'search_listings', 'country': 'in', 'listing_type': 'rent', 'keywords': 'commercial', 'place_name': place_name, 'centre_point': '26.8467,80.9462,10km', 'number_of_results' : '50'}
		search_result = requests.get(url, params=data).json()
		y = search_result.get("response")

		# Output Code
		output+="<thead><tr><th style="+css+">S No.</th><th>Owner Name</th><th>Property Address</th><th>Latitude</th><th>Longitude</th><th>Description</th><th>Rent</th></tr></thead><tbody>"
		for x in y.get("listings"):
			if x.get("lister_name") is not None:
				i+=1
				output+='''<tr><td>'''+str(i)+"</td><td><a data-toggle='tooltip' title='<img src=\""+str(x.get('img_url'))+"\">'>"+str(x.get('lister_name'))+"</a></td>"+'''
						'''+"<td><a href=\""+str(x.get('lister_url'))+"\" target='_blank'>"+str(x.get('title'))+"</a></td>"+'''
						'''+"<td><a href='https://maps.google.com/?q="+str(x.get('latitude'))+","+str(x.get('longitude'))+"' target='_blank'>"+str(x.get('latitude'))+"</a></td>"+'''
						'''+"<td><a href='https://maps.google.com/?q="+str(x.get('latitude'))+","+str(x.get('longitude'))+"' target='_blank'>"+str(x.get('longitude'))+"</a></td>"+'''
						'''+"<td>"+x.get('summary')+"</td><td>"+x.get('price_formatted')+"</td></tr>"			
		output+="</tbody></table></div>"+sc+"</body></html>"

		return HttpResponse(output)

	


