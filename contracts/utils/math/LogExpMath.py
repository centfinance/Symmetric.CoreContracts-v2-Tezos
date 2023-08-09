import smartpy as sp
import contracts.interfaces.SymmetricErrors as Errors


ONE = 1000000000000000000
HALF = 500000000000000000



def power(base, power):
    return exp2((sp.to_int(power) * log2(base)) // ONE)

def _exp2(x):
    _exp2_result = sp.local('_exp2_result', sp.nat(0x800000000000000000000000000000000000000000000000))

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
                    _exp2_result.value = (_exp2_result.value * factor) >> 64

    _exp2_result.value *= ONE
    _exp2_result.value >>= (sp.as_nat(191 - (x >> 64)))

    return _exp2_result.value

def exp2(x):
    exp2_result = sp.local('exp2_result', sp.nat(0))
 
    with sp.if_(x < -59_794705707972522261):
            exp2_result.value = sp.nat(0)
        # with sp.else_():
        #     # Do the fixed-point inversion 1 / 2^x inline to save gas. 1e36 is UNIT * UNIT.
        #     exp2_result.value = (10 ** 36)
    with sp.else_():
        new_x = sp.local('new_x', 0)
        negative = sp.local('negative', False)

        with sp.if_(x < 0):
            negative.value = True
            new_x.value = abs(x)
        with sp.else_():
            new_x.value = sp.as_nat(x)

        with sp.if_(new_x.value >= 192 * ONE):
                sp.failwith("PRBMath_SD59x18_Exp2_InputTooBig")
        with sp.else_():
                # Convert x to the 192.64-bit fixed-point format.
                x_192x64 = (new_x.value << 64) // ONE

                with sp.if_(negative.value == True):
                    exp2_result.value = (10 ** 36) // _exp2(x_192x64)
                with sp.else_():
                    exp2_result.value = _exp2(x_192x64)

    return exp2_result.value

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
    new_x =sp.local('new_x', x)
    log2_result = sp.local('log2Result', 0)
    with sp.if_(x <= 0):
        sp.failwith("PRBMath_SD59x18_Log_InputTooSmall")

    sign = sp.local('sign', 0)
    with sp.if_(x >= ONE):
        sign.value = 1
    with sp.else_():
        sign.value = -1
        new_x.value = (10 ** 36) // x
    
    n = msb(new_x.value // ONE)
    result_int = sp.local('result_int', sp.to_int(n) * sp.to_int(ONE))
    y = sp.local('y', new_x.value >> n)
    with sp.if_(y.value == ONE):
        log2_result.value = result_int.value * sign.value
    
    with sp.if_(log2_result.value == 0):
        double_unit = 2 * ONE
        delta = sp.local('delta', HALF)

        with sp.while_(delta.value > 0):
            y.value = (y.value * y.value) // ONE

            with sp.if_(y.value >= double_unit):
                result_int.value = result_int.value + sp.to_int(delta.value)
                y.value >>= 1

            delta.value >>= 1

        log2_result.value = result_int.value * sign.value

    return log2_result.value