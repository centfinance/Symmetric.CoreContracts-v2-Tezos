import smartpy as sp
import contracts.interfaces.SymmetricErrors as Errors

# All fixed point multiplications and divisions are inlined. This means we need to divide by ONE when multiplying
# two numbers, and multiply by ONE when dividing them.

# All arguments and return values are 18 decimal fixed point numbers.
ONE_18 = 1000000000000000000
# Internally, intermediate values are computed with higher precision as 20 decimal fixed point numbers, and in the
# case of ln36, 36 decimals.
ONE_20 = 100000000000000000000
ONE_36 = 1000000000000000000000000000000000000

# The domain of natural exponentiation is bound by the word size and number of decimals used.
#
# Because internally the result will be stored using 20 decimals, the largest possible result is
# (2^255 - 1) / 10^20, which makes the largest exponent ln((2^255 - 1) / 10^20) = 130.700829182905140221.
# The smallest possible result is 10^(-18), which makes largest negative argument
# ln(10^(-18)) = -41.446531673892822312.
# We use 130.0 and -41.0 to have some safety margin.
MAX_NATURAL_EXPONENT = 130000000000000000000
MIN_NATURAL_EXPONENT = -41000000000000000000

# Bounds for ln_36's argument. Both ln(0.9) and ln(1.1) can be represented with 36 decimal places in a fixed point
# 256 bit integer.
LN_36_LOWER_BOUND = ONE_18 - 100000000000000000
LN_36_UPPER_BOUND = ONE_18 + 100000000000000000

# MILD_EXPONENT_BOUND = 2**254 // (ONE_20)
MILD_EXPONENT_BOUND = 289480220000000000000000000000000000000000000000000000000
# 18 decimal s
x0 = 128000000000000000000  # 2ˆ7
# eˆ(x0) (no decimals)
a0 = 38877084059945950922200000000000000000000000000000000000
x1 = 64000000000000000000  # 2ˆ6
a1 = 6235149080811616882910000000  # eˆ(x1) (no decimals)

# 20 decimal s
x2 = 3200000000000000000000  # 2ˆ5
a2 = 7896296018268069516100000000000000  # eˆ(x2)
x3 = 1600000000000000000000  # 2ˆ4
a3 = 888611052050787263676000000  # eˆ(x3)
x4 = 800000000000000000000  # 2ˆ3
a4 = 298095798704172827474000  # eˆ(x4)
x5 = 400000000000000000000  # 2ˆ2
a5 = 5459815003314423907810  # eˆ(x5)
x6 = 200000000000000000000  # 2ˆ1
a6 = 738905609893065022723  # eˆ(x6)
x7 = 100000000000000000000  # 2ˆ0
a7 = 271828182845904523536  # eˆ(x7)
x8 = 50000000000000000000  # 2ˆ-1
a8 = 164872127070012814685  # eˆ(x8)
x9 = 25000000000000000000  # 2ˆ-2
a9 = 128402541668774148407  # eˆ(x9)
x10 = 12500000000000000000  # 2ˆ-3
a10 = 113314845306682631683  # eˆ(x10)
x11 = 6250000000000000000  # 2ˆ-4
a11 = 106449445891785942956  # eˆ(x11)


def div(x, y):
    return sp.fst(sp.ediv(x, y).open_some())


