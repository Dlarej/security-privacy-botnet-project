from flask import Flask,redirect
from flask import render_template
from flask import request
from twython import Twython
from redis import Redis
import shelve
 
app = Flask(__name__)
r = Redis()

API_KEY = "xDkNHkEOYBTGhTJYW3eyR4eqh"
API_SECRET = "TRargGx8DQ98tw60TOZYaGei3Rhj8n7uIr6XpFvZ1HU6JiygaT"

@app.route("/twitter", methods=["GET"])
def display():
	#Create Twitter API instance
	twitter = Twython(app_key=API_KEY, app_secret=API_SECRET)
	#Get auth url
	#auth = twitter.get_authentication_tokens()
	auth = twitter.get_authentication_tokens(callback_url='http://54.165.104.227:81/twitterfinish')
	#Save off token and secret for later use. Could be saved in cookies.
	d = shelve.open('tokens')
	twitter_token = auth['oauth_token']
	twitter_secret = auth['oauth_token_secret']
	d['twitter:token'] = auth['oauth_token']
	d['twitter:secret'] = auth['oauth_token_secret']
	d.close()
	#redirect user to auth link
	return redirect(auth['auth_url'])

@app.route("/twitterfinish", methods=["GET"])
def finish():
	#Get verifier from GET request from Twitter
	verifier = request.args['oauth_verifier']
	#Get token and secret that was saved earlier
	d = shelve.open('tokens')
	token = d['twitter:token'] #r.get("twitter:token")
	secret = d['twitter:secret'] #r.get("twitter:secret")
	d.close()
	print "Token "+token+"\n"
	print "Secret "+secret+"\n"
	#Create new Twitter API instance with the new credentials
	twitter = Twython(API_KEY, API_SECRET, token, secret)
	#Send new credentials with verifier to get the access_token
	last = twitter.get_authorized_tokens(verifier)
	# get access_key, access_secret & botname to writeout to writeout
	access_key = last['oauth_token']
	access_secret = last['oauth_token_secret']
	twitter2 = Twython(API_KEY, API_SECRET, access_key, access_secret)
	bot_name = twitter2.verify_credentials()['screen_name']
	# write out and update our csv file
	with open("bots.csv", "a") as f:
		f.write("bot=%s,%s,%s,%s,%s\n" % (bot_name, API_KEY, API_SECRET, access_key, access_secret))
	return "Success!"

if __name__ == '__main__':
	#app.run()
	app.run(host='0.0.0.0',debug=True, port=81)
