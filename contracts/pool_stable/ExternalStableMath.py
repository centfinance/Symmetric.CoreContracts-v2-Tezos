import smartpy as sp

import contracts.utils.math.FixedPoint as FixedPoint
from contracts.pool_stable.StableMath import StableMath


class ExternalStableMath(sp.Contract):
    def __init__(self):
        sp.Contract.__init__(self)
        self.init(
            fixedPoint=sp.big_map({
                "mulDown": FixedPoint.mulDown,
                "mulUp": FixedPoint.mulUp,
                "divDown": FixedPoint.divDown,
                "divUp": FixedPoint.divUp,
            }, tkey=sp.TString, tvalue=sp.TLambda(sp.TPair(sp.TNat, sp.TNat), sp.TNat))
        )

    @sp.onchain_view()
    def calculateInvariant(self, params):
        sp.result(self.data.calc_invariant((
            params.amp,
            params.balances,
        )))

    @sp.onchain_view()
    def calcInGivenOut(self, params):
        invariant = self.data.calc_invariant((
            params.amp,
            params.balances,
        ))
        sp.result(StableMath.calcInGivenOut(
            params.amp,
            params.balances,
            params.tokenIndexIn,
            params.tokenIndexOut,
            params.tokenAmountOut,
            invariant,
        ))

    @sp.onchain_view()
    def calcOutGivenIn(self, params):
        invariant = self.data.calc_invariant((
            params.amp,
            params.balances,
        ))
        sp.result(StableMath.calcOutGivenIn(
            params.amp,
            params.balances,
            params.tokenIndexIn,
            params.tokenIndexOut,
            params.tokenAmountIn,
            invariant,
        ))

    @sp.onchain_view()
    def calcSptOutGivenExactTokensIn(self, params):
        sp.result(StableMath.calcSptOutGivenExactTokensIn(
            params.amp,
            params.balances,
            params.amountsIn,
            params.sptTotalSupply,
            params.invariant,
            params.swapFeePercentage,
            self.data.calc_invariant,
            self.data.fpm,
        ))

    @sp.onchain_view()
    def calcSptInGivenExactTokensOut(self, params):
        sp.result(StableMath.calcSptInGivenExactTokensOut(
            params.amp,
            params.balances,
            params.amountsOut,
            params.sptTotalSupply,
            params.invariant,
            params.swapFeePercentage,
            self.data.calc_invariant,
            self.data.fpm,
        ))

    @sp.onchain_view()
    def calcTokenInGivenExactSptOut(self, params):
        sp.result(StableMath.calcTokenInGivenExactSptOut(
            params.amp,
            params.balances,
            params.tokenIndex,
            params.sptAmountOut,
            params.sptTotalSupply,
            params.invariant,
            params.swapFeePercentage,
            self.data.fpm,
        ))

    @sp.onchain_view()
    def calcTokenOutGivenExactSptIn(self, params):
        sp.result(StableMath.calcTokenOutGivenExactSptIn(
            params.amp,
            params.balances,
            params.tokenIndex,
            params.sptAmountIn,
            params.sptTotalSupply,
            params.invariant,
            params.swapFeePercentage,
            self.data.fpm,
        ))