# /**
#  * @dev Exponentiation (x^y) with unsigned 18 decimal fixed point base and exponent.
#  *
#  * Reverts if ln(x) * y is smaller than `MIN_NATURAL_EXPONENT`, or larger than `MAX_NATURAL_EXPONENT`.
#  */
def pow(x,  y):
    # We solve the 0^0 indetermination by making it equal one.
    pow = sp.local('pow', 0)
    with sp.if_(y == sp.int_or_nat(0)):
        pow.value = ONE_18

    with sp.if_(x == 0):
        pow.value = 0

    # # Instead of computing x^y directly, we instead rely on the properties of logarithms and exponentiation to
    # # arrive at that result. In particular, exp(ln(x)) = x, and ln(x^y) = y * ln(x). This means
    # # x^y = exp(y * ln(x)).

    # # The ln function takes a signed value, so we need to make sure x fits in the signed 256 bit range.
    sp.verify(((x >> 255) == 0), Errors.X_OUT_OF_BOUNDS)
    x_int = sp.to_int(x)
    # # We will compute y * ln(x) in a single step. Depending on the value of x, we can either use ln or ln_36. In
    # # both cases, we leave the division by ONE_18 (due to fixed point multiplication) to the end.

    # # This prevents y * ln(x) from overflowing, and at the same time guarantees y fits in the signed 256 bit range.
    sp.verify((y < MILD_EXPONENT_BOUND), Errors.Y_OUT_OF_BOUNDS)
    y_int = sp.to_int(y)

    logx_times_y = sp.local('logx_times_y', sp.int(0))
    # with sp.if_((LN_36_LOWER_BOUND < x) & (x < LN_36_UPPER_BOUND)):
    #     ln_36_x = _ln_36(x_int)

    #     # # ln_36_x has 36 decimal places, so multiplying by y isn't as straightforward, since we can't just
    #     # # bring y to 36 decimal places, as it might overflow. Instead, we perform two 18 decimal
    #     # # multiplications and add the results: one with the first 18 decimals of ln_36_x, and one with the
    #     # # (downscaled) last 18 decimals.
    #     logx_times_y.value = (div(ln_36_x, ONE_18) * y_int +
    #                           div((sp.to_int(ln_36_x % ONE_18) * y_int), ONE_18))
    # with sp.else_():
    logx_times_y.value = _ln(x_int) * y_int

    logx_times_y.value = div(logx_times_y.value, ONE_18)

    # # # Finally, we compute exp(y * ln(x)) to arrive at x^y
    sp.verify((MIN_NATURAL_EXPONENT <= logx_times_y.value) & (logx_times_y.value <= MAX_NATURAL_EXPONENT),
              Errors.PRODUCT_OUT_OF_BOUNDS)

    return sp.as_nat(logx_times_y.value)

    # /**
    #  * @dev Natural exponentiation (e^x) with signed 18 decimal fixed point exponent.
    #  *
    #  * Reverts if `x` is smaller than MIN_NATURAL_EXPONENT, or larger than `MAX_NATURAL_EXPONENT`.
    #  */


