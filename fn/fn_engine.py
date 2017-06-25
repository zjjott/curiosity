# coding=utf-8
"""实现时间片算法"""
from __future__ import unicode_literals, absolute_import
from fn.fn_loop import LoopContext
from fn.fn_eval import EvalContext
from collections import deque


class TimeSliceEngine(object):

    def __init__(self):
        # 运行上下文保存在这里面，切换时从里面开始切换，里面都应该是可执行的函数
        # 上下文应当是一个可循环、可修改(运行结束的就可以踢出去了)的数据结构
        self.context = deque()

    def run(self):
        """运行核心：
        只要所有上下文没有为空，那么从上下文中取一个出来
        使用具体实现的方法，执行一下
        如果上下文 尚未完结，那么从右边塞回去，继续
        """
        while self.context:
            # 因为是从右边进入的，所以从左侧pop，表达一种FIFO
            this_context = self.context.popleft()
            self.eval_context(this_context)

    def eval_context(self, context):
        raise NotImplemented

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """所以时间调度本质上就是在退出with块的时候开始执行
        """
        self.run()

    def for_loop(self, iterable):
        ctx = LoopContext(
            iterable
        )
        # 从右边加入
        self.context.append(ctx)
        return ctx

    def call(self, fn, *args, **kwargs):
        ctx = EvalContext(fn, *args, **kwargs)
        self.context.append(ctx)
        return ctx


class TimeCountEngine(TimeSliceEngine):
    """
    按次数分配
    函数:需要运行的次数
    A:10
    B:8
    C:4
    将会按照运行A 5次，B 5次，C 4次 A 5次，B3次 的顺序将他们执行完
    """

    def __init__(self, swith_every=1):
        """
        >>>
        """
        self.swith_every = swith_every
        return super(TimeCountEngine, self).__init__()

    def eval_context(self, context):
        count = 0
        while not context.done():
            # 执行一次上下文，然后加一个计数
            context()
            count += 1
            # 运行次数达到了，塞回去，然后break
            if count >= self.swith_every:
                self.context.append(context)
                break
            # 没达到 则继续执行，计数+1
