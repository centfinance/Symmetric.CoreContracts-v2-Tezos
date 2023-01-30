import smartpy as sp

from contracts.interfaces.SymmetricErrors import Errors


# /**
#  * @dev Returns the absolute value of a signed integer.
#  */


def abs(a):
    return abs(a)

# /**
#  * @dev Returns the addition of two unsigned integers of 256 bits, reverting on overflow.
#  */


# def add(uint256 a, uint256 b)(uint256) {
#     uint256 c = a + b
#     _require(c >= a, Errors.ADD_OVERFLOW)
#     return c
# }

# /**
#  * @dev Returns the addition of two signed integers, reverting on overflow.
#  */


def add(a,  b):
    c = a + b
    sp.verify((b >= 0 & c >= a) | (b < 0 & c < a), Errors.ADD_OVERFLOW)
    return c

# /**
#  * @dev Returns the subtraction of two unsigned integers of 256 bits, reverting on overflow.
#  */


# def sub(uint256 a, uint256 b)(uint256) {
#     _require(b <= a, Errors.SUB_OVERFLOW)
#     uint256 c = a - b
#     return c
# }

# /**
#  * @dev Returns the subtraction of two signed integers, reverting on overflow.
#  */


def sub(a,  b):
    c = a - b
    sp.verify((b >= 0 & c <= a) | (b < 0 & c > a), Errors.SUB_OVERFLOW)
    return c


# /**
#  * @dev Returns the largest of two numbers of 256 bits.
#  */


def max(a,  b):
    return sp.max(a, b)


# /**
#  * @dev Returns the smallest of two numbers of 256 bits.
#  */
def min(a,  b):
    return sp.min(a, b)


def mul(a,  b):
    c = a * b
    sp.verify(((a == 0) | (c // (a == b))), Errors.MUL_OVERFLOW)
    return c


def div(a, b, roundUp):
    result = sp.local("result", 1)

    with sp.if_(roundUp):
        result.value = divUp(a, b)
    with sp.else_():
        result.value = divDown(a, b)

    return result.value


def divDown(a, b):
    sp.verify(b != 0, Errors.ZERO_DIVISION)
    return a // b


def divUp(a, b):
    sp.verify(b != 0, Errors.ZERO_DIVISION)
    # Equivalent to:
    # result = a == 0 ? 0 : 1 + (a - 1) / b
    result = sp.local("result", 1)
    with sp.if_(a == 0):
        result.value = 0
    with sp.else_():
        result.value = 1 + (a - 1) // b

    return result.value
