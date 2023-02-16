import smartpy as sp

# from contracts.interfaces.SymmetricErrors import Errors

ONE = 1000000000000000000

TWO = 2 * ONE

FOUR = 4 * ONE

MAX_POW_RELATIVE_ERROR = 10000


def add(a, b):
    c = a + b
    sp.verify(c > + a)
    return c


def sub(a,  b):
    # Fixed Point addition is the same as regular checked addition
    sp.verify(b <= a, Errors.SUB_OVERFLOW)
    c = a - b
    return c


def mulDown(a,  b):
    product = a * b
    sp.verify(((a == 0) | (product // (a == b))), Errors.MUL_OVERFLOW)
    result = sp.local('result', (product / ONE))
    return result.value


def mulUp(a,  b):
    product = a * b
    sp.verify((a == 0) | ((product // a) == b), Errors.MUL_OVERFLOW)
    # The traditional divUp formula is:
    # divUp(x, y) := (x + y - 1) / y
    # To avoid intermediate overflow in the addition, we distribute the division and get:
    # divUp(x, y) := (x - 1) / y + 1
    # Note that this requires x != 0, if x == 0 then the  is zero
    #
    # Equivalent to:
    #  = product == 0 ? 0 : ((product - 1) / FixedPoint.ONE) + 1;
    result = sp.local("result", 1)
    with sp.if_(product == 0):
        result.value = 0
    with sp.else_():
        result.value = (((product - 1) // ONE) + 1)

    return result.value


def divDown(a,  b):
    sp.verify(b != 0, Errors.ZERO_DIVISION)
    aInflated = a * ONE
    # mul overflow
    sp.verify((a == 0) | ((aInflated // a) == ONE), Errors.DIV_INTERNAL)
    result = sp.local('result', (aInflated / b))
    return result.value


def divUp(a,  b):
    sp.verify(b != 0, Errors.ZERO_DIVISION)
    aInflated = a * ONE
    # mul overflo
    sp.verify((a == 0) | ((aInflated // a) == ONE), Errors.DIV_INTERNAL)
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
        result.value = (a * ONE - 1) // b + 1

    return result.value


# /**
#  * @dev Returns x^y, assuming both are fixed point numbers, rounding down. The  is guaranteed to not be above
#  * the true value (that is, the error def expected - actual is always positive).
#  */
def powDown(x,  y):
    # Optimize for when y equals 1.0, 2.0 or 4.0, as those are very simple to implement and occur often in 50/50
    # and 80/20 Weighted Pools
    result = sp.local("result", 1)
    with sp.if_(y == ONE):
        result.value = x
    with sp.if_(y == TWO):
        result.value = mulDown(x, x)
    with sp.if_(y == FOUR):
        square = (mulDown(x, x))
        result.value = mulDown(square, square)
    with sp.else_():
        raw = pow(x, y)
        maxError = add(mulUp(raw, MAX_POW_RELATIVE_ERROR), 1)
        with sp.if_(raw < maxError):
            result.value = 0
        with sp.else_():
            result.value = sub(raw, maxError)

    return result.value


def pow(x, y):
    result = sp.local("result", 1)
    base = sp.local("base", x)
    exponent = sp.local("exponent", y)

    with sp.while_(exponent.value != 0):
        with sp.if_((exponent.value % 2) != 0):
            result.value *= base.value

        exponent.value = exponent.value >> sp.nat(
            1)  # Equivalent to exponent.value / 2
        base.value *= base.value

    return result.value

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
