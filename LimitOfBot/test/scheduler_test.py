import unittest
import os
import time
from .. import Scheduler

#tester functions


class scheduler_test(unittest.TestCase):

    def test_noargs(self):
        results = []
        scheduler = Scheduler()
        scheduler.addEvent(3, lambda x: results.append(10))
        scheduler.addEvent(2, lambda x: results.append(5))
        scheduler.sleepTillNext()
        scheduler.sleepTillNext()
        self.assertEqual(5, results[0])
        self.assertEqual(10, results[1])

    def test_onearg(self):
        results = []
        scheduler = Scheduler()
        scheduler.addEvent(1, lambda x: results.append(x[0]), [1])
        scheduler.addEvent(2, lambda x: results.append(x[0]), [2])
        scheduler.sleepTillNext()
        scheduler.sleepTillNext()
        self.assertEqual(1, results[0])
        self.assertEqual(2, results[1])

    def test_twoarg(self):
        results = []
        scheduler = Scheduler()
        scheduler.addEvent(1, lambda x: results.append(x[0] + x[1]), [1,0])
        scheduler.addEvent(2, lambda x: results.append(x[0] + x[1]), [1,1])
        scheduler.sleepTillNext()
        scheduler.sleepTillNext()
        self.assertEqual(1, results[0])
        self.assertEqual(2, results[1])

    def test_negativetime(self):
        results = []
        scheduler = Scheduler()
        scheduler.addEvent(-10, lambda x: results.append(5))
        beforeTime = time.perf_counter()
        scheduler.sleepTillNext()
        afterTime = time.perf_counter()
        timedelta = afterTime - beforeTime
        self.assertEqual(5, results[0])
        self.assertTrue(timedelta < 1)

if __name__ == '__main__':
    unittest.main()