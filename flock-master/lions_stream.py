import gevent
from twython import Twython, TwythonError, TwythonStreamer
import json
from birdie import TwitterBot
from stream import TwitterStreamer
import find_fakes 
CU_DIR = "columbia_data/"
FAKES_DIR = "fakes_data/"

# Searches and saves the stream to the specified file
# Accounts
# - Tracks tweet if retweeted from one of these accounts
# Keywords 
# - All words in a phrase must be included to be tracked 
# - Hashtags are considered keywords. # is not needed
# Excluded
# - If any words in a phrase match 
def search(stream, accounts, keywords, excluded, directory, filename):
    # Only search for retweets from related accounts
    for account in accounts.split():
        keywords = keywords + ", RT "+account
    
    stream.directory = directory
    stream.filename = filename 
    stream.filter_out(excluded)
    stream.statuses.filter(track=keywords)

if __name__ == "__main__":
    # Columbia University Athletics search terms
    lions_stream = find_fakes.get_stream()
    lions_stream.timeout = 30
    lions_accounts = 'GoColumbiaLions, ColumbiaLionsFB, CULionsMBB, CULionsWBB, ColumbiaMSoccer, ColumbiaWSoccer'
    lions_keywords = 'Columbia Lions, ColumbiaLions, columbia football, columbia basketball, columbia soccer, go columbia, RoarLionRoar, TurnItBlue, turn it blue' 
    lions_excluded = cu_excluded+', detroit, nittany, loyola'
    search(lions_stream, lions_accounts, lions_keywords, lions_excluded, CU_DIR, 'lions_fakes.csv')
