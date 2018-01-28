from src import app
from pymessenger.bot import Bot
from pyshorteners import Shortener
from flask import request, jsonify, send_file
import os, json, requests, random, urllib

ACCESS_TOKEN = os.environ['PAGE_ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
API_KEY = os.environ['API_KEY']
bot = Bot (ACCESS_TOKEN)

@app.route("/")
def home():
    return "Hasura Hello World"

# Uncomment to add a new URL at /new

# @app.route("/json")
# def json_message():
#     return jsonify(message="Hello World")

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/webhook", methods=['GET', 'POST'])
def receive_message():
	if request.method == 'GET':
		"""Before allowing people to message your bot, Facebook has implemented a verify token
		that confirms all requests that your bot receives came from Facebook.""" 
		token_sent = request.args.get("hub.verify_token")
		return verify_fb_token(token_sent)
	#if the request was not get, it must be POST and we can just proceed with sending a message back to user
	else:
		# get whatever message a user sent the bot
		output = request.get_json()
		for event in output['entry']:
			messaging = event['messaging']
			for message in messaging:
				if message.get('message'):
					#Facebook Messenger ID for user so we know where to send response back to
					recipient_id = message['sender']['id']
					if message['message'].get('text'):
						msg = list(map(str, message['message'].get('text').split()))
						if msg[0] == '/qr':
							response_sent_text = get_qr_code(msg[1])
							send_message(recipient_id, response_sent_text)
						else:
							response_sent_text = get_text_message(msg[0])
							send_message(recipient_id, response_sent_text)
	return "Message Processed"


def verify_fb_token(token_sent):
	#take token sent by facebook and verify it matches the verify token you sent
	#if they match, allow the request, else return an error 
	if token_sent == VERIFY_TOKEN:
		return request.args.get("hub.challenge")
	return 'Invalid verification token'

def get_text_message(url):
	shortener = Shortener('Google', api_key=API_KEY)
	url = shortener.short(url)
	try:
		return "Your shorten url is \n {}".format(url)
	except Exception as e:
		return "Ahh... Snap :O"

def get_qr_code(url):
	shortener = Shortener('Google', api_key=API_KEY)
	shortener.short(url)
	try:
		return "Share your QR Code as \n {}".format(shortener.qrcode())
	except Exception as e:
		return "Ahh... Snap :O"

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
	#sends user the text message provided via input response parameter
	bot.send_text_message(recipient_id, response)
	return "success"

if __name__ == "__main__":
	app.run()