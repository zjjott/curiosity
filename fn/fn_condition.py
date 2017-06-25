# coding=utf-8
from __future__ import unicode_literals, absolute_import
from fn.fn_base import ContextBase


class ConditionContext(ContextBase):
    def __init__(self, ctx, condition_fn,
                 true_fn, false_fn):
        self.is_done = False

    def __call__(self):
        if self.condition_fn():
            self.true_fn()
        else:
            self.false_fn()
        self.is_done = True

    def done(self):
        return self.is_done
