#scheduler.py
#event scheduler system. give it a timestamp, a function, and list of arguments
#and it will execute the function with those args at that time.

#all scheduler compatible functions need to take an array of args.

import time

class Scheduler:
    def __init__(self):
        self.events = []

    def addEvent(self, timeoffset, func, args = None):
        targettime = time.perf_counter() + timeoffset
        self.events.append((targettime, func, args))
        self.events.sort(key=lambda t: t[0])

    def sleepTillNext(self):
        targettime, func, args = self.events[0]
        offset = targettime - time.perf_counter()
        if (offset > 0):
            time.sleep(offset)
        func(args)
        del self.events[0]
