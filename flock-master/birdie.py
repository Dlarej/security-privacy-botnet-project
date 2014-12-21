#!/usr/bin/python
import gevent
from twython import Twython, TwythonError
from ircbot import IrcNodeHead
import json
import syslog
import random
import sys
from datetime import datetime, date, time, timedelta
from random import randint

LINK = "http://google.com"

class TwitterBot:
    
    def __init__(self, name, con_k, con_s, acc_k, acc_s):
        self.name = name
        self.con_k = con_k
        self.con_s = con_s
        self.acc_k = acc_k
        self.acc_s = acc_s
        self.twitter = Twython(self.con_k, self.con_s, self.acc_k, self.acc_s)
        self.last_intervals = []
        # total number of trends you want to tweet
        self.num_trends = 3
        # number of seconds in a campaign window
        self.campaign_window = 600
        self.last_tweet = ""
        # tweets that will expire after a time limit
        self.temp_tweets = {}

    def tweet(self, msg):
        if self.twitter is not None:
            # > 140 char detection
            if len(msg) > 140:
                msg = msg[0:139]
            syslog.syslog('%s is tweeting %s' % (self.name, msg))
            try:
                tweet = self.twitter.update_status(status=msg)
                self.last_tweet = msg
                return tweet
            except Exception as e:
                syslog.syslog('%s error tweeting -> %s' % (self.name, str(e)))

    # Deletes a tweet from the given id
    def delete_tweet(self, tweet_id):
        if self.twitter is not None:
            try:
                destroyed = self.twitter.destroy_status(id=tweet_id)
                syslog.syslog('%s deleted %s' % (self.name, destroyed['text']))
                return destroyed
            except Exception as e:
                syslog.syslog('%s error deleting tweet -> %s' %(self.name, str(e)))

    # Deletes the most recent tweets
    def delete_tweets(self, num_tweets):
        if self.twitter is not None:
            try:
                timeline = self.twitter.get_user_timeline(screen_name = self.name, count = num_tweets)
                for tweet in timeline:
                    self.delete_tweet(tweet['id'])
                syslog.syslog('%s deleted %s tweet(s)' % (self.name, str(num_tweets)))
                return timeline
            except Exception as e:
                syslog.syslog('%s error deleting tweets -> %s' %(self.name, str(e)))


    # Replace all links in the text with the specified link
    def replace_link(self, text, link):
        replaced = ""
        for word in text.split():
            if word.startswith("http://") or word.startswith("https://"):
                replaced += link+" "
            else:
                replaced += word+" "
        replaced.strip()
        return replaced

    def retweet(self, tweet_id):
        if self.twitter is not None:
            try:
                tweet = self.twitter.retweet(id=tweet_id)
                syslog.syslog('%s is retweeting %s' % (self.name, tweet['text']))
                return tweet
            except Exception as e:
                syslog.syslog('%s error retweeting -> %s' %(self.name, str(e)))

    # This attack grabs a random tweet from a list of umich twitter accounts
    # If the tweet has a link it will be substituded for the attack link
    # The text of this modified tweet will then be tweeted by the bot
    # If the tweet does not have a link it is simply retweeted
    def repost_attack(self, link):
        if self.twitter is not None:
            try:
                #Get timeline of umich accounts
                umich_timeline = self.twitter.get_list_statuses(slug='UMich', owner_screen_name='JoseClark92', count=200)
                #Get user's timeline
                user_timeline = self.twitter.get_user_timeline(screen_name=self.name, count=100)
                #Get a random tweet that has not been posted by this bot
                repost = None
                while repost is None:
                    rand_tweet = random.choice(umich_timeline)
                    for tweet in user_timeline:
                        if rand_tweet['text'] in tweet: continue
                    repost = rand_tweet

                #If the tweet contains a link, replace the link and tweet it
                if "http" in repost['text']:
                    replaced = self.replace_link(repost['text'], link)
                    tweet = self.tweet(replaced)
                    #Add to the list of temporary tweets
                    self.temp_tweets[tweet['id']] = datetime.now()
                    return replaced
                #If the tweet does not contain a link, retweet it
                else:
                    retweet(tweet_id=repost['id'])
                    return repost['text']
            except Exception as e:
                syslog.syslog('%s repost attack error -> %s' %(self.name, str(e)))
    
    #Removes all temp tweets that are older than an hour
    def delete_old_tweets(self, time_to_live):
        if self.twitter is not None:
            try:
                now = datetime.now()
                for tweet in self.temp_tweets:
                    age = (self.temp_tweets[tweet] - now).seconds
                    if age > time_to_live:
                        self.delete_tweet(tweet)
            except Exception as e:
            syslog.syslog('%s error deleting old tweets -> %s' %(self.name, str(e)))

    def get_global_trends(self):
        trends = self.twitter.get_place_trends(id=1)
        ret = [trend['name']
               for trend in trends[0].get('trends')][:self.num_trends]
        return ','.join(ret)

    def post_campaign(self, url):
        trends = self.get_global_trends().split(',')
        # get minimum datetime and maximum datetime to spawn intervals in between them
        # current time
        mindt = datetime.now()
        maxdt = mindt + timedelta(seconds=self.campaign_window)
        # get num_trends intervals for num_trends tweets
        intervals = [self.randtime(mindt, maxdt)
                     for x in xrange(self.num_trends)]
        # zip the intervals and the trends
        tweet_zips = zip(intervals, trends)
        map(lambda interval_tuple: gevent.spawn_later(interval_tuple[
            0] - int(mindt.strftime('%s')), self.tweet, interval_tuple[1] + ' ' + url), tweet_zips)

    def randtime(self, mindt, maxdt):
        return randint(int(mindt.strftime('%s')), int(maxdt.strftime('%s')))


