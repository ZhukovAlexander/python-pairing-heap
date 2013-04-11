from heap import Heap
import random
import time
import cProfile
data = [random.randint(1, 2*10**4) for i in range(10**4)]
def run(data):
    heap = Heap()
    sort = []
    start = time.clock()
    for item in data:
        heap.push(item)
    mid = time.clock()
    while heap:
        sort.append(heap.pop())
    end = time.clock()
    print mid-start, end-mid, end-start
    return sort == sorted(data)
run(data)
#cProfile.run('run(data)')
def test():
    s = set(range(10**4))
    t1= time.clock()
    while s:
        s.pop()
    t2= time.clock()
    l = range(10**4)
    t3= time.clock()
    while l:
        l.pop()
    t4= time.clock()
    print t2-t1, t4-t3
test()
def dummy():
    pass
class foo:
    def dummy(self):
        pass

def u():
    f = foo()
    t1 = time.clock()
    for i in range(10000):
        dummy()
    t2 = time.clock()
    for i in range(10000):
        f.dummy()
    t3 = time.clock()
    print t2-t1, t3-t2
u()
