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
        #print(val)
        for next in self.nextstate:
            if next.count >= val:
                return next
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

#Has a dict that matches words to outernodes, uses outernodes to find the next word.
class MarkovTextGenerator:

    def __init__(self, path=None):
        #ToDo: check if file is readable and writable
        self.start = "@START"
        self.end = "@END"
        self.start_node = OuterNode(self.start)
        self.end_node = OuterNode(self.end)
        self.backup = None
        self.chain = dict() #maps strings to outernodes
        self.chain[self.start] = self.start_node
        self.chain[self.end] = self.end_node
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

    #read sample of text and add to chain
    def read_sample(self, sample):
        #assuming sample is a list
        if(len(sample) == 0):
            return
        first = self.start_node.state
        for second in sample:
            if not self.is_in_chain(first):
                self.chain[first] = OuterNode(first)
            node = self.chain[first]
            node.add_state(second)
            first = second
        second = self.end
        if not self.is_in_chain(first):
            self.chain[first] = OuterNode(first)
        node = self.chain[first]
        node.add_state(second)

    #read sample of text, add to chain, and save to store file
    def read_save_sample(self, sample):
        if self.backup is not None:
            stringsample = ' '.join(sample) + "\n"
            self.backup.write(stringsample)
        self.read_sample(sample)

    #generate limit characters of text
    def generate(self, limit, rand):
        current = self.start_node
        text = []
        while limit > 0 and current != self.end_node:
            current = current.get_next_state(rand)
            if len(current.state) > limit or current.state == self.end:
                break
            limit -= (len(current.state) + 1)
            text.append(current.state)
            current = self.chain[current.state]
        return u' '.join(text)

    def is_in_chain(self, target):
        for node in self.chain:
            if node == target:
                return True
        return False
