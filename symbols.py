def isNumber(x):
    return isinstance(x, (int, long, float))


def isValid(x):
    return isinstance(x, (Symbols, int, long, float))


def isSymbols(x):
    return isinstance(x, Symbols)


class Solution(object):

    def __init__(self, children):
        self.children = children
        self.table = {}
        self.combine()

    def combine(self):
        origin_child = []
        number = filter(isNumber, self.children)
        number = sum(number)
        if number:
            origin_child.append(number)
        symbols = filter(isSymbols, self.children)
        table = self.table
        for child in symbols:
            if child.name in table:
                new_value = table[child.name] + child
                if new_value.value == 0:
                    del table[child.name]
                    continue
                table[child.name] = new_value
            else:
                table[child.name] = child
        origin_child.extend(table.values())
        origin_child.sort()
        self.children = origin_child

    @property
    def solution(self):
        symbols = filter(isSymbols, self.children)
        assert len(symbols) == 1
        number = filter(isNumber, self.children)
        number = sum(number)
        symbol = symbols[0]
        # move number from left to right
        return {symbol.name: -number / symbol.value}


class SymbolsTuple(Solution):

    def __str__(self):
        """
        >>> str(SymbolsTuple([1,2,3]))
        'SymbolsTuple(6)'
        """
        s = []
        for index, child in enumerate(self.children):
            if isSymbols(child):
                value = child.value
            else:
                value = child
            if index:
                s.append("+%s" % child if value > 0 else "%s" % child)
            else:
                s.append("%s" % child)

        return "SymbolsTuple(%s)" % "".join(s)

    def __repr__(self):
        return 'SymbolsTuple([%s])' % (
            ",".join([repr(child)
                      for child in self.children]))

    def __len__(self):
        return len(self.children)

    def __eq__(self, other):
        if isinstance(other, SymbolsTuple):
            return Solution(self.children + [
                -child for child in other.children])
        elif isValid(other):
            # move other from left to right
            return Solution(self.children + [-other])

    def __add__(self, other):
        """
        >>> Symbols("x")+3+5+Symbols("x")
        SymbolsTuple([Symbols("x",2),8])
        """
        if isinstance(other, (Symbols, int, long)):
            result = SymbolsTuple(self.children + [other])
            return result
        elif isinstance(other, SymbolsTuple):
            result = SymbolsTuple(self.children + other.children)
            return result
        else:
            raise ValueError(
                "TypeError: cannot "
                "concatenate 'Symbols' and '%s' objects" % type(
                    other))

    def __neg__(self):
        """
        >>> -SymbolsTuple([Symbols("x",2),8])
        SymbolsTuple([Symbols("x",-2),-8])
        """
        return SymbolsTuple([-child for child in self.children])

    def __sub__(self, other):
        if isinstance(other, (Symbols, int, long)):
            result = SymbolsTuple(self.children + [-other])
            return result
        elif isinstance(other, SymbolsTuple):
            result = SymbolsTuple(
                self.children + [-child for child in other.children])
            return result
        else:
            raise ValueError(
                "TypeError: cannot "
                "concatenate 'Symbols' and '%s' objects" % type(
                    other))

    def __mul__(self, other):
        """
        >>> (Symbols("x")+3)*2
        SymbolsTuple([Symbols("x",2),6])
        """
        if isNumber(other):
            result = SymbolsTuple([child * other for child in self.children])
            return result
        else:
            raise ValueError(
                "TypeError: cannot "
                "concatenate 'Symbols' and '%s' objects" % type(
                    other))

    def __rmul__(self, other):
        """
        >>> 2*(Symbols("x")+3)
        SymbolsTuple([Symbols("x",2),6])
        """
        return self * other

    def __div__(self, other):
        """
        >>> (Symbols("x")+3)/2.0
        SymbolsTuple([Symbols("x",0.5),1.5])
        """
        if isNumber(other):
            result = SymbolsTuple([child / other for child in self.children])
            return result
        else:
            raise ValueError(
                "TypeError: cannot "
                "concatenate 'Symbols' and '%s' objects" % type(
                    other))


class Symbols(object):
    """Simple Symbols lol..."""
    __slot__ = ['name', 'value']

    def __new__(self, name, value=1):
        if value == 0:
            return 0
        return super(Symbols, self).__new__(self, name, value)

    def __init__(self, name, value=1):
        self.name = name
        self.value = value  # coefficient

    def __str__(self):
        """
        >>> str(Symbols("x", 1))
        'x'
        >>> str(Symbols("x", 2))
        '2x'
        """
        if self.value == 1:
            return "%s" % self.name
        elif self.value == -1:
            return "-%s" % self.name
        else:
            return "%s%s" % (self.value, self.name)

    def __gt__(self, other):
        """
        >>> Symbols("x")>0
        False
        """
        if isNumber(other):
            return False  # use by sort, always before number in SymbolsTuple
        elif isSymbols(other):
            return self.name > other.name
        else:
            raise ValueError("can not compare which is bigger")

    def __lt__(self, other):
        return not (self > other)

    def __eq__(self, other):
        """
        >>> Symbols("x") == Symbols("x")
        True
        >>> Symbols("x",1) != Symbols("x",2)
        True
        >>> Symbols("x") != Symbols("y")
        True
        """
        if isinstance(other, Symbols):
            return other.name == self.name and other.value == self.value
        elif isNumber(other):
            return Solution([self, other])
        else:
            return False

    def __add__(self, other):
        """
        >>> Symbols("x",1) + Symbols("x",2)
        Symbols("x",3)
        """
        if not isValid(other):
            raise ValueError(
                "TypeError: cannot add 'Symbols' and '%s' objects" % type(
                    other))
        if isinstance(other, Symbols):
            if self.name == other.name:
                return Symbols(self.name, self.value + other.value)
        return SymbolsTuple([self, other])

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        """
        >>> Symbols("x",1) - Symbols("x",2)
        Symbols("x",-1)
        """
        if not isValid(other):
            raise ValueError(
                "TypeError: cannot sub 'Symbols' and '%s' objects" % type(
                    other))
        if isinstance(other, Symbols):
            if self.name == other.name:
                return Symbols(self.name, self.value - other.value)
        return SymbolsTuple([self, -other])

    def __rsub__(self, other):
        """
        >>> 2-Symbols("x",1)
        SymbolsTuple([Symbols("x",-1),2])
        """
        return -(self - other)

    def __rmul__(self, other):
        return self * other

    def __neg__(self):
        """
        >>> -Symbols("x",2)
        Symbols("x",-2)
        """
        return Symbols(self.name, -self.value)

    def __mul__(self, other):
        """
        >>> Symbols("x",2) * 4
        Symbols("x",8)
        """
        if not isNumber(other):
            raise ValueError(
                "TypeError: cannot multi 'Symbols' and '%s' objects" % type(
                    other))
        return Symbols(self.name, self.value * other)

    def __repr__(self):
        if self.value == 1:
            return 'Symbols("%s")' % self.nameself.value,
        else:
            return 'Symbols("%s",%s)' % (self.name, self.value)

    def __div__(self, other):
        """
        >>> Symbols("x",2) / 4.0
        Symbols("x",0.5)
        """
        if not isNumber(other):
            raise ValueError(
                "TypeError: cannot div 'Symbols' and '%s' objects" % type(
                    other))
        return Symbols(self.name, self.value / other)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    x = Symbols("x")
    print(x * 2 + 1 == 8.0 * x + 6).solution
