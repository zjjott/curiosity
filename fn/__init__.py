# coding=utf-8
from __future__ import unicode_literals
"""
    >>> with TimeCountEngine(2) as ctx:
    >>>     ctx.for_loop(range(10), lambda x: print("A", x))
    >>>     ctx.for_loop(range(8), lambda x: print("B", x))
    >>>     ctx.for_loop(range(4), lambda x: print("C", x))
"""
