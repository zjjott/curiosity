# coding=utf-8
from __future__ import unicode_literals, absolute_import
from fn.fn_engine import TimeCountEngine
import unittest


class TestTimeCountEngine(unittest.TestCase):
    def _test_simple_for_loop(self):

        result = []
        with TimeCountEngine(2) as ctx:
            (ctx.for_loop(range(10))
                .then(lambda x: print("A", x))
             )
        # self.assertListEqual(result, [(i + 1) * 2
            #   for i in range(10)])

    def test_for_loop_then(self):
        """
        按次数分配
        函数:需要运行的次数
        A:10
        B:8
        C:4
        将会按照运行A 5次，B 5次，C 4次 A 5次，B3次 的顺序将他们执行完

        其中，A在语义上等同于：
        for i in range(10):
            x = i + 1
            y = x * 2
            print(y)
        B在语义上等于：
        for i in range(8):

        """
        def f0(x):
            print("f0", x)
            return x + 1

        def f1(x):
            print("f1", x)
            return x * 2

        def f2(x):
            print("f2", x)

        def f3(x):
            print("f3", x)
        with TimeCountEngine(5) as ctx:
            (ctx.for_loop(range(10))
                .then(f0)
                .then(f1)
                .then(f2)
             )
            (ctx.for_loop(range(8))
             .then(f3)
             )
            # (ctx.for_loop(range(4))
            #  .then(lambda x: print("C", x))
            #  )
            # ctx.call(lambda: print("hello"))


def main():
    unittest.main()


if __name__ == '__main__':
    main()
