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
    # Columbia job search
    job_stream = find_fakes.get_stream()
    job_stream.timeout = 30
    job_accounts = 'ColumbiaCCE'
    job_keywords = 'columbia job, columbia career, columbia coreers, columbia info session, columbia employment, columbia networking'
    cu_excluded = 'sportswear, chicago, illinois, ohio, records, british, vancouver, carolina, maryland, distict of, ColumUniversity'
    search(job_stream, job_accounts, job_keywords, cu_excluded, CU_DIR, 'job_fakes.csv')

