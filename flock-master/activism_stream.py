import gevent
from twython import Twython, TwythonError, TwythonStreamer
import json
from birdie import TwitterBot
from stream import TwitterStreamer
import find_fakes 
CU_DIR = "columbia_data/"

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
    # Columbia University activism
    activ_stream = find_fakes.get_stream()
    activ_stream.timeout = 30
    activ_accounts = 'NoRedTapeCU, cuprisondivesti'
    activ_keywords = 'Columbia sexual assault, columbia sexual violence, columbia rape, columbia divest, columbia activism, columbia activists, emma sulkowicz, columbia mattress'
    cu_excluded = 'sportswear, chicago, illinois, ohio, records, british, vancouver, carolina, maryland, distict of, ColumUniversity'
    search(activ_stream, activ_accounts, activ_keywords, cu_excluded, CU_DIR, 'activism_fakes.csv')
