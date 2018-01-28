# Building a URL Shortener & QR Code Generator Bot for Facebook Messenger on Hasura

<p align="center"><img src="https://user-images.githubusercontent.com/20622980/35486412-aa3af56c-0493-11e8-8c9f-31544fbbea63.gif" /></p>

This tutorial is a guide to run a **URL Shortener & QR Code Generator bot on facebook messenger**, that create short URLs in real time and can also generate QR Code for that URL, which can be easily shared, tweeted, or emailed to friends. It is build by using [Google URL Shortener API](https://developers.google.com/api-client-library/python/apis/urlshortener/v1) and [pyshorteners](http://www.ellison.rocks/pyshorteners/).

For the chat bot to function we'll need a server that will receive the messages sent by the Facebook users, process this message and respond back to the user. To send messages back to the server we will use the graph API provided by Facebook. For the Facebook servers to talk to our server, the endpoint URL of our server should be accessible to the Facebook server and should use a secure HTTPS URL. For this reason, running our server locally will not work and instead we need to host our server online. In this tutorial, we are going to deploy our server on Hasura which automatically provides SSL-enabled domains.

You can get the full code for the project from this [Github repository](https://github.com/vishalpolley/fb-url-shortener-bot).


## Pre-requisites

- [Hasura CLI](https://docs.hasura.io/0.15/manual/install-hasura-cli.html)

- [Git](https://git-scm.com)

- [Python 3](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installing/) (required only for local development)

- [Flask](http://flask.pocoo.org/)


## Getting the bot running

### Create a facebook application

* Navigate to https://developers.facebook.com/apps/

* Click on **'+ Create a new app’** or **'+ Add a new app’**.


![fb app photo1](https://user-images.githubusercontent.com/20622980/35475394-e0a6651c-03c3-11e8-894e-e23f1c5773d5.png)


* Give a **Display Name** for your app and your **Contact Email**.


![fb app photo2](https://user-images.githubusercontent.com/20622980/35474339-ef8a9e6a-03b2-11e8-8ac1-5fcfad27a88d.png)


* In the select a product screen, hover over **Messenger** and click on **Set Up**


![fb app photo3](https://user-images.githubusercontent.com/20622980/35475404-0dca5f80-03c4-11e8-8069-b41626ef9e77.png)


* To start using the bot, we need a facebook page to host our bot.

  + Scroll over to the **Token Generation** section

  + Choose a page from the dropdown (Incase you do not have a page, create one [here](https://www.facebook.com/pages/create))

  + Once you have selected a page, a *Page Access Token* will be generated for you.

  + Save this token somewhere.


![Page Token](https://user-images.githubusercontent.com/20622980/35475423-37019c88-03c4-11e8-9fa3-38d62f2dd5ad.png)


* Now, we need to trigger the facebook app to start sending us messages

  - Switch back to the terminal

  - Paste the following command:

```sh
# Replace <PAGE_ACCESS_TOKEN> with the page access token you just generated.
$ curl -X POST "https://graph.facebook.com/v2.6/me/subscribed_apps?access_token=<PAGE_ACCESS_TOKEN>"
```

* In this project, we are using [pyshorteners](http://www.ellison.rocks/pyshorteners/) python module which requires Google API key to generate the QR Code for the URL in real time. To get your API key follow up [here](https://support.google.com/googleapi/answer/6158862?hl=en).

### Getting the Hasura project

```
$ hasura quickstart vishalpolley/fb-url-shortener-bot
$ cd fb-url-shortener-bot
# Add FACEBOOK_VERIFY_TOKEN to secrets. This is any pass phrase that you decide on, keep a note on what you are choosing as your verify token, we will be using it later while setting things up for your bot on the facebook developer page.
$ hasura secrets update verify.token <YOUR-VERIFY-TOKEN>
# Add FACEBOOK_PAGE_ACCESS_TOKEN to secrets
$ hasura secrets update page.access.token <YOUR-FB-PAGE-ACCESS-TOKEN>
# Add GOOGLE_API_KEY to secrets
$ hasura secrets update api.key <YOUR-GOOGLE-API-KEY>
# Deploy
$ git add . && git commit -m "Deployment commit"
$ git push hasura master
```

After the `git push` completes:

```sh
$ hasura microservice list
```

You will get an output like so:

```sh
INFO Getting microservices...                     
INFO Hasura microservices:                        
USER MS NAME     STATUS      INTERNAL-URL       EXTERNAL-URL        
app              Running     app.default:80     http://app.cynosure54.hasura-app.io/

HASURA MS NAME     STATUS      INTERNAL-URL                  EXTERNAL-URL
le-agent           Running                                   
platform-sync      Running                                   
session-redis      Running     session-redis.hasura:6379     
notify             Running     notify.hasura:80              http://notify.cynosure54.hasura-app.io/
gateway            Running                                   
sshd               Running                                   
auth               Running     auth.hasura:80                http://auth.cynosure54.hasura-app.io/
data               Running     data.hasura:80                http://data.cynosure54.hasura-app.io/
filestore          Running     filestore.hasura:80           http://filestore.cynosure54.hasura-app.io/
postgres           Running     postgres.hasura:5432  
```

Find the EXTERNAL-URL for the service named `bot` and keep a note of it after changing the `http` to `https` in the URL. 
(For example, in this case -> https://app.cynosure54.hasura-app.io/).

### Enabling webhooks

In your fb app page, scroll down until you find a card name `Webhooks`. Click on the `setup webhooks` button.

![Enable Webhooks](https://user-images.githubusercontent.com/20622980/35474409-e5c7ee0e-03b3-11e8-8046-0345c2f23854.png)

* The `callback URL` is the URL that the facebook servers will hit to verify as well as forward the messages sent to our bot. The flask app in this project uses the `/webhook` path as the `callback URL`. Making the `callback URL` https://bot.YOUR-CLUSTER-NAME.hasura-app.io/webhook (in this case -> https://app.cynosure54.hasura-app.io/webhook/)

* The `verify token`is the verify token that you set in your secrets above (in the command `$ hasura secrets update verify.token <YOUR-VERIFY-TOKEN>`)

* After selecting all the `Subsciption Fields`. Submit and save.

* You will also see another section under `Webhooks` that says `Select a page to subscribe your webhook to the page events`, ensure that you select the respective facebook page here.

Next, open up your facebook page.

* Hover over the **Send Message** button and click on Test Button.


![Test Button](https://user-images.githubusercontent.com/20622980/35487016-b3b4e4a0-049c-11e8-9f84-de1ea784c168.png)


* Instead, if your button says **+ Add Button**, click on it.

* Next, click on **Use our messenger bot**. Then, **Get Started** and finally **Add Button**.

* You will now see that the **+ Add button** has now changed to **Get Started**. Hovering over this will show you a list with an item named **Test this button**. Click on it to start chatting with your bot.

* Send a message to your bot.


## Usage

The bot creates short URLs in real time and can also generate QR Code for that URL, which can be easily shared, tweeted, or emailed to friends.

* To generate **Shorten URL** for any web address, just paste the URL as 

```
https://hasura.io/hub/project/vishalpolley/fb-url-shortener-bot
``` 

The bot will generate the shorten URL as 

```
Your shorten url is 
 https://goo.gl/A4KDsC
```

* To get the **Sharable QR Code** for your URL, just add `\qr` before the web address in following way

```
/qr https://hasura.io/hub/project/vishalpolley/fb-url-shortener-bot
```

This will generate the QR Code as 

```
Share your QR Code as 
 http://chart.apis.google.com/chart?cht=qr&chl=https://goo.gl/A4KDsC&chs=120x120
```
![chart](https://user-images.githubusercontent.com/20622980/35487139-4e2e394a-049e-11e8-9f17-b0dcab496c12.png)


## Support

If you happen to get stuck anywhere, feel free to raise an issue [here](https://github.com/vishalpolley/fb-url-shortener-bot/issues)

Also, you can contact me via [email](mailto:vishalpolley290996@gmail.com) or [linkedin](https://www.linkedin.com/in/vishalpolley/) or [facebook](https://www.fb.com/vishal.polley).