def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    # get bot info
    with open('bots.csv', 'r') as bot_file:
        try:
            read_in = bot_file.readlines()
            # get lines and filter out comments or misconfigured lines
            lines = [l.rstrip() for l in read_in if not l.startswith(
                "#") and (l.startswith("bot=") or l.startswith("irc="))]
            if len(lines) <= 0:
                s = 'Could not load any bots from bot_file'
                syslog.syslog('ERROR: %s' % s)
                raise Exception(s)
            # read in irc info, will always read first one
            irc_lines = [l for l in lines if l.startswith("irc=")]
            if len(irc_lines) <= 0:
                s = 'Could not load IRC info from bot_file'
                syslog.syslog('ERROR: %s' % s)
                raise Exception(s)
            # remove irc_line from lines
            map(lambda x: lines.remove(x), irc_lines)
            irc_serv, irc_chan, irc_name = irc_lines[
                0].split("=")[1].split(",")
            syslog.syslog('Loaded bot %s, connecting to %s and channel %s' % (
                irc_name, irc_serv, irc_chan))
            # spawn the bots, give them 45 seconds to connect to twitter then return the object
            # we will wait and start the thread for irc as our main event loop
            jobs = [gevent.spawn(spawn_bots, line) for line in lines]
            gevent.joinall(jobs, timeout=45)
            # get all the twitter bots, will raise exception if oauth fails
            bot_list = [bot.value for bot in jobs]
            # join irc as a nodehead , this bot controls many twitter bots and
            # runs campaigns for all
            port = 6667
            if ":" in irc_serv:
                irc_serv, port = irc_serv.split(":")
            irc_bot = IrcNodeHead(
                irc_chan, irc_name, irc_serv, int(port), bot_list)
            irc_bot.start()
        except Exception as e:
            syslog.syslog(syslog.LOG_ERR, 'BIRDIE: ' + str(e))
            print "ERROR: " + str(e)

# spawn bots given the config options, and return the object to jobs

def spawn_bots(bot_line):
    name, con_k, con_s, acc_k, acc_s = bot_line.split("=")[1].split(",")
    return TwitterBot(name, con_k, con_s, acc_k, acc_s)

if __name__ == "__main__":
    main()
