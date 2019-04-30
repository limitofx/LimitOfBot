#scheduler.py
#event scheduler system. give it a timestamp, a function, and additional arguments.
#and it will execute the function with those args at that time.

#all scheduler compatible functions need to take a tuple of args.

import time
import logging

#logfilename = "logs/sched.log"

class Scheduler:
    def __init__(self):
        self.events = []
        #logging.basicConfig(filename=logfilename, level=logging.INFO)
        #logging.basicConfig(format='%(asctime)s %(message)s')
        #logging.info("Starting up!")

    def addEvent(self, timeoffset, func, args = None):
        targettime = time.perf_counter() + timeoffset
        self.events.append((targettime, func, args))
        self.events.sort(key=lambda t: t[0])
        logging.info("Add event to execute " + func.__name__ + " in " + str(timeoffset) + "s")

    def sleepTillNext(self):
        targettime, func, args = self.events[0]
        offset = targettime - time.perf_counter()
        if (offset > 0):
            time.sleep(offset)
        func(args)
        logging.info("Performed " + func.__name__ + " event!")
        logging.info("Events in queue: " + str(len(events)))
        del self.events[0]