def exp(x):
    sp.verify(((x >= MIN_NATURAL_EXPONENT) & (x <=
              MAX_NATURAL_EXPONENT)), Errors.INVALID_EXPONENT)
    # We only handle positive exponents: e^(-x) is computed as 1 / e^x. We can safely make x positive since it
    # fits in the signed 256 bit range (as it is larger than MIN_NATURAL_EXPONENT).
    # Fixed point division requires multiplying by ONE_18.
    local_x = sp.local('local_x', x)
    was_less_than_zero = sp.local('was_less_than_zero', False)
    with sp.if_(x < 0):
        was_less_than_zero.value = True
        local_x.value = -x
    # div((ONE_18 * ONE_18), exp(-x))

    # First, we use the fact that e^(x+y) = e^x * e^y to decompose x into a sum of powers of two, which we call x_n,
    # where x_n == 2^(7 - n), and e^x_n = a_n has been precomputed. We choose the first x_n, x0, to equal 2^7
    # because all larger powers are larger than MAX_NATURAL_EXPONENT, and therefore not present in the
    # decomposition.
    # At the end of this process we will have the product of all e^x_n = a_n that apply, and the remainder of this
    # decomposition, which will be lower than the smallest x_n.
    # exp(x) = k_0 * a_0 * k_1 * a_1 * ... + k_n * a_n * exp(remainder), where each k_n equals either 0 or 1.
    # We mutate x by subtracting x_n, making it the remainder of the decomposition.

    # The first two a_n (e^(2^7) and e^(2^6)) are too large if stored as 18 decimal numbers, and could cause
    # intermediate overflows. Instead we store them as plain integers, with 0 decimals.
    # Additionally, x0 + x1 is larger than MAX_NATURAL_EXPONENT, which means they will not both be present in the
    # decomposition.

    # For each x_n, we test if that term.value is present in the decomposition (if x is larger than it), and if so deduct
    # it and compute the accumulated product.

    firstAN = sp.local('firstAn', 0)
    with sp.if_(local_x.value >= x0):
        local_x.value -= x0
        firstAN.value = a0
    with sp.else_():
        with sp.if_(local_x.value >= x1):
            local_x.value -= x1
            firstAN.value = a1
        with sp.else_():
            firstAN.value = 1  # One with no decimal places

    # We now transform local_x.value into a 20 decimal fixed point number, to have enhanced precision when computing the
    # smaller terms.
    local_x.value *= 100

    # `product` is the accumulated product of all a_n (except a0 and a1), which starts at 20 decimal fixed point
    # one. Recall that fixed point multiplication requires dividing by ONE_20.
    product = sp.local('product', ONE_20)

    with sp.if_(local_x.value >= x2):
        local_x.value -= x2
        product.value = div((product.value * a2), ONE_20)

    with sp.if_(local_x.value >= x3):
        local_x.value -= x3
        product.value = div((product.value * a3), ONE_20)

    with sp.if_(local_x.value >= x4):
        local_x.value -= x4
        product.value = div((product.value * a4), ONE_20)

    with sp.if_(local_x.value >= x5):
        local_x.value -= x5
        product.value = div((product.value * a5), ONE_20)

    with sp.if_(local_x.value >= x6):
        local_x.value -= x6
        product.value = div((product.value * a6), ONE_20)

    with sp.if_(local_x.value >= x7):
        local_x.value -= x7
        product.value = div((product.value * a7), ONE_20)

    with sp.if_(local_x.value >= x8):
        local_x.value -= x8
        product.value = div((product.value * a8), ONE_20)

    with sp.if_(local_x.value >= x9):
        local_x.value -= x9
        product.value = div((product.value * a9), ONE_20)

    # x10 and x11 are unnecessary here since we have high enough precision already.

    # Now we need to compute e^x, where x is small (in particular, it is smaller than x9). We use the Taylor series
    # expansion for e^x: 1 + x + (x^2 // 2!) + (x^3 // 3!) + ... + (x^n // n!).

    # The initial one in the sum, with 20 decimal places.
    seriesSum = sp.local('seriesSum', ONE_20)
    # Each term.value in the sum, where the nth term.value is (x^n // n!).

    # The first term.value is simply x.
    term = sp.local('term', x)
    seriesSum.value += term.value

    # Each term.value (x^n // n!) equals the previous one times x, divided by n. Since x is a fixed point number,
    # multiplying by it requires dividing by ONE_20, but dividing by the non-fixed point n values does not.

    term.value = div(div((term.value * local_x.value), ONE_20), 2)
    seriesSum.value += term.value

    term.value = div(div((term.value * local_x.value), ONE_20), 3)
    seriesSum.value += term.value

    term.value = div(div((term.value * local_x.value), ONE_20), 4)
    seriesSum.value += term.value

    term.value = div(div((term.value * local_x.value), ONE_20), 5)
    seriesSum.value += term.value

    term.value = div(div((term.value * local_x.value), ONE_20), 6)
    seriesSum.value += term.value

    term.value = div(div((term.value * local_x.value), ONE_20), 7)
    seriesSum.value += term.value

    term.value = div(div((term.value * local_x.value), ONE_20), 8)
    seriesSum.value += term.value

    term.value = div(div((term.value * local_x.value), ONE_20), 9)
    seriesSum.value += term.value

    term.value = div(div((term.value * local_x.value), ONE_20), 10)
    seriesSum.value += term.value

    term.value = div(div((term.value * local_x.value), ONE_20), 11)
    seriesSum.value += term.value

    term.value = div(div((term.value * local_x.value), ONE_20), 12)
    seriesSum.value += term.value

    # 12 Taylor terms are sufficient for 18 decimal precision.

    # We now have the first a_n (with no decimals), and the product of all other a_n present, and the Taylor
    # approximation of the exponentiation of the remainder (both with 20 decimals). All that remains is to multiply
    # all three (one 20 decimal fixed point multiplication, dividing by ONE_20, and one integer multiplication),
    # and then drop two digits to return an 18 decimal value.
    exp_result = sp.local('exp_result', 0)
    with sp.if_(was_less_than_zero.value):
        exp_result.value = div((ONE_18 * ONE_18), (div((div((product.value * seriesSum.value), ONE_20)
                                                        * firstAN.value), 100)))
    with sp.else_():
        exp_result.value = (div((div((product.value * seriesSum.value), ONE_20)
                                 * firstAN.value), 100))

    return exp_result.value

