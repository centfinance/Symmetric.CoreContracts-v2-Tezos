import smartpy as sp

import contracts.utils.math.LogExpMath as LogExpMath

HALF = 500000000000000000

ONE = 1000000000000000000

TWO = 2 * ONE

FOUR = 4 * ONE

MAX_POW_RELATIVE_ERROR = 10000


def mulDown(p):
    """
    Multiplies two numbers and scales down by ONE.
    
    Args:
        p: Tuple containing the two numbers to be multiplied.
        
    Returns:
        Product of the numbers scaled down.
    """
    product = sp.fst(p) * sp.snd(p)
    sp.result(product // ONE)


def mulUp(p):
    """
    Multiply the values of a pair and round up the result.
    
    :param p: A tuple (pair) of two numbers
    :return: Rounded up product of the two numbers
    """
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
    """
    Divide the first value of a pair by the second and round down the result.
    
    :param p: A tuple (pair) of two numbers where the second number is non-zero
    :return: Rounded down division result
    """
    sp.verify(sp.snd(p) != 0)
    aInflated = sp.fst(p) * ONE
    # mul overflow
    sp.result(aInflated // sp.snd(p))


def divUp(p):
    """
    Divide the first value of a pair by the second and round up the result.
    
    :param p: A tuple (pair) of two numbers where the second number is non-zero
    :return: Rounded up division result
    """
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


def complement(x):
    """
    Returns the complement of a value (1 - x), capped to 0 if x is larger than 1.
    
    Args:
        x: Integer whose complement is to be found.
        
    Returns:
        Complement of x.
    """
    # Equivalent to:
    #  = (x < ONE) ? (ONE - x) : 0;
    return sp.eif(
        (x < ONE),
        sp.as_nat(ONE - x),
        sp.nat(0,)
    )
