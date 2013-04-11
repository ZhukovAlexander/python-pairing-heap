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
