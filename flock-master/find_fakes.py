import sys
if 'threading' in sys.modules:
    del sys.modules['threading']
import gevent
import threading
from twython import Twython, TwythonError, TwythonStreamer
import json
from birdie import TwitterBot

CU_DIR = "columbia_data/"
FAKES_DIR = "fakes_data/"

def spawn_stream(line):
    name, con_k, con_s, acc_k, acc_s = line.split("=")[1].split(",")
    return TwitterStreamer(con_k, con_s, acc_k, acc_s)

# Get Streamer 
def get_stream():
    with open('bots.csv', 'r') as bot_file:
        try:
            read_in = bot_file.readlines()
            # get lines and filter out comments or misconfigured lines
            lines = [l.rstrip() for l in read_in if not l.startswith(
                "#") and (l.startswith("bot=") or l.startswith("irc="))]
            if len(lines) <= 0:
                s = 'Could not load any bots from bot_file'
                raise Exception(s)
            
            #Create stream

            #Spawn a stream
            stream = gevent.spawn(spawn_stream, lines[3])
            stream.join(timeout=45)
            return stream.value
        except Exception as e:
            print "ERROR: " + str(e)            
 
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
    stream = get_stream()
    
    # Each stream runs as long as the timeout indicates
    # A negative timeout will run indefinitely 

    # Generic search terms
    stream = get_stream()
    stream.timeout = 30
    keywords = "http, free, weight loss, shoes"
    stream.directory = FAKES_DIR
    stream.filename = 'fakes.csv'
    stream.statuses.filter(track=keywords)

"""
    # Columbia Univeristy
    cu_stream = get_stream()
    cu_stream.timeout = 10
    cu_accounts = 'Columbia, ColumbiaMed, ColumbiaJourn, CUSEAS, TeachersCollege, BarnardCollege, CC_Columbia, Lee_Bollinger, CUMB, MillerTheater' 
    cu_keywords = 'ColumbiaUniversity, Columbia University, Columbia, CU, ColumbiaProfessor, Columbia Professor, Morningside Heights, MorningsideHeights, ccstateofmind, CUatMiller, barnard college, barnard125' 
    cu_excluded = 'sportswear, chicago, illinois, ohio, records, british, vancouver, carolina, maryland, distict of, ColumUniversity'

    search(cu_stream, cu_accounts, cu_keywords, cu_excluded, CU_DIR, 'columbia_fakes.csv')

    # Columbia University Athletics search terms
    lions_stream = get_stream()
    lions_stream.timeout = 10
    lions_accounts = 'GoColumbiaLions, ColumbiaLionsFB, CULionsMBB, CULionsWBB, ColumbiaMSoccer, ColumbiaWSoccer'
    lions_keywords = 'Columbia Lions, ColumbiaLions, columbia football, columbia basketball, columbia soccer, go columbia, RoarLionRoar, TurnItBlue, turn it blue' 
    lions_excluded = cu_excluded+', detroit, nittany, loyola'
    search(lions_stream, lions_accounts, lions_keywords, lions_excluded, CU_DIR, 'lions_fakes.csv')

    # Columbia University News
    news_stream = get_stream()
    news_stream.timeout = 10
    news_accounts = 'ColumbiaSpec, CUspectrum, CUSpecSports, theeyemag, ColumbiaUP'
    news_keywords = 'columbia news, columbia spectator, columbia article'
    search(news_stream, news_accounts, news_keywords, cu_excluded, CU_DIR, 'news_fakes.csv')

    # Columbia University activism
    activ_stream = get_stream()
    activ_stream.timeout = 10
    activ_accounts = 'NoRedTapeCU, cuprisondivesti'
    activ_keywords = 'Columbia sexual assault, columbia sexual violence, columbia rape, columbia divest, columbia activism, columbia activists, emma sulkowicz, columbia mattress'
    search(activ_stream, activ_accounts, activ_keywords, cu_excluded, CU_DIR, 'activism_fakes.csv')
    
    # Greek life
    greek_stream = get_stream()
    greek_accounts = 'axocolumbia, dgzetatheta, columbiatheta, SDTGammaTau, aoii_alpha, ColumbiaSigmaNu, AEPiColumbia'
    greek_keywords = 'columbia sorority, columbia fraternity, columbia greek, columbia alpha chi omega, columbia delta gamma, columbia DG, columiba theta, columbia SDT, columbia sigma delta tau, columbia AOII, columbia alpha omicron pi, columbia sigma nu, columiba signu, columbia aepi, columbia Alpha epsilon pi'
    search(greek_stream, greek_accounts, greek_keywords, cu_excluded, CU_DIR, 'greek_fakes.csv')

    # Columbia job search
    job_stream = get_stream()
    job_accounts = 'ColumbiaCCE'
    job_keywords = 'columbia job, columbia career, columbia coreers, columbia info session, columbia employment, columbia networking'
    search(job_stream, job_accounts, job_keywords, cu_excluded, CU_DIR, 'job_fakes.csv')
"""
