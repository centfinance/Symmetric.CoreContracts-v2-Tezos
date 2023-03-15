import smartpy as sp

import contracts.utils.math.FixedPoint as FixedPoint

from contracts.pool_weighted.WeightedMath import WeightedMath


class ExternalWeightedMath(sp.Contract):
    def __init__(self):
        sp.Contract.__init__(self)
        self.init(
            fixedPoint=sp.big_map({
                "mulDown": FixedPoint.mulDown,
                "mulUp": FixedPoint.mulUp,
                "divDown": FixedPoint.divDown,
                "divUp": FixedPoint.divUp,
                "powDown": FixedPoint.powDown,
                "powUp": FixedPoint.powUp,
                "pow": FixedPoint.pow,
            }, tkey=sp.TString, tvalue=sp.TLambda(sp.TPair(sp.TNat, sp.TNat), sp.TNat))
        )

    @sp.onchain_view()
    def calcOutGivenIn(self, params):
        sp.result(WeightedMath._calcOutGivenIn(
            params.balanceIn,
            params.weightIn,
            params.balanceOut,
            params.weightOut,
            params.amountIn,
            self.data.fixedPoint,
        ))

    @sp.onchain_view()
    def calcInGivenOut(self, params):
        sp.result(WeightedMath._calcInGivenOut(
            params.balanceIn,
            params.weightIn,
            params.balanceOut,
            params.weightOut,
            params.amountOut,
            self.data.fixedPoint,
        ))

    @sp.onchain_view()
    def calculateInvariant(self, params):
        sp.result(WeightedMath._calculateInvariant(
            params.normalizedWeights,
            params.balances,
            self.data.fixedPoint['powDown'],
        ))

    @sp.onchain_view()
    def calcSptOutGivenExactTokensIn(self, params):
        sp.result(WeightedMath._calcSptOutGivenExactTokensIn(
            params.balances,
            params.normalizedWeights,
            params.amountsIn,
            params.totalSupply,
            params.swapFeePercentage,
            self.data.fixedPoint,
        ))

    @sp.onchain_view()
    def calcSptInGivenExactTokensOut(self, params):
        sp.result(WeightedMath._calcSptInGivenExactTokensOut(
            params.balances,
            params.normalizedWeights,
            params.amountsOut,
            params.totalSupply,
            params.swapFeePercentage,
            self.data.fixedPoint,
        ))

    @sp.onchain_view()
    def calcTokenInGivenExactSptOut(self, params):
        sp.result(WeightedMath._calcTokenInGivenExactSptOut(
            params.balance,
            params.normalizedWeight,
            params.sptAmountOut,
            params.sptTotalSupply,
            params.swapFeePercentage,
            self.data.fixedPoint,
        ))

    @sp.onchain_view()
    def calcTokenOutGivenExactSptIn(self, params):
        sp.result(WeightedMath._calcTokenOutGivenExactSptIn(
            params.balance,
            params.normalizedWeight,
            params.sptAmountIn,
            params.sptTotalSupply,
            params.swapFeePercentage,
            self.data.fixedPoint,
        ))
