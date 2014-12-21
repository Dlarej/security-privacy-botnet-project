from twython import TwythonStreamer
from profile import Profile
import time
import sys

MOST_LIKELY_FILE = 'most_likely_'
LIKELY_FILE = 'likely_'
LEAST_LIKELY_FILE = 'least_likely_'

profiles = {}

def clean(s):
    s = s.strip()
    s = s.lower()
    return s

# Check if the account is fake
# Adds fakes to a file
def track_fake(tweet, directory, filename):
    user = tweet['user']
    fakeness = 0
    most_likely = 7
    likely = 4 
    least_likely = 2
    reasons = 'Reasons: '

    if user['id_str'] not in profiles:
        profile = Profile(user, user['id_str'], user['screen_name'])
        profiles[user['id_str']] = profile
    else:
        profile = profiles[user['id_str']]

    # Check if tweet matches another tweet
    tweetText = tweet['text'].encode('utf-8')
    profile.addTweet(tweetText)
    if profile.checkSameTweet():
        profile.fakeness += 2
        profile.reasons += 'duplicate tweet, '

    #Check if they have a default profile
    if user['default_profile']:
        profile.fakeness += 1
        profile.reasons += 'default, '

    # Check if they have a profile picture
    if user['default_profile_image']:
        profile.fakeness += 2
        profile.reasons += 'egghead, '

    # Check if they have a description
    if user['description'] is None:
        profile.fakeness += 1
        profile.reasons += 'no description, '

    # Check if they follow or 2000 or 2001 users
    if user['friends_count'] == 2000 or user['friends_count'] == 2001:
        profile.fakeness +=  1
        profile.reasons += 'max followings, '

    # Check if they are followed by many people
    if user['followers_count'] == 0:
        profile.fakeness += 2
        profile.reasons += 'no followers, '
    elif user['followers_count'] < 5:
        profile.fakeness += 1

    # A profile is considered fake if the number of fake attributes are greater than the threshold
    # Fake profiles are added to a file
    if profile.fakeness >= most_likely:
        path = directory+MOST_LIKELY_FILE+filename
        with open(path, 'a') as file:
            file.write(str(user['id'])+', '+str(user['screen_name'])+', '+profile.reasons+'\n')
        return True
    elif profile.fakeness >= likely:
        path = directory+LIKELY_FILE+filename
        with open(path, 'a') as file:
            file.write(str(user['id'])+', '+str(user['screen_name'])+', '+profile.reasons+'\n')
        return True
    elif profile.fakeness >= least_likely:
        path = directory+LEAST_LIKELY_FILE+filename
        with open(path, 'a') as file:
            file.write(str(user['id'])+', '+str(user['screen_name'])+', '+profile.reasons+'\n')
        return True
    else:
        return False

class TwitterStreamer(TwythonStreamer):

    excluded = []
    directory = 'fakes_data/'
    filename = 'fakes.csv'
    timeout = -1
    start_time = time.time()

    def filter_out(self, ex):
        words = ex.split(",")
        self.excluded = []
        for word in words:
            self.excluded.append(clean(word))

    def on_success(self, data):
        if 'text' in data:
            text = data['text'].encode('utf-8')
            
            # Filter out if tweet contains excluded words
            for phrase in self.excluded:
                if phrase.lower() in text.lower():
                    return

            # Check if account is fake
            track_fake(data, self.directory, self.filename)


        if time.time()-self.start_time > self.timeout and self.timeout >= 0:
            self.disconnect()
            #sys.exit()
            
    def on_error(self, status_code, data):
        self.disconnect()

