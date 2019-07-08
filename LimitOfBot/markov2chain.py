#Code for a variation of the markov chain generator that uses nodes of 2 words instead of one
#should function as a dropin replacement for markov.py
import random
import pdb

class InnerNode(object):
    def __init__(self, state):
        self.state = state
        self.count = 1

    def add_count(self):
        self.count += 1

    def __gt__(self, other):
        return self.count > other.count

    def __lt__(self, other):
        return self.count < other.count

    def __ge__(self, other):
        return self.count >= other.count

    def __le__(self, other):
        return self.count <= other.count


class OuterNode(InnerNode):
    def __init__(self, state):
        super(OuterNode, self).__init__(state)
        self.nextstate = list()
        self.count = 0

    def get_next_state(self, rand):
        self.nextstate.sort(reverse=True)
        val = rand(0, self.count)
        for next in self.nextstate:
            if next.count >= val:
                return next
            print("val " + str(val))
            print("count " + str(next.count))
            val -= next.count
        #pdb.set_trace()
        raise RuntimeError("NODE COUNTS INCORRECT")

    def is_in_node(self, target):
        for node in self.nextstate:
            if node.state == target:
                return True
        return False

    def add_state(self, state):
        self.count += 1
        if not self.is_in_node(state):
            self.nextstate.append(InnerNode(state))
            return
        for node in self.nextstate:
            if node.state == state:
                node.add_count()

class MarkovTextGenerator2Node:

    def __init__(self, path=None):
        #ToDo: check if file is readable and writable
        self.start = "@START"
        self.end = "@END"
        self.start_node = OuterNode((None, self.start))
        self.backup = None
        self.chain = dict() #maps tuples to outernodes
        self.chain[(None, self.start)] = self.start_node
        if(path is not None):
            self.backup = open(path, 'a+', encoding='utf-8')
            self.init_from_file(self.backup)

    def close(self):
        if self.backup is not None:
            self.backup.close()

    def init_from_file(self, file):
        file.seek(0,0)
        for line in file:
            self.read_sample(line.split())

    def is_in_chain(self, target):
        for node in self.chain:
            if node == target:
                return True
        return False

    def read_sample(self, sample):
        if (len(sample) < 1):
            return
        first = self.start_node.state
        for part in sample:
            second = (first[1], part)
            if not self.is_in_chain(second):
                self.chain[second] = OuterNode(second)
            self.chain[first].add_state(second)
            first = second
        second = (first[1], self.end)
        self.chain[first].add_state(second)
        if not self.is_in_chain(second):
            self.chain[second] = OuterNode(second)


    def read_save_sample(self, sample):
        if self.backup is not None:
            stringsample = ' '.join(sample) + "\n"
            self.backup.write(stringsample)
        self.read_sample(sample)

    def generate(self, limit, rand):
        current = self.start_node
        text = []
        while limit > 0 and current.state[1] != self.end:
            current = current.get_next_state(rand)
            if len(current.state[1]) > limit or current.state[1] == self.end:
                break
            limit -= (len(current.state[1]) + 1)
            text.append(current.state[1])
            current = self.chain[current.state]
        return u' '.join(text)