# #     # /**
# #     #  * @dev Internal natural logarithm (ln(a)) with signed 18 decimal fixed point argument.
# #     #  */


def _ln(a):
    # _ln_result = sp.local('_ln_result', 0)
    localA = sp.local('localA', a)
    with sp.if_(localA.value < ONE_18):
        # Since ln(a^k) = k * ln(a), we can compute ln(a) as ln(a) = ln((1/a)^(-1)) = - ln((1/a)). If a is less
        # than one, 1/a will be greater than one, and this if statement will not be entered in the recursive call.
        # Fixed point division requires multiplying by ONE_18.
        localA.value = -(div((ONE_18 * ONE_18), a))

    # First, we use the fact that ln^(a * b) = ln(a) + ln(b) to decompose ln(a) into a sum of powers of two, which
    # we call x_n, where x_n == 2^(7 - n), which are the natural logarithm of precomputed quantities a_n (that is,
    # ln(a_n) = x_n). We choose the first x_n, x0, to equal 2^7 because the exponential of all larger powers cannot
    # be represented as 18 fixed point decimal numbers in 256 bits, and are therefore larger than a.
    # At the end of this process we will have the sum of all x_n = ln(a_n) that apply, and the remainder of this
    # decomposition, which will be lower than the smallest a_n.
    # ln(a) = k_0 * x_0 + k_1 * x_1 + ... + k_n * x_n + ln(remainder), where each k_n equals either 0 or 1.
    # We mutate a by subtracting a_n, making it the remainder of the decomposition.

    # For reasons related to how `exp` works, the first two a_n (e^(2^7) and e^(2^6)) are not stored as fixed point
    # numbers with 18 decimals, but instead as plain integers with 0 decimals, so we need to multiply them by
    # ONE_18 to convert them to fixed point.
    # For each a_n, we test if that term is present in the decomposition (if a is larger than it), and if so divide
    # by it and compute the accumulated sum.

    sum1 = sp.local('sum1', 0)
    with sp.if_(localA.value >= (a0 * ONE_18)):
        # Integer, not fixed point division
        localA.value = div(localA.value, a0)
        sum1.value += x0

    with sp.if_(localA.value >= (a1 * ONE_18)):
        # Integer, not fixed point division
        localA.value = div(localA.value, a1)
        sum1.value += x1

    # All other a_n and x_n are stored as 20 digit fixed point numbers, so we convert the sum1 and a to this format.
    sum1.value *= 100
    localA.value *= 100

    # Because further a_n are  20 digit fixed point numbers, we multiply by ONE_20 when dividing by them.

    with sp.if_(localA.value >= a2):
        localA.value = div((localA.value * ONE_20), a2)
        sum1.value += x2

    with sp.if_(localA.value >= a3):
        localA.value = div((localA.value * ONE_20), a3)
        sum1.value += x3

    with sp.if_(localA.value >= a4):
        localA.value = div((localA.value * ONE_20), a4)
        sum1.value += x4

    with sp.if_(localA.value >= a5):
        localA.value = div((localA.value * ONE_20), a5)
        sum1.value += x5

    with sp.if_(localA.value >= a6):
        localA.value = div((localA.value * ONE_20), a6)
        sum1.value += x6

    with sp.if_(localA.value >= a7):
        localA.value = div((localA.value * ONE_20), a7)
        sum1.value += x7

    with sp.if_(localA.value >= a8):
        localA.value = div((localA.value * ONE_20), a8)
        sum1.value += x8

    with sp.if_(localA.value >= a9):
        localA.value = div((localA.value * ONE_20), a9)
        sum1.value += x9

    with sp.if_(localA.value >= a10):
        localA.value = div((localA.value * ONE_20), a10)
        sum1.value += x10

    with sp.if_(localA.value >= a11):
        localA.value = div((localA.value * ONE_20), a11)
        sum1.value += x11

    # # a is now a small number (smaller than a_11, which roughly equals 1.06). This means we can use a Taylor series
    # # that converges rapidly for values of `a` close to one - the same one used in ln_36.
    # # Let z = (a - 1) // (a + 1).
    # # ln(a) = 2 * (z + z^3 // 3 + z^5 // 5 + z^7 // 7 + ... + z^(2 * n + 1) // (2 * n + 1))

    # # Recall that 20 digit fixed point division requires multiplying by ONE_20, and multiplication requires
    # # division by ONE_20.
    z = div(((localA.value - ONE_20) * ONE_20), (localA.value + ONE_20))
    z_squared = div((z * z), ONE_20)

    # # num is the numerator of the series: the z^(2 * n + 1) term
    num = sp.local('num', z)

    # seriesSum holds the accumulated sum of each term in the series, starting with the initial z
    seriesSum2 = sp.local('seriesSum2', num.value)

    # In each step, the numerator is multiplied by z^2
    num.value = div((num.value * z_squared), ONE_20)
    seriesSum2.value += div(num.value, 3)

    num.value = div((num.value * z_squared), ONE_20)
    seriesSum2.value += div(num.value, 5)

    num.value = div((num.value * z_squared), ONE_20)
    seriesSum2.value += div(num.value, 7)

    num.value = div((num.value * z_squared), ONE_20)
    seriesSum2.value += div(num.value, 9)

    num.value = div((num.value * z_squared), ONE_20)
    seriesSum2.value += div(num.value, 11)

    # # 6 Taylor terms are sufficient for 36 decimal precision.

    # # Finally, we multiply by 2 (non fixed point) to compute ln(remainder)
    seriesSum2.value *= 2

    # We now have the sum of all x_n present, and the Taylor approximation of the logarithm of the remainder (both
    # with 20 decimals). All that remains is to sum these two, and then drop two digits to sp.result a 18 decimal
    # value.

    return div((sum1.value + seriesSum2.value), 100)

