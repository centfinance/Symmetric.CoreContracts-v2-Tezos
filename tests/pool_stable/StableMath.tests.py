import smartpy as sp

from contracts.pool_stable.StableMath import StableMath

AMP_PRECISION = sp.nat(10000)


class MockStableMath(sp.Contract):
    def __init__(self):
        self.init(
            calc_invariant=StableMath.calculateInvariant,
            invariant_result=sp.nat(0,)
        )

    @sp.onchain_view()
    def calculateInvariant(self, params):
        sp.result(self.data.calc_invariant((
            params.amplificationParameter,
            params.balances,
            params.roundUp,
        )))


@sp.add_test(name="StableMath Test")
def stableMathTest():
    scenario = sp.test_scenario()
    scenario.h1("StableMath Test")

    # Instantiate the StableMath contract
    stable_math = MockStableMath()
    scenario += stable_math

    # Test data
    amplificationParameter = sp.nat(2000)
    balances = sp.map(
        {0: sp.nat(100000000),
         1: sp.nat(200000000),
         2: sp.nat(300000000)})
    roundUp = True

    # Test the calculateInvariant function
    invariant = stable_math.calculateInvariant(
        sp.record(
            amplificationParameter=amplificationParameter,
            balances=balances,
            roundUp=roundUp,
        ))

    scenario.show(invariant)
