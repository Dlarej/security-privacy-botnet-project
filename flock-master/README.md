flock
=====

Project for Chaim/Zack

*DEBIAN*

apt-get install libevent-dev python-dev tmux

pip install twython gevent irc flask redis greenclock TwitterAPI

I use twython for tweeting / getitng events and TwitterAPI was best for getting twitter streams

tmux

python birdie.py

python twitter_app.py

Making your botnet Application
====
1. Register for Google Voice and get a number
2. Use ToR Browser and navigate to both www.fakenamegenerator.com and www.twitter.com
3. Generate a female/male name, and activate the e-mail address they give you
4. Sign up for twitter using the full name, e-mail address
5. Activate the account
6. Go to www.tumblr.com, search 'selfie' and grab an attractive looking one for your bot
7. Upload to Twitter while following creation steps
8. Tweet a couple times and add a few more pictures related to the picture you pulled from tumblr
9. Verify your mobile phone through twitter options -- use the Google Voice phone number to text
10. Once verified, go to www.dev.twitter.com and create your app. Make sure to assign all permissions to read, write execute (full)
11. Done! Run the flask app (twitter_app.py), and edit the callback IP to some VPS
12. Once running, follow steps 2-8 and add/authorize the app through your new bots
13. Once you have enough, add an irc server in the csv, format is: irc=server:port,#channel,botname
14. Success!

Running flock
====
Connect to channel and type these commands out:

?botlist -> shows current twitter profiles connected to that bot

?shorten url -> Replace URL with the URL you want to shorten, returns shortened url

?gettrends -> returns current global top 10 trends

?tweet botname msg -> Replace botname with bot that the app owns and msg with the message you want to tweet

?campaign all url -> Posts a campaign to ALL the bots that the app owns, and shortens URL given

?campaign botname url -> Posts a campaign to only botname, shortens URL given

?campaign #hashtag url -> Posts a campaign to a specific hashtag to ALL that bots that the app owns, and shortens URL given

?tweettimes botname -> Posts tweettimes for bot botname on that specific day


A *campaign* is when an app takes 1 or all of its bots and retrieves that current time's top 10 trends. It then generates a shortened URL for each bot, and then posts a tweet according with that hashtag from the top 10 trends. It then waits a pseudo-random time to tweet again. This is all done asynchronously so bots do not need to depend on each other.

TODO
===
Mongo integration

Retweet storms
