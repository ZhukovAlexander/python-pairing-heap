# Pairing heap-based priority queue/min-heap implementation.
# Copyright (c) 2012 Lars Buitinck.

from collections import namedtuple, deque
from functools import reduce
from llist import dllist

class Heap(object):
    """Min-heap.

    Objects that have been inserted using push can be retrieved in sorted
    order by repeated use of pop or pop_safe.
    """

    __slots__ = ["_root", "_nelems"]

    def __init__(self, items=()):
        self._root = None
        self._nelems = 0

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

    @property
    def top(self):
        """The smallest element of the heap."""
        try:
            return self._root.key
        except AttributeError:
            raise IndexError("min of an empty Heap")


_Node = namedtuple("_Node", "key sub")


def _meld(l, r):
    """Meld (merge) two pairing heaps, destructively."""
    # We deviate from the usual (persistent) treatment of pairing heaps by
    # using list's destructive, amortized O(1) append rather than a "cons".
    if l and r:
        if l.key < r.key:
            l.sub.append(r)
            return l
        else:
            r.sub.append(l)
            return r
    else:   return r or l


def _mpass(heaps):
    #meld = _meld
    """Multipass pairing."""
    if not heaps:return None
    while len(heaps) > 1:
        heaps.appendleft((_meld(heaps.pop(), heaps.pop())))
    #    pairs.append(heaps.pop())
    #return reduce(_meld, pairs, None)
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
    #***WARNING: running time is enormous*** 
    """Singlepass pairing. Came from original version of
    heap. """
    return reduce(_meld, heaps, None)
_pair = _twopass
