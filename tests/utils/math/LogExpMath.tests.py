import smartpy as sp

import contracts.utils.math.LogExpMath as LogExpMath

class MathContract(sp.Contract):
    def __init__(self):
        self.init()

    @sp.onchain_view()
    def power(self, params):
        x = params.x
        power = params.power
        result = LogExpMath.power(x, power)
        sp.result(result)

    @sp.onchain_view()
    def exp2(self, params):
        x = params.x
        result = LogExpMath.exp2(x)
        sp.result(result)

    @sp.onchain_view()
    def log2(self, params):
        x = params.x
        result = LogExpMath.log2(x)
        sp.result(result)

    # Define all other required functions here

@sp.add_test(name="Math Functions Test")
def test():
    scenario = sp.test_scenario()
    contract = MathContract()

    scenario += contract

    power_test_cases = [
        (2, 3, 8),
        (4, 0.5, 2),
        (9, 0.5, 3),
        (27, 1/3, 3),
    ]

    exp2_test_cases = [
        (0, 1),
        (1, 2),
        (2, 4),
        (3, 8),
    ]

    log2_test_cases = [
        (1, 0),
        (2, 1),
        (4, 2),
        (8, 3),
    ]

    for base, exponent, expected in power_test_cases:
        base_sp = sp.nat(base * 10 ** 18)
        exponent_sp = sp.as_nat(int(exponent * 10 ** 18))
        expected_sp = sp.nat(expected * 10 ** 18)

        power = contract.power(sp.record(x=base_sp, power=exponent_sp))
        scenario.show(power)
        # scenario.verify(power == expected_sp)

    for x, expected in exp2_test_cases:
        x_sp = sp.nat(x * 10 ** 18)
        expected_sp = sp.nat(expected * 10 ** 18)

        exp2 = contract.exp2(sp.record(x=x_sp))
        scenario.show(exp2)

        scenario.verify(exp2 == expected_sp)

    for x, expected in log2_test_cases:
        x_sp = sp.nat(x * 10 ** 18)
        expected_sp = sp.int(expected * 10 ** 18)

        log2 = contract.log2(sp.record(x=x_sp))
        scenario.show(log2)

        scenario.verify(log2 == expected_sp)

