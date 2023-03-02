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


def mulDown(a,  b):
    product = a * b
    return product // ONE


def mulUp(a,  b):
    product = a * b
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

    return sp.as_nat(sp.fst(sp.ediv((product - 1), ONE).open_some()) + 1)


def divDown(a,  b):
    sp.verify(b != 0)
    aInflated = a * ONE
    # mul overflow
    return (aInflated // b)


def divUp(a,  b):
    sp.verify(b != 0)
    aInflated = a * ONE
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
    return (sp.as_nat(aInflated + b - 1)) // b


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

# /**
#  * @dev Returns x^y, assuming both are fixed point numbers, rounding down. The  is guaranteed to not be above
#  * the true value (that is, the error def expected - actual is always positive).
#  */


def powDown(x,  y):
    # Optimize for when y equals 1.0, 2.0 or 4.0, as those are very simple to implement and occur often in 50/50
    # and 80/20 Weighted Pools
    # def mulDown(x, y): return (x*y)//ONE
    powDown = sp.local('powDown', sp.nat(0))
    with sp.if_(y == HALF):
        powDown.value = square_root(x)
    with sp.if_(y == ONE):
        powDown.value = x
    with sp.if_(y == TWO):
        powDown.value = mulDown(x, x)
    with sp.if_(y == FOUR):
        powDown.value = mulDown(mulDown(x, x), mulDown(x, x))

    # with sp.if_((y != ONE) & (y != TWO) & (y != FOUR)):
    #     raw = powu(x, y)
    #     # raw = sp.nat(5)
    #     maxError = mulUp(raw, MAX_POW_RELATIVE_ERROR) + 1
    #     with sp.if_(raw < maxError):
    #         powDown.value = 0
    #     with sp.else_():
    #         powDown.value = sp.as_nat(raw - maxError)

    return powDown.value


def pow(x, y):
    powResult = sp.local('powResult', 1)
    base = sp.local('base', x)
    exponent = sp.local('exponent', y)

    with sp.while_(exponent.value != 0):
        with sp.if_((exponent.value % 2) != 0):
            powResult.value *= base.value

        exponent.value = exponent.value >> 1  # Equivalent to exponent.value / 2
        base.value *= base.value
    return powResult.value


def powUp(x,  y):
    # Optimize for when y equals 1.0, 2.0 or 4.0, as those are very simple to implement and occur often in 50/50
    # and 80/20 Weighted Pools
    powUp = sp.local("result", 1)
    with sp.if_(y == HALF):
        powUp.value = square_root(x)
    with sp.if_(y == ONE):
        powUp.value = x
    with sp.if_(y == TWO):
        powUp.value = mulUp(x, x)
    with sp.if_(y == FOUR):
        square = mulUp(x, x)
        powUp.value = mulUp(square, square)
    # with sp.else_():
    #     raw = pow(x, y)
    #     maxError = add(mulUp(raw, MAX_POW_RELATIVE_ERROR), 1)
    #     result.value = add(raw, maxError)
    return powUp.value

# /**
#  * @dev Returns the complement of a value (1 - x), capped to 0 if x is larger than 1.
#  *
#  * Useful when computing the complement for values with some level of relative error, as it strips this error and
#  * prevents intermediate negative values.
#  */


def complement(x):
    # Equivalent to:
    #  = (x < ONE) ? (ONE - x) : 0;
    result = sp.local("result", 0)
    with sp.if_(x < ONE):
        result.value = ONE - x

    return result.value


def powu(x,  y):
    xAbs = sp.local('xAbs', x)

    # // Calculate the first iteration of the loop in advance.
    resultAbs = sp.local('resultAbs', ONE)
    with sp.if_(y & 1 > 0):
        resultAbs.value = xAbs.value

    # // Equivalent to "for(y /= 2; y > 0; y /= 2)" but faster.
    yAux = sp.local('yAux', y >> 1)
    # with sp.for_(yAux >>= 1; yAux > 0; yAux >>= 1):
    with sp.while_(yAux.value > 0):

        xAbs.value = mulDown(xAbs.value, xAbs.value)
        # // Equivalent to "y % 2 == 1" but faster.
        with sp.if_(yAux.value & 1 > 0):
            resultAbs.value = mulDown(resultAbs.value, xAbs.value)

        yAux.value = yAux.value >> 1

        # // Is the base negative and the exponent an odd number?
    # resultInt = sp.to_int(resultAbs)
    # isNegative = unwrap(x) < 0 && y & 1 == 1;
    # with sp.if_(isNegative):
    #     resultInt = -resultInt;
    sp.trace(resultAbs.value)

    return resultAbs.value
