import tweepy
import time, signal, sys, datetime
import logging
import random
import pdb
from markov import MarkovTextGenerator
#create file in this directory with the twitter keys and tokens
from access import consumer_key, consumer_secret, access_token, access_token_secret
from scheduler import Scheduler

#structure:
#sleep event looop
#keep a list of events. sleep until the next event.
#A check tweets and replies happens every 5 minutes
#A create new tweet event happens somewherew between every 20 and 40 minutes.

#and when i implement replies, they can be scheduled after a tweet and reply check.

#how the scheduler works:
#bot will do the current task, schedule new ones, then sleep until next event.
#the bot will maintain a list of ints representing millisecond timestamps
#whena  new event is scheduled, it will take the time to the next event, convert to ms, and add the current timer's timestamp
#when it's time to wait for the next event, it will sleep (next event timestamp - current timer) ms

#be sure to add better logging!
logfilename = "logs/bot.log"
words_store = "words.txt"
idfile = "latest.id"
chain = None
latestid = 0
account_name = "LimitOfBot"
#bot reads all non retweeted statuses it gets from people it follows
laststatus = ""

def main():
    global chain
    chain, api, latestidfile, events = initialize()
    count = 10
    events.addEvent(30, readTweets, [chain, api, latestidfile, events])
    events.addEvent(60, createTweet, [chain, api, events])
    try:
        while(events.events):
            events.sleepTillNext()
            logging.info("Event executed!")
    except Exception as e:
        logging.error("EXCEPTION: AN EXCEPTION HAS OCCURRED AT " + str(datetime.datetime.now()))
        logging.error("EXCEPTION: {0}\n".format(str(e)))
    logging.info("No longer processing events as of" + str(datetime.datetime.now()))
    terminate(0, None)


def initialize():
    #create chain and api obj
    chain = MarkovTextGenerator(words_store)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    #setup id file and event scheduler
    latestidfile = open(idfile, 'r+')
    events = Scheduler()

    #setup logger
    logging.basicConfig(filename=logfilename, level=logging.INFO)
    logging.basicConfig(format='%(asctime)s %(message)s')
    logging.info("Starting up!")

    #function to run when terminating program
    signal.signal(signal.SIGTERM, terminate)
    return chain, api, latestidfile, events
    
def terminate(signum, frame):
    #could i get the chain from the frame?
    global chain
    chain.close()
    logging.info("Shutting down!")
    sys.exit(1)


#from here on are functions that the scheduler will execute. They must take precisely one arg

#expected args [chain, api, latestid, events]
def readTweets(args):
    chain = args[0]
    api = args[1]
    latestidfile = args[2]
    events = args[3]
    latestid = int(latestidfile.read())
    count = 3200
    newid = latestid
    for status in api.home_timeline(since_id=latestid, count=count, tweet_mode='extended'):
        if(status.id > newid):
            newid = status.id
        if(status.full_text.startswith("RT @")):
            continue
        if(status.user.name == account_name):
            continue
        if(status.is_quote_status):
            status.full_text = ' '.join(status.full_text.split(' ')[:-1])
        if(status.id == latestid):
            break #reached tweets already read.
        status = status.full_text
        status_parts = status.split()
        status_parts = list(filter(lambda x : not x.startswith('@') and not x.startswith('#'), status_parts))
        #pdb.set_trace()
        chain.read_save_sample(status_parts)
    latestid = newid
    latestidfile.seek(0)
    latestidfile.write(str(newid))
    latestidfile.truncate()
    latestidfile.seek(0)
    events.addEvent(1800, readTweets, [chain, api, latestidfile, events])
    logging.info("read tweets at " + str(datetime.datetime.now()))

#[chain, api, events]
def createTweet(args):
    global laststatus
    chain = args[0]
    api = args[1]
    events = args[2]
    status = chain.generate(240, random.randint)
    if (status == laststatus):
        status = chain.generate(240, random.randint)
    try:
        api.update_status(status)
        laststatus = status
    except Exception as e:
        logging.error("status: " + status + "\n")
        logging.error("laststatus: " + laststatus + "\n")
        logging.error("error : " + str(e) + "\n")
        terminate(None, None)
    events.addEvent(1800, createTweet, [chain, api, events])
    logging.info("send tweets at " + str(datetime.datetime.now()))

#[api]
def checkNotifs(args):
    pass
    logging.info("read notifs")

#[chain, api]
def sendReply(args):
    pass
    logging.info("sent reply")

def printTest(args):
    print("event happened")
    logging.info("test occurred")

#[chain]
def printTweet(args):
    chain = args[0]
    status = chain.generate(240, random.randint)
    print(status)
    logging.info("tweet printed to console")

if __name__ == '__main__':
    main()
