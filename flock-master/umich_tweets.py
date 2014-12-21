import sys
reload(sys)
sys.setdefaultencoding("utf-8")
if 'threading' in sys.modules:
    del sys.modules['threading']
import gevent
import threading
from twython import Twython, TwythonError, TwythonStreamer
import json
from birdie import TwitterBot
from stream import TwitterStreamer


def spawn_stream(line):
    name, con_k, con_s, acc_k, acc_s = line.split("=")[1].split(",")
    return AttackStream(con_k, con_s, acc_k, acc_s)

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
 
def replace_link(text, link):
        replaced = ""        
        for word in text.split():
            if word.startswith("http://") or word.startswith("https://"):
                replaced += link+" "
            else:
                replaced += word+" "
        replaced.strip()
        return replaced



class AttackStream(TwythonStreamer):
    
    LINK = "http://my.link"
    
    def on_success(self, data):
        if 'text' in data:
            text = data['text'].encode('utf-8')
            user = data['user']['screen_name']
            #Replace link with our link
            text = replace_link(text, self.LINK)
            print user+": "+text
    
    def on_error(self, status_code, data):
        self.disconnect()

if __name__ == "__main__":
    stream = get_stream()

# Each stream runs as long as the timeout indicates
# A negative timeout will run indefinitely 

# Generic search terms
stream = get_stream()
keywords = "university of michigan, umich, michigan student, UM student, U-M student, ann arbor student, ann arbor http, U-M http, umichlaw, umalumni, umalumjobs, umicharts, victors2018, victors2019, umichstudybreak, mgopositive, umichengin, innovateblue, umichvictors, umichgradschool"

stream.statuses.filter(track=keywords)

