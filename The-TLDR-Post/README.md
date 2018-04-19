# The TLDR; Post Web Application 

It is a Web Application built by using Django.

## Table of Contents
  - [Set Up](#set-up)
  - [Accessing the REST Framework](#accessing-the-rest-framework)
  - [Operations on the REST API](#operations-on-the-rest-api)
  - [Production Guide](#production-guide)
  - [API](#api)
  
## Set Up

* Firstly clone/download the repo [Click](https://github.com/gksrivas/WebApp-TLDR-Khabar/archive/vishalpolley.zip)
* Navigate to src folder inside TLDR.
```
cd TLDR/
```
* Install the required python packages by using the following commands in terminal (Ubuntu/Mint users)
```
sudo pip2 install -r requirements.txt
```
Required only to install via pip2 in place of pip.

* Create a superuser by using following command
```
python manage.py createsuperuser
```

* Now run the server by using 
```
python manage.py runserver
```

* Navigate to page and enter the URL 
```
http://localhost:8000/
```

The summarized content/detail for the page will be displayed.

![screenshot from 2017-09-23 14-54-34](https://user-images.githubusercontent.com/20622980/30771928-b2826ef4-a06f-11e7-91c0-13e1ba0d41fd.png)

![screenshot from 2017-09-23 14-57-40](https://user-images.githubusercontent.com/20622980/30771929-b827536a-a06f-11e7-999d-96c5767651e7.png)


### Fixtures

* Load the fixtures(database dump) into database 
```
python manage.py loaddata feeds.json
```
Dump the current feeds from the database using following command (the feeds will be saved in JSON format in feeds.json)
```
python manage.py dumpdata --format=json summarize --indent 4 > feeds.json
```

### CRON Job

Cron Job is done by django-crontab python module [Link](https://github.com/kraiz/django-crontab)

* Run the Cron Job for getting latest news feeds (The feeds are refreshed every hour.)
```
python manage.py crontab add
```
to stop the cron job run
```
python manage.py crontab remove
```
to display current cron job running run
```
python manage.py crontab show
```

## Accessing the REST Framework

* Navigate to the page
```
http://localhost:8000/api/summary/list/
```
At this page the title, url, summarized url and source from the rss news feeds are displayed in JSON format.

![screenshot from 2017-07-23 23-14-26](https://user-images.githubusercontent.com/20622980/28501598-d710e370-6ffc-11e7-8ab1-4f32a4977a2a.png)

* Access the Raw JSON data by going to the url
```
http://localhost:8000/api/summary/list/?format=json
```

* The response JSON data is in the following form
```
{"title":"news_title","url":"entered_url","summarize_url":"summary_of_the_url","source":"news_source"}
```

## Operations on the REST API 

1. **Creating summaries of the urls via [cURL](https://curl.haxx.se/docs/manpage.html)**

* Enter the following command in the terminal
```
curl -X POST http://localhost:8000/api/summary/ -d "url=enter_url&source=news_source"
```
where `enter_url` must be replaced by the requested URL and `source` must be replaced by the news source (e.g. Huffington Post, CNN, Times of India etc.)

* ``` "url=enter_url" ``` is the url parameter. Entered URL must be in valid form.

* ``` "source=news_source" ``` is the news source parameter. It is a non compulsory field.

* On sending `` POST `` request on ``` http://localhost://8000/api/summary/ ```  API url via cURL command, we get the summary of the entered url.

* The response JSON data is in the following form
```
{"title":"news_title","url":"entered_url","summarize_url":"summary_of_the_url","source":"news_source"}
```
where
```title``` - Title of the news article.

``url`` - Entered URL.

``summarize_url`` - Summarized article of the URL.

```source``` - News Source of the summarized article.

![screenshot from 2017-07-23 23-21-33](https://user-images.githubusercontent.com/20622980/28501652-ed7d1bfa-6ffd-11e7-8f5d-810e33c15893.png)

2. **Creating summaries of the urls via [Postman](https://www.getpostman.com/)**

* From the requests options select `POST` request.

* Enter the following API url
```
http://localhost:8000/api/summary/
```

* In the ``Body``, click on `raw` radio button and from the options select `JSON(application/json)`.

* Enter the `url` and `source` in JSON format as
```
{
  "url": "enter_url",
  "source": "news_source"
}
```

![screenshot from 2017-07-23 23-22-52](https://user-images.githubusercontent.com/20622980/28501654-f469fc3a-6ffd-11e7-9880-5263eba33c8a.png)

* The response is in the JSON format as
```
{
    "title": "news_title",
    "url": "entered_url",
    "summarize_url": "summary_of_the_url",
    "source": "news_source"
}
```

![screenshot from 2017-07-23 23-22-57](https://user-images.githubusercontent.com/20622980/28501655-f7657a22-6ffd-11e7-9d4e-d2e8bd802e3b.png)


## Production Guide

`Required Python version - 2.7`

`Required Django version - 1.11`

The following steps are necessary for deploying the project over production server : - 

* Firstly navigate to settings module at

```
cd TLDR/tldr/
```

### Editing `settings.py` file

```
DEBUG = False
```

>For production purposes, keep `DEBUG` value `False`.
>
>For testing the project locally change the value of `DEBUG` equals `True`.

#### 1). Edit the ADMINS command 

Add the `admins` whom you want to send `emails` regarding `500 server errors` , this command will send the details regarding the errors occuring in the server to the admins.

Add the `name` and `email` in `tuple` format 

```
ADMINS = (("admin_name", "admin_email"),)
```
#### 2). Edit the allowed host command 

Enter the `website` url where you project will host.

```
ALLOWED_HOSTS = ['https://tldr.erigolabs.com',]
```

#### 3). Database settings (MySQL) 

> Reference video - [Link](https://youtu.be/cJESeioAFpU?t=3m26s)

Enter the name of the `database table`, `username` and `password`

```
MySQL Database -- During Production
DATABASES = {
    'default': {
        'NAME': 'database_table_name',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'mysql_user',
        'PASSWORD': 'superS3cret'
    }
}
```

The `NAME` , `USER` and `PASSWORD` fields must be changed.

* After that run the following command
```
python manage.py migrate
```
* Now create a new superuser
```
python manage.py createsuperuser
```
* Navigate to 
```
# Replace mysite.com with the actual site url.
https://tldr.erigolabs.com/admin/
```

to test if the admin page is displayed, after that enter the `username` and `password` as created during `createsuperuser` command


## API

The application contains following two APIs :-

  - [Summary API](#summary-api)
  - [Feeds API](#feeds-api)
  
  
### Summary API

* Send HTTP request on the following url 

```
https://tldr.erigolabs.com/api/summary/
```

* On Summary API you can perform `GET` and `POST` requests. 

#### GET

On sending GET request on the API you can fetch all the stored feeds from the database (default number of lines of feeds is 5) in the following format.

```
[
  {
      "title": "news_title",
      "url": "news_url",
      "summarize_url": "summary_of_the_url",
      "source": "news_source"
  },
  {
      "title": "news_title",
      "url": "news_url",
      "summarize_url": "summary_of_the_url",
      "source": "news_source"
  },
  .
  .
  .
]
```

#### POST

* Send the POST request with `url` and `source` as parameters to get the summary.

```
{
  "url": "enter_url",
  "source": "news_source"
}
```

* The return JSON is in the following format

```
{
    "title": "news_title",
    "url": "entered_url",
    "summarize_url": "summary_of_the_url",
    "source": "news_source"
}
```


### Feeds API

* Send HTTP request on the following url 
```
https://tldr.erigolabs.com/api/summary/list/
```

* On Feeds API you can perform `GET` and `POST` requests. 

#### GET

* In the GET API, if the user is authenticated (mainly for web app) then the feeds are returned according to the parameters set by him in the settings, in the same format.

* If the user is not authenticated then the API fetches all the stored feeds from the database (default number of lines of feeds is 5).

#### POST

* Send the POST request (for android app) with `nol` (number of lines) and `toi`, `ht` and `cnn` as parameters to get the required summary in the following format 

```
{  
   "nol" : 5,
   "toi" : true,
   "cnn" : true,
   "ht" : false
}
```
* `nol` (number of lines) must be varied between 1 to 10.

* The values of `toi`, `ht` and `cnn` must be set to either `true` or `false`.

* The retured JSON will contain the feeds according to the parameterized settings.
