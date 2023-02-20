import smartpy as sp

# from contracts.interfaces.SymmetricErrors import Errors
import contracts.utils.math.LogExpMath as LogExpMath

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


def mulDown(a,  b):
    product = a * b
    sp.verify(((a == 0) | ((product // a) == b)))
    return product // ONE


def mulUp(a,  b):
    product = a * b
    sp.verify((a == 0) | ((product // a) == b))
    # The traditional divUp formula is:
    # divUp(x, y) := (x + y - 1) / y
    # To avoid intermediate overflow in the addition, we distribute the division and get:
    # divUp(x, y) := (x - 1) / y + 1
    # Note that this requires x != 0, if x == 0 then the  is zero
    #
    # Equivalent to:
    #  = product == 0 ? 0 : ((product - 1) / FixedPoint.ONE) + 1;
    mulUp = sp.local('mulUp', 0)
    with sp.if_(product == 0):
        mulUp.value = 0
    with sp.else_():
        mulUp.value = (((sp.as_nat(product - 1)) // ONE) + 1)

    return mulUp.value


def divDown(a,  b):
    sp.verify(b != 0)
    aInflated = a * ONE
    # mul overflow
    sp.verify((a == 0) | ((aInflated // a) == ONE))
    result = sp.local('result', (aInflated / b))
    return result.value


def divUp(a,  b):
    sp.verify(b != 0)
    aInflated = a * ONE
    # mul overflo
    sp.verify((a == 0) | ((aInflated // a) == ONE))
    # The traditional divUp formula is:
    # divUp(x, y) := (x + y - 1) / y
    # To avoid intermediate overflow in the addition, we distribute the division and get:
    # divUp(x, y) := (x - 1) / y + 1
    # Note that this requires x != 0, if x == 0 then the  is zero
    #
    # Equivalent to:
    #  = a == 0 ? 0 : (a * FixedPoint.ONE - 1) / b + 1;
    result = sp.local("result", 1)
    with sp.if_(a == 0):
        result.value = 0
    with sp.else_():
        result.value = (sp.as_nat((a * ONE) - 1)) // b + 1

    return result.value


def square_root(self, x):
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

    sp.result(y.value)

# /**
#  * @dev Returns x^y, assuming both are fixed point numbers, rounding down. The  is guaranteed to not be above
#  * the true value (that is, the error def expected - actual is always positive).
#  */


def powDown(x,  y):
    # Optimize for when y equals 1.0, 2.0 or 4.0, as those are very simple to implement and occur often in 50/50
    # and 80/20 Weighted Pools
    # def mulDown(x, y): return (x*y)//ONE
    powDown = sp.local('powDown', sp.nat(0))

    with sp.if_(y == ONE):
        powDown.value = x
    with sp.if_(y == TWO):
        powDown.value = mulDown(x, x)
    with sp.if_(y == FOUR):
        powDown.value = mulDown(mulDown(x, x), mulDown(x, x))

    with sp.if_((y != ONE) & (y != TWO) & (y != FOUR)):
        raw = LogExpMath.pow(x, y)
        # raw = sp.nat(5)
        maxError = add(mulUp(raw, MAX_POW_RELATIVE_ERROR), 1)
        with sp.if_(raw < maxError):
            powDown.value = 0
        with sp.else_():
            powDown.value = sub(raw, maxError)

    return powDown.value


# def pow(x, y):
#     powResult = sp.local('powResult', 0)
#     base = sp.local('base', x)
#     exponent = sp.local('exponent', y)

#     with sp.while_(exponent.value != 0):
#         with sp.if_((exponent.value % 2) != 0):
#             powResult.value *= base.value

#         exponent.value = exponent.value >> 1  # Equivalent to exponent.value / 2
#         base.value *= base.value

#     return powResult.value

# /**
#  * @dev Returns x^y, assuming both are fixed point numbers, rounding up. The  is guaranteed to not be below
#  * the true value (that is, the error def expected - actual is always negative).
#  */


def powUp(x,  y):
    # Optimize for when y equals 1.0, 2.0 or 4.0, as those are very simple to implement and occur often in 50/50
    # and 80/20 Weighted Pools
    result = sp.local("result", 1)
    with sp.if_(y == ONE):
        result.value = x
    with sp.if_(y == TWO):
        result.value = mulUp(x, x)
    with sp.if_(y == FOUR):
        square = mulUp(x, x)
        result.value = mulUp(square, square)
    with sp.else_():
        raw = pow(x, y)
        maxError = add(mulUp(raw, MAX_POW_RELATIVE_ERROR), 1)
        result.value = add(raw, maxError)


# /**
#  * @dev Returns the complement of a value (1 - x), capped to 0 if x is larger than 1.
#  *
#  * Useful when computing the complement for values with some level of relative error, as it strips this error and
#  * prevents intermediate negative values.
#  */
def complement(x):
    # Equivalent to:
    #  = (x < ONE) ? (ONE - x) : 0;
    result = sp.local("result", 1)
    with sp.if_(x < ONE):
        result.value = ONE - x
    with sp.else_():
        result.value = 0

    return result.value
