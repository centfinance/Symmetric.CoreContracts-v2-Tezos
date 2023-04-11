import smartpy as sp

# from contracts.interfaces.SymmetricErrors import Errors
import contracts.utils.math.LogExpMath as LogExpMath

HALF = 500000000000000000

ONE = 1000000000000000000

TWO = 2 * ONE

FOUR = 4 * ONE

MAX_POW_RELATIVE_ERROR = 10000


def add(a, b):
    c = a + b
    sp.verify(c >= a)
    return c


def sub(a,  b):
    # Fixed Point addition is the same as regular checked addition
    sp.verify(b <= a)
    c = a - b
    return sp.as_nat(c)


def mulDown(p):
    product = sp.fst(p) * sp.snd(p)
    sp.result(product // ONE)


def mulUp(p):
    product = sp.fst(p) * sp.snd(p)
    # The traditional divUp formula is:
    # divUp(x, y) := (x + y - 1) / y
    # To avoid intermediate overflow in the addition, we distribute the division and get:
    # divUp(x, y) := (x - 1) / y + 1
    # Note that this requires x != 0, if x == 0 then the  is zero
    #
    # Equivalent to:
    #  = product == 0 ? 0 : ((product - 1) / FixedPoint.ONE) + 1;
    # mulUp = sp.local('mulUp', 0)
    # with sp.if_(product != 0):
    #     mulUp.value = (((sp.as_nat(product - 1)) // ONE) + 1)

    sp.result(sp.as_nat(sp.fst(sp.ediv((product - 1), ONE).open_some()) + 1))


def divDown(p):
    sp.verify(sp.snd(p) != 0)
    aInflated = sp.fst(p) * ONE
    # mul overflow
    sp.result(aInflated // sp.snd(p))


def divUp(p):
    sp.verify(sp.snd(p) != 0)
    aInflated = sp.fst(p) * ONE
    # mul overflo
    # The traditional divUp formula is:
    # divUp(x, y) := (x + y - 1) / y
    # To avoid intermediate overflow in the addition, we distribute the division and get:
    # divUp(x, y) := (x - 1) / y + 1
    # Note that this requires x != 0, if x == 0 then the  is zero
    #
    # Equivalent to:
    #  = a == 0 ? 0 : (a * FixedPoint.ONE - 1) / b + 1;
    # divUp = sp.local("divUp", 0)
    # with sp.if_(a != 0):
    sp.result((sp.as_nat(aInflated + sp.snd(p) - 1)) // sp.snd(p))


def square_root(x):
    """Calculates the square root of a given integer

    Args:
        x : integer whose square root is to be determined
    Returns:
        square root of x
    """

    sp.verify(x >= 0, "Negative_Value")

    y = sp.local('y', x)

    with sp.while_(y.value * y.value > x):

        y.value = (x // y.value + y.value) // 2

    sp.verify((y.value * y.value <= x) & (x < (y.value + 1) * (y.value + 1)))

    return y.value


def nth_root(x, n):
    """Calculates the nth root of a given integer

    Args:
        x: integer whose nth root is to be determined
        n: the degree of the root
    Returns:
        nth root of x
    """

    sp.verify(x >= 0, "Negative_Value")
    sp.verify(n > 0, "Invalid_Root_Degree")

    # Base cases
    with sp.if_(x == 0):
        sp.result(0)
    with sp.if_(n == 1):
        sp.result(x)

    y = sp.local('y', x)

    # Initialization of y
    y.value = x // n

    # Newton-Raphson method
    while True:
        y_next = sp.local('y_next', ((n - 1) * y.value +
                          x // (y.value ** (n - 1))) // n)

        with sp.if_(abs(y_next.value - y.value) <= 1):
            break
        y.value = y_next.value

    sp.verify(y.value ** n <= x)

    return y.value

# /**
#  * @dev Returns x^y, assuming both are fixed point numbers, rounding down. The  is guaranteed to not be above
#  * the true value (that is, the error def expected - actual is always positive).
#  */


def powDown(p):
    # Optimize for when y equals 1.0, 2.0 or 4.0, as those are very simple to implement and occur often in 50/50
    # and 80/20 Weighted Pools
    # def mulDown(x, y): return (x*y)//ONE
    def mul(x, y): return (x * y) // ONE
    def mulUp(x, y): return sp.as_nat(
        sp.fst(sp.ediv(((x * y) - 1), ONE).open_some()) + 1)

    x, y = sp.match_pair(p)

    powDown = sp.local('powDown', sp.nat(0))

    # with sp.if_(y == HALF):
    #     powDown.value = square_root(x)
    with sp.if_(y == ONE):
        powDown.value = x
    with sp.if_(y == TWO):
        powDown.value = mul(x, x)
    with sp.if_(y == FOUR):
        powDown.value = mul(mul(x, x), mul(x, x))

    with sp.if_((y != ONE) & (y != TWO) & (y != FOUR)):
        raw = LogExpMath.power(x, y)

        maxError = mulUp(raw, MAX_POW_RELATIVE_ERROR) + 1
        with sp.if_(raw < maxError):
            powDown.value = 0
        with sp.else_():
            powDown.value = sp.as_nat(raw - maxError)

    sp.result(powDown.value)


def pow(p):
    x, y = sp.match_pair(p)
    powResult = sp.local('powResult', 1)
    base = sp.local('base', x)
    exponent = sp.local('exponent', y)

    with sp.while_(exponent.value != 0):
        with sp.if_((exponent.value % 2) != 0):
            powResult.value *= base.value

        exponent.value = exponent.value >> 1  # Equivalent to exponent.value / 2
        base.value *= base.value

    sp.result(powResult.value)

# /**
#  * @dev Returns x^y, assuming both are fixed point numbers, rounding up. The  is guaranteed to not be below
#  * the true value (that is, the error def expected - actual is always negative).
#  */


def powUp(p):
    # Optimize for when y equals 1.0, 2.0 or 4.0, as those are very simple to implement and occur often in 50/50
    # and 80/20 Weighted Pools
    def mul(x, y): return sp.as_nat(
        sp.fst(sp.ediv(((x * y) - 1), ONE).open_some()) + 1)
    x, y = sp.match_pair(p)

    powUp = sp.local('powUp', 1)
    # with sp.if_(y == HALF):
    #     powUp.value = square_root(x)
    with sp.if_(y == ONE):
        powUp.value = x
    with sp.if_(y == TWO):
        powUp.value = mul(x, x)
    with sp.if_(y == FOUR):
        square = mul(x, x)
        powUp.value = mul(square, square)

    with sp.if_((y != ONE) & (y != TWO) & (y != FOUR)):
        raw = LogExpMath.power(x, y)
        maxError = (mul(raw, MAX_POW_RELATIVE_ERROR) + 1)
        powUp.value = (raw + maxError)

    sp.result(powUp.value)

# /**
#  * @dev Returns the complement of a value (1 - x), capped to 0 if x is larger than 1.
#  *
#  * Useful when computing the complement for values with some level of relative error, as it strips this error and
#  * prevents intermediate negative values.
#  */


def complement(x):
    # Equivalent to:
    #  = (x < ONE) ? (ONE - x) : 0;
    return sp.eif(
        (x < ONE),
        sp.as_nat(ONE - x),
        sp.nat(0,)
    )
