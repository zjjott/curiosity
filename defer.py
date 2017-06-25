# coding=utf-8
from __future__ import unicode_literals


class Defer(object):
    """
    Implement Go lang defer keywords
    like demo
    """

    def __init__(self):
        self.waiting = []

    def __call__(self, some_func, *args, **kwargs):
        # stack,LIFO
        self.waiting.insert(0, (some_func, args, kwargs))

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        for func, args, kwargs in self.waiting:
            func(*args, **kwargs)


def print_n(n):
    print n


def test_func():
    print "begin"
    with Defer() as defer:
        for i in range(10):
            defer(print_n, i)
        print "done"

if __name__ == '__main__':
    print test_func.func_code
