# coding=utf-8
from __future__ import unicode_literals, absolute_import
from fn.fn_base import ContextBase


class EvalContext(ContextBase):
    """延后执行context"""

    def __init__(self, fn, *args, **kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.is_done = False

    def __call__(self, *args, **kwargs):
        kwargs.update(self.kwargs)
        result = self.fn(*(args + self.args), **kwargs)
        self.is_done = True
        return result

    def done(self):
        """函数执行完了就是结束了"""
        return self.is_done
