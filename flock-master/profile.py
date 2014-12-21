from twython import TwythonStreamer

class Profile:

    def __init__(self, user, name, ID):
            self.twitterUser = user
            self.name = name
            self.twitterID = ID
            self.fakeness = 0
            self.reasons = 'Reasons: '
            self.tweetsMade = []

    def checkSameTweet(self):
        for tweet1 in self.tweetsMade:
            count = 0
            if tweet1 in self.tweetsMade:
                count = count+1
            if count == 2:
                print self.name+" has duplicate tweet: \n    "+tweet1
                self.reasons = self.reasons+'duplicate tweet, '
                return True
            else:
                return False

    def addTweet(self, tweet):
        self.tweetsMade.append(tweet)

