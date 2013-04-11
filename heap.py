# Pairing heap-based priority queue/min-heap implementation.
# Copyright (c) 2012 Lars Buitinck.

from collections import namedtuple, deque
from functools import reduce
from llist import dllist
from rcdtype import *

class Heap(object):
    """Min-heap.

    Objects that have been inserted using push can be retrieved in sorted
    order by repeated use of pop or pop_safe.
    """

    __slots__ = ["_root", "_nelems", "_map"]

    def __init__(self, items=()):
        self._root = None
        self._nelems = 0
        self._map = {}
        for x in items:
            self.push(x)

    def __iadd__(self, other):
        """Merge other into self, destroying other in the process."""

        self._root = _meld(self._root, other._root)
        self._nelems += other._nelems

        other._root = None
        other._nelems = 0

        return self

    def __len__(self):
        return self._nelems

    def _pop(self):
        r = self._root.key
        self._root = _pair(self._root.sub)
        self._nelems -= 1
        return r

    def pop(self):
        """Remove the smallest element from the heap and return it.

        Raises IndexError when the heap is empty.
        """
        try:
            return self._pop()
        except AttributeError:
            raise IndexError("pop from an empty Heap")

    def pop_safe(self):
        """Like pop, but returns None when the heap is empty."""
        return self._root and self._pop()

    def push(self, x):
        """Push element x onto the heap."""
        self._root = _meld(self._root, _Node(x, dllist()))
        self._nelems += 1
        if x is not self._root.key:      #returns ref to dllistnode
            return self._root.sub.last   #in which x is now

    def decreasekey(self, node, newkey):
        #assert newkey < node.value.key
        if not node:                    #decreasing key of the root, so
            self._root.key = newkey     #simply change its key to newkey
            return
        parent = node.value.parent
        newheap = parent.sub.remove(node) #removes ref to node from its parent
        newheap.key = newkey
        self._root = _meld(self._root, newheap)
        if newkey is not self._root.key:  #as above
            return self._root.sub.last
        
    @property
    def root(self):
        """The smallest element of the heap."""
        try:
            return self._root.key
        except AttributeError:
            raise IndexError("min of an empty Heap")

class _Node(object):
    __slots__ = ('key', 'sub', 'parent')
    def __init__(self, key, sub):
        self.key = key
        self.sub = sub
        self.parent = None
        
def _meld(l, r):
    """Meld (merge) two pairing heaps, destructively."""
    # We deviate from the usual (persistent) treatment of pairing heaps by
    # using list's destructive, amortized O(1) append rather than a "cons".
    if l and r:
        if l.key < r.key:
            r.parent = l
            l.sub.append(r)
            return l
        else:
            l.parent = r
            r.sub.append(l)
            return r
    else:   return r or l


def _mpass(heaps):
    """Multipass pairing."""
    if not heaps:return None
    while len(heaps) > 1:
        heaps.appendleft((_meld(heaps.pop(), heaps.pop())))
    return heaps.pop()

def _twopass(heaps):
    """Twopass pairing."""
    pairs = []
    while len(heaps) > 1:
        pairs.append((_meld(heaps.pop(), heaps.pop())))
    if heaps:
        pairs.append(heaps.pop())
    return reduce(_meld, pairs, None)

def _spass(heaps):
    """Singlepass pairing."""
    return reduce(_meld, heaps, None)

_pair = _twopass


