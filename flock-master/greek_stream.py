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
   # Greek life
    greek_stream = find_fakes.get_stream()
    greek_stream.timeout = 30
    greek_accounts = 'axocolumbia, dgzetatheta, columbiatheta, SDTGammaTau, aoii_alpha, ColumbiaSigmaNu, AEPiColumbia'
    greek_keywords = 'columbia sorority, columbia fraternity, columbia greek, columbia alpha chi omega, columbia delta gamma, columbia DG, columiba theta, columbia SDT, columbia sigma delta tau, columbia AOII, columbia alpha omicron pi, columbia sigma nu, columiba signu, columbia aepi, columbia Alpha epsilon pi'
    cu_excluded = 'sportswear, chicago, illinois, ohio, records, british, vancouver, carolina, maryland, distict of, ColumUniversity'
    search(greek_stream, greek_accounts, greek_keywords, cu_excluded, CU_DIR, 'greek_fakes.csv')

