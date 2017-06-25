# coding=utf-8
from __future__ import unicode_literals, absolute_import


class ContextBase(object):
    def done(self):
        """这个上下文是否已经结束，
        如果已经结束，就会从Engine从踢出去"""
        raise NotImplemented

    def __call__(self):
        """执行这个上下文"""
        raise NotImplemented