#     # /**
#     #  * @dev Intrnal high precision (36 decimal places) natural logarithm (ln(x)) with signed 18 decimal fixed point argument,
#     #  * for x close to one.
#     #  *
#     #  * Should only be used if x is between LN_36_LOWER_BOUND and LN_36_UPPER_BOUND.
#     #  */


# def _ln_36(x):
#     # // Since ln(1) = 0, a value of x close to one will yield a very small result, which makes using 36 digits
#     # // worthwhile.

#     # // First, we transform x to a 36 digit fixed point value.
#     xLocal = sp.local('xLocal', x)
#     xLocal.value *= ONE_18

#     # // We will use the following Taylor expansion, which converges very rapidly. Let z = (x - 1) / (x + 1).
#     # // ln(x) = 2 * (z + z^3 / 3 + z^5 / 5 + z^7 / 7 + ... + z^(2 * n + 1) / (2 * n + 1))

#     # // Recall that 36 digit fixed point division requires multiplying by ONE_36, and multiplication requires
#     # // division by ONE_36.
#     z = div((xLocal.value - sp.to_int(ONE_36) * sp.to_int(ONE_36)),
#             (xLocal.value + sp.to_int(ONE_36)))
#     z_squared = div((z * z), ONE_36)

#     # // num is the numerator of the series: the z^(2 * n + 1) term
#     num = sp.local('num', z)

#     # // seriesSum holds the accumulated sum of each term in the series, starting with the initial z
#     seriesSum = sp.local('seriesSum', num.value)

#     # // In each step, the numerator is multiplied by z^2
#     num.value = div((num.value * z_squared), ONE_36)
#     seriesSum.value += div(num.value, 3)

#     num.value = div((num.value * z_squared), ONE_36)
#     seriesSum.value += div(num.value, 5)

#     num.value = div((num.value * z_squared), ONE_36)
#     seriesSum.value += div(num.value, 7)

#     num.value = div((num.value * z_squared), ONE_36)
#     seriesSum.value += div(num.value, 9)

#     num.value = div((num.value * z_squared), ONE_36)
#     seriesSum.value += div(num.value, 11)

#     num.value = div((num.value * z_squared), ONE_36)
#     seriesSum.value += div(num.value, 13)

#     num.value = div((num.value * z_squared), ONE_36)
#     seriesSum.value += div(num.value, 15)

#     # // 8 Taylor terms are sufficient for 36 decimal precision.

#     # // All that remains is multiplying by 2 (non fixed point).
#     return (seriesSum.value * 2)
