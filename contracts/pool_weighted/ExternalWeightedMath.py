import smartpy as sp

import contracts.utils.math.FixedPoint as FixedPoint

from contracts.pool_weighted.WeightedMath import WeightedMath


class IExternalWeightedMath:

    def calcOutGivenIn(lib, params):
        return sp.view('calcOutGivenIn', lib, params,
                       t=sp.TNat).open_some("Invalid view")

    def calcInGivenOut(lib, params):
        return sp.view('calcInGivenOut', lib, params,
                       t=sp.TNat).open_some("Invalid view")

    def calculateInvariant(lib, params):
        return sp.view('calculateInvariant', lib, params,
                       t=sp.TNat).open_some("Invalid view")

    def calcSptOutGivenExactTokensIn(lib, params):
        return sp.view('calcSptOutGivenExactTokensIn', lib, params,
                       t=sp.TNat).open_some("Invalid view")

    def calcSptInGivenExactTokensOut(lib, params):
        return sp.view('calcSptInGivenExactTokensOut', lib, params,
                       t=sp.TNat).open_some("Invalid view")

    def calcTokenInGivenExactSptOut(lib, params):
        return sp.view('calcTokenInGivenExactSptOut', lib, params,
                       t=sp.TNat).open_some("Invalid view")

    def calcTokenOutGivenExactSptIn(lib, params):
        return sp.view('calcTokenOutGivenExactSptIn', lib, params,
                       t=sp.TNat).open_some("Invalid view")


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
