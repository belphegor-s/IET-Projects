# New Branch Evaluation API

**Used to find out various potential premises for setting up banks through spatial analysis and location intelligence.**

## Idea

* Opening a new branch and identifying the ideal location for new Branch, ATM or Kiosk, is important to widen its customer base.
* In gaining new customers, a bank gain edge over other competitors, if it is the first to enter the market, so we predict places where future growth of the bank is tremendous by analyzing upcoming commercial hub and major projects.
* Analyzing various factors to widen our HNI (High net worth individual) and corporate customer base.
* The branch location would also be easily accessible by the customers as they are nearby Bus Stops, Metro, Railway Stations etc.

## Working

**Finding out potential hubs/premises based upon spatial and data analysis**

*( Spatial Analysis on the basis of Scoring and Ranking of the markers clustered over specific locations to find out the potential premise/hub over the whole city )*

<p align="center"><img alt="Spacial Analysis" src="https://user-images.githubusercontent.com/20622980/31309537-5ebd70ca-aba5-11e7-8800-663ee72bebff.jpg"></p>

* With the help of Marker Clustering and Geocoding Google Maps APIs, we will first scan the whole city and find out the densities of location pointers over a particular area.
* Then with the help of scoring and ranking of the markers over that particular premises we will add the weights to those markers to calculate the Statistical Value (Sv) of that location. Statistical value is calculated on the basis of population, traffic, pointer showing shop, bus stops, bus stands,marker clustering.
* With the K nearest neighbors (KNN) Algorithm we would be able to make smaller cluster and find out its centroid. The centroid will be marked as a premise location.
* Then through the Bank's APIs and Statistical Radius, we will find out that if the bank is already setup nearby that location or not.
* If not then with the above analysis we will confirm the bank to set up a branch there.

<h3 align="center"><b><i>Statistical Value = &Sigma;(Scores and Ranks of the various clusters formed)</i></b></h3>

<h3 align="center"><b><i>Statistical Radius = Radius of smallest Incircle of the tangential polygon (Cluster) formed by KNN Algorithm</i></b></h3>

## Constraints 

* No other bank near it as it increase competition; college, mall, shopping mart should have a bank.
* Model works on score and ranking that is bigger hospital is given more priority over smaller clinic i.e. scores.
* More score is given to a place according to its value, For e.g. Ram Lohiya Hospital spread across 1km^2 has higher preference than 50 small marker shop spread across 500m^2.

## Input

*City Name*

## Output

| S No. | Longitude | Latitude |Statistical Radius | Type (Eg : Branches, ATM etc)|
| -------- | ---------------|------------- | -------------------------| --------------------------------------- |
| 1       |               |             |                         |                                      |    
| 2       |               |             |                         |                                      |  
| 3       |               |             |                         |                                      |

* Here on entering the city name ,the output will be displayed on the screen showing latitude,longitude of the potential premise for setting up bank and value of statistical radius instructing the bank that new branch should be open within statistical radius keeping longitude and longitude as the center of the circle.Type column indicate branch/office/currency chest/ATM/e-lounge/digital kiosk.

## Features

* [Marker Clustering](https://googlemaps.github.io/js-marker-clusterer/docs/reference.html) 
	* With the help of marker clustering we will be able to find out the density of markers in a particular location.

* [K nearest neighbors Algorithm]( https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm) 
	* With the KNN algorithm we would be able to make smaller cluster and find the centroid of the weighted markers.The centroid longitude and latitude will be the desired output.

## APIs to Use

**Bank API**

* [BRANCH AND ATM LOCATION](https://s3-ap-southeast-1.amazonaws.com/he-public-data/Finathon_API_Version_1_0e754ae7.pdf)
	* RADIUS SEARCH
			
	* CITY WISE SEARCH

<br>					
	
**Google Maps APIs**

* [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding/start)

	**Geocoding** is the process of converting addresses (like a street address) into geographic coordinates (like latitude and longitude), which you can use to   place markers on a map, or position on the map.

	**Reverse geocoding** is the process of converting geographic coordinates into a human-readable address.

	You can also use the Google Maps Geocoding API to find the address for a given place ID.


* [Heatmap Layer](https://developers.google.com/maps/documentation/javascript/heatmaplayer)

	A heatmap is a visualization used to depict the intensity of data at geographical points. When the Heatmap Layer is enabled, a colored overlay will appear on top of the map. By default, areas of higher intensity will be colored red, and areas of lower intensity will appear green.
	
<br>	

-----

<br>

# Tender Filling API

 **Used to scrap data from various relevant sites & present potential premises to be taken for rent / lease.**

## Idea

* **Problem -**
	*  Basically tender filling is considered to be herculean task & people might miss reading about that in the newspaper.So if we can increase the number of tender being filled then the probability of getting best location at best price increases. 
* **Solution -**
	* With the help of property dealing and renting sites like MagicBricks, 99Acres.com etc. we can tell bank about the availability of the properties available over that location.

## Working 

**Finding out Commercial properties in that locality with following specification :**

* For this purpose we are using `Nestoria API` which will find out the ideal properties for rent/lease for setting up of the bank branch. 
* The API will fetch the properties from the sites like 99Acres.com, MagicBricks etc. and on the comparison basis we can tell the bank where the property is available at the lowest rates. 
* We also will see the presence of other banks in that location, for setting up a new bank branch in that location.
* For competition purpose, we will also check out their revenues and annual turnovers to see if the presence of any other bank's branch will not make any issue while setting up a new bank location there.

## Input

* Based upon above data analysis i.e. Longitude, Latitude and Statistical Radius.

## Output

` By collecting data from various websites e.g: Magic Bricks, 99Acres.com`

| S No. | Owner Name | Property Address | Description | Rent |
| -------- | -------- | -------- | -------- | -------- |
| 1   |   |   |   |   |    
|  2  |   |   |   |   |   
|  3  |   |   |   |   |  | 

## APIs to Use

**Nestoria API**

* [Nestoria API](https://www.nestoria.co.uk/help/api)	

	Nestoria is a search engine for Indian real estate. Our goal is to make it as easy as possible for you to find your ideal property to rent/lease.
