import smartpy as sp

import contracts.utils.math.FixedPoint as FixedPoint

from contracts.pool_weighted.WeightedMath import WeightedMath


class IExternalWeightedMath:
    t_calcOutGivenIn_params = sp.TRecord(
        balanceIn=sp.TNat,
        weightIn=sp.TNat,
        balanceOut=sp.TNat,
        weightOut=sp.TNat,
        amountIn=sp.TNat,
    )

    t_calcInGivenOut_params = sp.TRecord(
        balanceIn=sp.TNat,
        weightIn=sp.TNat,
        balanceOut=sp.TNat,
        weightOut=sp.TNat,
        amountOut=sp.TNat,
    )

    t_calculateInvariant_params = sp.TRecord(
        normalizedWeights=sp.TMap(sp.TNat, sp.TNat),
        balances=sp.TMap(sp.TNat, sp.TNat),
    )

    t_calcSptOutGivenExactTokensIn_params = sp.TRecord(
        normalizedWeights=sp.TMap(sp.TNat, sp.TNat),
        balances=sp.TMap(sp.TNat, sp.TNat),
        amountsIn=sp.TMap(sp.TNat, sp.TNat),
        totalSupply=sp.TNat,
        swapFeePercentage=sp.TNat,
    )

    t_calcSptInGivenExactTokensOut_params = sp.TRecord(
        normalizedWeights=sp.TMap(sp.TNat, sp.TNat),
        balances=sp.TMap(sp.TNat, sp.TNat),
        amountsOut=sp.TMap(sp.TNat, sp.TNat),
        totalSupply=sp.TNat,
        swapFeePercentage=sp.TNat,
    )

    t_calcTokenInGivenExactSptOut_params = sp.TRecord(
        balance=sp.TNat,
        normalizedWeight=sp.TNat,
        sptAmountOut=sp.TNat,
        sptTotalSupply=sp.TNat,
        swapFeePercentage=sp.TNat,
    )

    t_calcTokenOutGivenExactSptIn_params = sp.TRecord(
        balance=sp.TNat,
        normalizedWeight=sp.TNat,
        sptAmountIn=sp.TNat,
        sptTotalSupply=sp.TNat,
        swapFeePercentage=sp.TNat,
    )

    def calcOutGivenIn(lib, params):
        sp.set_type(params, sp.TRecord(
            balanceIn=sp.TNat,
            weightIn=sp.TNat,
            balanceOut=sp.TNat,
            weightOut=sp.TNat,
            amountIn=sp.TNat,
        ))
        return sp.compute(sp.view('calcOutGivenIn', lib, params,
                                  t=sp.TNat).open_some("Invalid view"))

    def calcInGivenOut(lib, params):
        sp.set_type(params, sp.TRecord(
            balanceIn=sp.TNat,
            weightIn=sp.TNat,
            balanceOut=sp.TNat,
            weightOut=sp.TNat,
            amountOut=sp.TNat,
        ))
        return sp.compute(sp.view('calcInGivenOut', lib, params,
                                  t=sp.TNat).open_some("Invalid view"))

    def calculateInvariant(lib, params):
        sp.set_type(params, sp.TRecord(
            normalizedWeights=sp.TMap(sp.TNat, sp.TNat),
            balances=sp.TMap(sp.TNat, sp.TNat),
        ))
        return sp.compute(sp.view('calculateInvariant', lib, params,
                                  t=sp.TNat).open_some("Invalid view"))

    def calcSptOutGivenExactTokensIn(lib, params):
        sp.set_type(params, sp.TRecord(
            normalizedWeights=sp.TMap(sp.TNat, sp.TNat),
            balances=sp.TMap(sp.TNat, sp.TNat),
            amountsIn=sp.TMap(sp.TNat, sp.TNat),
            totalSupply=sp.TNat,
            swapFeePercentage=sp.TNat,
        ))
        return sp.compute(sp.view('calcSptOutGivenExactTokensIn', lib, params,
                                  t=sp.TNat).open_some("Invalid view"))

    def calcSptInGivenExactTokensOut(lib, params):
        sp.set_type(params, sp.TRecord(
            normalizedWeights=sp.TMap(sp.TNat, sp.TNat),
            balances=sp.TMap(sp.TNat, sp.TNat),
            amountsOut=sp.TMap(sp.TNat, sp.TNat),
            totalSupply=sp.TNat,
            swapFeePercentage=sp.TNat,
        ))
        return sp.compute(sp.view('calcSptInGivenExactTokensOut', lib, params,
                                  t=sp.TNat).open_some("Invalid view"))

    def calcTokenInGivenExactSptOut(lib, params):
        sp.set_type(params, sp.TRecord(
            balance=sp.TNat,
            normalizedWeight=sp.TNat,
            sptAmountOut=sp.TNat,
            sptTotalSupply=sp.TNat,
            swapFeePercentage=sp.TNat,
        ))
        return sp.compute(sp.view('calcTokenInGivenExactSptOut', lib, params,
                                  t=sp.TNat).open_some("Invalid view"))

    def calcTokenOutGivenExactSptIn(lib, params):
        sp.set_type(params, sp.TRecord(
            balance=sp.TNat,
            normalizedWeight=sp.TNat,
            sptAmountIn=sp.TNat,
            sptTotalSupply=sp.TNat,
            swapFeePercentage=sp.TNat,
        ))
        return sp.compute(sp.view('calcTokenOutGivenExactSptIn', lib, params,
                                  t=sp.TNat).open_some("Invalid view"))


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
        sp.set_type(params, IExternalWeightedMath.t_calcOutGivenIn_params)
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
        sp.set_type(params, IExternalWeightedMath.t_calcInGivenOut_params)
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
        sp.set_type(params, IExternalWeightedMath.t_calculateInvariant_params)
        sp.result(WeightedMath._calculateInvariant(
            params.normalizedWeights,
            params.balances,
            self.data.fixedPoint,
        ))

    @sp.onchain_view()
    def calcSptOutGivenExactTokensIn(self, params):
        sp.set_type(
            params, IExternalWeightedMath.t_calcSptOutGivenExactTokensIn_params)

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
        sp.set_type(
            params, IExternalWeightedMath.t_calcSptInGivenExactTokensOut_params)

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
        sp.set_type(
            params, IExternalWeightedMath.t_calcTokenInGivenExactSptOut_params)

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
        sp.set_type(
            params, IExternalWeightedMath.t_calcTokenOutGivenExactSptIn_params)

        sp.result(WeightedMath._calcTokenOutGivenExactSptIn(
            params.balance,
            params.normalizedWeight,
            params.sptAmountIn,
            params.sptTotalSupply,
            params.swapFeePercentage,
            self.data.fixedPoint,
        ))


sp.add_compilation_target('ExternalWeightedMath', ExternalWeightedMath())
