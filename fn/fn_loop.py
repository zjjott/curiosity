# coding=utf-8
from __future__ import unicode_literals, absolute_import
from fn.fn_base import ContextBase
from itertools import product, repeat


class LoopContext(ContextBase):
    """循环的上下文
    关键是：一个循环例如xrange(1)，
    假设我们的时间片跳转是2次执行就跳走
    并且不妨假设每次循环体中有三个待执行函数

    那么时间片在进入循环，取得第一个数值的时候，计数+=1
    执行第一个函数的时候，计数+=1

    此时时间片把上下文切换走了，
    下次回来的时候，应当执行第二个函数计数+1
    第三个函数计数+1

    循环体上下文此时已经done，会从全局上下文中被踢出


    """

    def __init__(self, iterable):
        self.iterable = iterable
        self.fn = []
        self.iter = None
        self.is_done = False

    def _init_iter(self):
        if self.fn:
            for i in self.iterable:
                current = i
                yield current
                for fn in self.fn:
                    current = fn(current)
                    yield current
        else:
            for i in self.iterable:
                yield i

    def __call__(self):
        if self.iter is None:
            self.iter = self._init_iter()
        try:
            ret = next(self.iter)
            return ret
        except StopIteration:
            self.is_done = True

    def done(self):
        """
        >>> a = LoopContext(range(4))
        >>> sum(a)
        4
        循环到头了就是结束了        
        >>> a.is_done()
        True
        """
        return self.is_done

    def then(self, fn):
        """循环里面执行一个函数
        """
        self.fn.append(fn)
        return self
