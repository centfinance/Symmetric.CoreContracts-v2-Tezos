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
        y_next = sp.local('y_next', ((n - 1) * y.value + x // (y.value ** (n - 1))) // n)

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
    x, y = sp.match_pair(p)
    powDown = sp.local('powDown', sp.nat(0))
    with sp.if_(y == HALF):
        powDown.value = square_root(x)
    with sp.if_(y == ONE):
        powDown.value = x
    with sp.if_(y == TWO):
        powDown.value = mul(x, x)
    with sp.if_(y == FOUR):
        powDown.value = mul(mul(x, x), mul(x, x))

    # with sp.if_((y != ONE) & (y != TWO) & (y != FOUR)):
    #     raw = powu(x, y)
    #     # raw = sp.nat(5)
    #     maxError = mulUp(raw, MAX_POW_RELATIVE_ERROR) + 1
    #     with sp.if_(raw < maxError):
    #         powDown.value = 0
    #     with sp.else_():
    #         powDown.value = sp.as_nat(raw - maxError)

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
    with sp.if_(y == HALF):
        powUp.value = square_root(x)
    with sp.if_(y == ONE):
        powUp.value = x
    with sp.if_(y == TWO):
        powUp.value = mul(x, x)
    with sp.if_(y == FOUR):
        square = mul(x, x)
        powUp.value = mul(square, square)
    # with sp.else_():
    #     raw = pow(x, y)
    #     maxError = add(mulUp(raw, MAX_POW_RELATIVE_ERROR), 1)
    #     result.value = add(raw, maxError)
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
    complement = sp.local('complement', 0)
    with sp.if_(x < ONE):
        complement.value = sp.as_nat(ONE - x)

    return complement.value


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

        xAbs.value = mulDown((xAbs.value, xAbs.value))
        sp.trace(xAbs.value)
        # // Equivalent to "y % 2 == 1" but faster.
        with sp.if_(yAux.value & 1 > 0):
            resultAbs.value = mulDown((resultAbs.value, xAbs.value))

        yAux.value = yAux.value >> 1

        # // Is the base negative and the exponent an odd number?
    # resultInt = sp.to_int(resultAbs)
    # isNegative = unwrap(x) < 0 && y & 1 == 1;
    # with sp.if_(isNegative):
    #     resultInt = -resultInt;

    return resultAbs.value


UNIT = sp.nat(1000000000000000000)


def prbExp2(x):
    prbexp2_result = sp.local('prbexp2_result', sp.nat(0x800000000000000000000000000000000000000000000000))

    conditions = [
        (0xFF00000000000000, [
            (0x8000000000000000, 0x16A09E667F3BCC909),
            (0x4000000000000000, 0x1306FE0A31B7152DF),
            (0x2000000000000000, 0x1172B83C7D517ADCE),
            (0x1000000000000000, 0x10B5586CF9890F62A),
            (0x800000000000000, 0x1059B0D31585743AE),
            (0x400000000000000, 0x102C9A3E778060EE7),
            (0x200000000000000, 0x10163DA9FB33356D8),
            (0x100000000000000, 0x100B1AFA5ABCBED61)
        ]),
        (0xFF000000000000, [
            (0x80000000000000, 0x10058C86DA1C09EA2),
            (0x40000000000000, 0x1002C605E2E8CEC50),
            (0x20000000000000, 0x100162F3904051FA1),
            (0x10000000000000, 0x1000B175EFFDC76BA),
            (0x8000000000000, 0x100058BA01FB9F96D),
            (0x4000000000000, 0x10002C5CC37DA9492),
            (0x2000000000000, 0x1000162E525EE0547),
            (0x1000000000000, 0x10000B17255775C04)
        ]),
        (0xFF0000000000, [
            (0x800000000000, 0x1000058B91B5BC9AE),
            (0x400000000000, 0x100002C5C89D5EC6D),
            (0x200000000000, 0x10000162E43F4F831),
            (0x100000000000, 0x100000B1721BCFC9A),
            (0x80000000000, 0x10000058B90CF1E6E),
            (0x40000000000, 0x1000002C5C863B73F),
            (0x20000000000, 0x100000162E430E5A2),
            (0x10000000000, 0x1000000B172183551)
        ]),
        (0xFF00000000, [
            (0x8000000000, 0x100000058B90C0B49),
            (0x4000000000, 0x10000002C5C8601CC),
            (0x2000000000, 0x1000000162E42FFF0),
            (0x1000000000, 0x10000000B17217FBB),
            (0x800000000, 0x1000000058B90BFCE),
            (0x400000000, 0x100000002C5C85FE3),
            (0x200000000, 0x10000000162E42FF1),
            (0x100000000, 0x100000000B17217F8)
        ]),
        (0xFF000000, [
            (0x80000000, 0x10000000058B90BFC),
            (0x40000000, 0x1000000002C5C85FE),
            (0x20000000, 0x100000000162E42FF),
            (0x10000000, 0x1000000000B17217F),
            (0x8000000, 0x100000000058B90C0),
            (0x4000000, 0x10000000002C5C860),
            (0x2000000, 0x1000000000162E430),
            (0x1000000, 0x10000000000B17218)
        ]),
        (0xFF0000, [
            (0x800000, 0x1000000000058B90C),
            (0x400000, 0x100000000002C5C86),
            (0x200000, 0x10000000000162E43),
            (0x100000, 0x100000000000B1721),
            (0x80000, 0x10000000000058B91),
            (0x40000, 0x1000000000002C5C8),
            (0x20000, 0x100000000000162E4),
            (0x10000, 0x1000000000000B172)
        ]),
        (0xFF00, [
            (0x8000, 0x100000000000058B9),
            (0x4000, 0x10000000000002C5D),
            (0x2000, 0x1000000000000162E),
            (0x1000, 0x10000000000000B17),
            (0x800, 0x1000000000000058C),
            (0x400, 0x100000000000002C6),
            (0x200, 0x10000000000000163),
            (0x100, 0x100000000000000B1)
        ]),
        (0xFF0, [
            (0x80, 0x10000000000000059),
            (0x40, 0x1000000000000002C),
            (0x20, 0x10000000000000016),
            (0x10, 0x1000000000000000B),
            (0x8, 0x10000000000000006),
            (0x4, 0x10000000000000003),
            (0x2, 0x10000000000000001),
            (0x1, 0x10000000000000001)
        ]),    
    ]

    with sp.for_('conditon',  conditions) as condition:
        mask, subconditions = sp.match_pair(condition)
        with sp.if_((x & mask) > 0):
            with sp.for_('subcondition', subconditions) as subcondition:
                submask, factor = sp.match_pair(subcondition)
                with sp.if_((x & submask) > 0):
                    prbexp2_result.value = (prbexp2_result.value * factor) >> 64

    prbexp2_result.value *= UNIT
    prbexp2_result.value >>= (sp.as_nat(191 - (x >> 64)))

    return prbexp2_result.value

def exp2(x):
    xInt = x
    exp2_result = sp.local('exp2_result', 0)
    sp.trace(xInt)
    # with sp.if_(xInt < 0):
    #     with sp.if_(xInt < -59_794705707972522261):
    #         result.value = sp.nat(0)
    #     with sp.else_():
    #         # Do the fixed-point inversion 1 / 2^x inline to save gas. 1e36 is UNIT * UNIT.
    #         result.value = (10 ** 36) // exp2(-xInt)
    # with sp.else_():
    with sp.if_(xInt >= 192 * UNIT):
            sp.failwith("PRBMath_SD59x18_Exp2_InputTooBig")
    with sp.else_():
            # Convert x to the 192.64-bit fixed-point format.
            x_192x64 = (xInt << 64) // UNIT

            # It is safe to convert the result to int256 with no checks because the maximum input allowed in this function is 192.
            exp2_result.value = prbExp2(x_192x64)

    return exp2_result.value

UNIT = sp.nat(10 ** 18)
HALF_UNIT = UNIT // 2

# def msb(x):
#     result = sp.local('result', sp.nat(0))
#     shift = sp.local('shift', sp.nat(0))
#     with sp.while_(x > 0):
#         x = x >> 1
#         result.value += 1
#         shift.value += 1
#     sp.trace(result.value)
#     return result.value - 1

def msb(x):
    msb_result = sp.local('msb_result', sp.nat(0))
    x_var = sp.local('x_var', x)

    def check_and_shift(factor, mask):
        with sp.if_(x_var.value > mask):
            x_var.value = x_var.value >> factor
            msb_result.value = msb_result.value | factor

    check_and_shift(128, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF)
    check_and_shift(64, 0xFFFFFFFFFFFFFFFF)
    check_and_shift(32, 0xFFFFFFFF)
    check_and_shift(16, 0xFFFF)
    check_and_shift(8, 0xFF)
    check_and_shift(4, 0xF)
    check_and_shift(2, 0x3)
    check_and_shift(1, 0x1)

    return msb_result.value


def log2(x):
    log2_result = sp.local('log2Result', 0)
    with sp.if_(x <= 0):
        sp.failwith("PRBMath_SD59x18_Log_InputTooSmall")

    sign = sp.local('sign', 0)
    with sp.if_(x >= UNIT):
        sign.value = 1
    with sp.else_():
        sign.value = -1
        x = (10 ** 36) // x

    n = msb(x // UNIT)
    result_int = sp.local('result_int', sp.to_int(n) * sp.to_int(UNIT))
    y = sp.local('y', x >> n)

    with sp.if_(y.value == UNIT):
        log2_result.value = result_int.value * sign.value
    
    with sp.if_(log2_result.value == 0):
        double_unit = 2 * UNIT
        delta = sp.local('delta', HALF_UNIT)

        with sp.while_(delta.value > 0):
            y.value = (y.value * y.value) // UNIT

            with sp.if_( y.value >= double_unit):
                result_int.value = result_int.value + sp.to_int(delta.value)
                y.value >>= 1

            delta.value >>= 1

        log2_result.value = result_int.value * sign.value
    
    return log2_result.value

def frac_pow(input, power):
    return exp2((sp.to_int(power) * log2(sp.to_int(input)) // sp.int(ONE)))

class TestPrbExp2(sp.Contract):
    def __init__(self):
        self.init(
          result=0,
        )

    @sp.entry_point
    def test(self, x):
        self.data.result = prbExp2(x)
        sp.verify(self.data.result > 0)

@sp.add_test(name="TestPrbExp2")
def test_prbExp2():
    scenario = sp.test_scenario()
    test_prbExp2 = TestPrbExp2()

    scenario += test_prbExp2

    # Test cases for prbExp2 function
    scenario += test_prbExp2.test(0x8000000000000000).run()
    scenario += test_prbExp2.test(0x4000000000000000).run()
    scenario += test_prbExp2.test(0x2000000000000000).run()
    scenario += test_prbExp2.test(0x1000000000000000).run()
    scenario += test_prbExp2.test(0x800000000000000).run()
    scenario += test_prbExp2.test(0x400000000000000).run()
    scenario += test_prbExp2.test(0x200000000000000).run()
    scenario += test_prbExp2.test(0x100000000000000).run()

  
class Log2Test(sp.Contract):
    def __init__(self):
        self.init(test_results = [])

    @sp.entry_point
    def test_log2(self):
        tests = [
            {'input': sp.nat(1) * UNIT, 'expected': 0},
            {'input': sp.nat(2) * UNIT, 'expected': UNIT},
            {'input': sp.nat(4) * UNIT, 'expected': 2 * UNIT},
            {'input': sp.nat(8) * UNIT, 'expected': 3 * UNIT},
            {'input': UNIT // 2, 'expected': -UNIT},
            {'input': UNIT // 4, 'expected': -2 * UNIT},
            {'input': UNIT // 8, 'expected': -3 * UNIT},
        ]

        # for test in tests:
        result = log2(tests[1]['input'])
        self.data.test_results.push(result)

@sp.add_test(name="Log2Test")
def test_suite():
    scenario = sp.test_scenario()

    contract = Log2Test()
    scenario += contract

    scenario += contract.test_log2()  # InputTooSmall

    # scenario.verify(contract.data.test_results == [True] * 7)

import smartpy as sp

class FracPowContract(sp.Contract):
    def __init__(self):
        self.init(
          result=0
        )

    @sp.entry_point
    def frac_pow(self, params):
        input = params.input
        power = params.power
        self.data.result = self.frac_pow_internal(input, power)

    def frac_pow_internal(self, input, power):
        return exp2((sp.to_int(power) * sp.to_int(log2(sp.to_int(input))) // sp.to_int(ONE)))

    # Implement exp2 and log2 functions here

@sp.add_test(name="FracPowContract_Test")
def test():
    scenario = sp.test_scenario()
    contract = FracPowContract()

    scenario += contract

    test_cases = [
        (2, 3, 8),       # 2^3 = 8
        # (4, 0.5, 2),     # 4^0.5 = 2
        # (9, 0.5, 3),     # 9^0.5 = 3
        # (27, 1/3, 3),    # 27^(1/3) = 3
    ]

    for input, power, expected in test_cases:
        input_sp = sp.nat(input * 10 ** 18)
        power_sp = sp.nat(power * 10 ** 18)
        expected_sp = sp.nat(expected * 10 ** 18)

        scenario += contract.frac_pow(input=input_sp, power=power_sp).run(valid=True)
