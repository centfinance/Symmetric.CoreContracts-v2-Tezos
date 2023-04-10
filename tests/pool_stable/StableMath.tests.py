import smartpy as sp

from contracts.pool_stable.StableMath import StableMath

AMP_PRECISION = sp.nat(1000)


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

    @sp.onchain_view()
    def calcInGivenOut(self, params):
        invariant = self.data.calc_invariant((
            params.amplificationParameter,
            params.balances,
            params.roundUp,
        ))
        sp.result(StableMath.calcInGivenOut(
            params.amplificationParameter,
            params.balances,
            params.tokenIndexIn,
            params.tokenIndexOut,
            params.tokenAmountOut,
            invariant,
        ))

    @sp.onchain_view()
    def calcOutGivenIn(self, params):
        invariant = self.data.calc_invariant((
            params.amplificationParameter,
            params.balances,
            params.roundUp,
        ))
        sp.result(StableMath.calcOutGivenIn(
            params.amplificationParameter,
            params.balances,
            params.tokenIndexIn,
            params.tokenIndexOut,
            params.tokenAmountIn,
            invariant,
        ))


@sp.add_test(name="StableMath Test")
def stableMathTest():
    scenario = sp.test_scenario()
    scenario.h1("StableMath Test")

    # Instantiate the StableMath contract
    stable_math = MockStableMath()
    scenario += stable_math

    # Test data
    amplificationParameter = sp.nat(2000) * AMP_PRECISION
    balances = sp.map(
        {0: sp.nat(100 * 10**18),
         1: sp.nat(200 * 10**18),
         2: sp.nat(300 * 10**18)})
    roundUp = True

    # Test the calculateInvariant function
    invariant = stable_math.calculateInvariant(
        sp.record(
            amplificationParameter=amplificationParameter,
            balances=balances,
            roundUp=roundUp,
        ))

    scenario.show(invariant)

    # Test the calcInGivenOut function
    tokenIndexIn = 0
    tokenIndexOut = 1
    tokenAmountOut = sp.nat(5 * 10**18)

    in_given_out = stable_math.calcInGivenOut(
        sp.record(
            amplificationParameter=amplificationParameter,
            balances=balances,
            tokenIndexIn=tokenIndexIn,
            tokenIndexOut=tokenIndexOut,
            tokenAmountOut=tokenAmountOut,
            roundUp=roundUp,
        ))

    scenario.show(in_given_out)

    # Test the calcOutGivenIn function
    tokenAmountIn = sp.nat(5 * 10**18)

    out_given_in = stable_math.calcOutGivenIn(
        sp.record(
            amplificationParameter=amplificationParameter,
            balances=balances,
            tokenIndexIn=tokenIndexIn,
            tokenIndexOut=tokenIndexOut,
            tokenAmountIn=tokenAmountIn,
            roundUp=roundUp,
        ))

    scenario.show(out_given_in)
