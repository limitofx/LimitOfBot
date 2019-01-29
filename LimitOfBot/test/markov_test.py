import unittest
import os
from .. import MarkovTextGenerator

def mocked_randint_one(a, b):
    return 1
def mocked_randint_zero(a, b):
    return 0
def mocked_randint_seq(a, b, sequence = [1,1,2,4,0]):
    #this is really more to be clever than anything else. exploits single evaluation of default parameters
    for x in sequence:
        sequence.remove(x)
        return x

class markov_test(unittest.TestCase):


    def test_simple_add_gen(self):
        chain1 = MarkovTextGenerator(None)
        #add some strings. no words to filter, that's done at bot level
        #then grab the chain and make sure they appear at the right amounts.
        #will have to be reworked when we make the chain more space efficient through use of counts
        chain1.read_sample("Hello there!".split())
        node_one = chain1.chain["Hello"]
        node_two = chain1.chain["there!"]

        self.assertEqual(node_one.state, "Hello", msg="Node state incorrect")
        self.assertEqual(node_two.state, "there!", msg="Node state incorrect")
        #self.assertEqual(node_one.count, 1, msg="Node count incorrect")
        #self.assertEqual(node_two.count, 1, msg="Node count incorrect")

        self.assertEqual(node_one.nextstate[0].state, "there!", msg="Next state incorrect")
        self.assertEqual(node_two.nextstate[0].state, chain1.end, msg="Next state incorrect")

        result = chain1.generate(50, mocked_randint_zero)
        self.assertEqual(result, "Hello there!")

    def test_complex_add_gen(self):
        chain = MarkovTextGenerator(None)
        #point is to test tweet generation, specifically that if the randomly generated target value
        #is greater than the count of the tested word, it will decrement the target value and try to the next highest one.
        #so build a string where word 2 appears less times than the target value.
        chain.read_sample("bob burger bob burger bob burger bob bean".split())
        result = chain.generate(50, mocked_randint_seq)
        self.assertEqual(result, "bob burger bob bean")

    def test_file_io(self):
        chain = MarkovTextGenerator("test.txt")
        chain.read_save_sample("hello borld".split())
        result1 = chain.generate(20, mocked_randint_zero)
        chain.close()
        del chain
        chain = MarkovTextGenerator("test.txt")
        #should have state of old chain thanks to word store file
        result2 = chain.generate(20, mocked_randint_zero)
        self.assertEqual(result1, result2)
        chain.close()
        del chain
        os.remove("./test.txt")

    def test_write_past_limit(self):
        chain1 = MarkovTextGenerator(None)
        chain1.read_sample("hello world how are you".split())
        result = chain1.generate(11, mocked_randint_zero)
        self.assertEqual(result, "hello world")
        result = chain1.generate(15, mocked_randint_zero)
        self.assertEqual(result, "hello world how")

if __name__ == '__main__':
    unittest.main()