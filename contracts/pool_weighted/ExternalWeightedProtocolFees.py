import smartpy as sp

from contracts.pool_utils.external_fees.InvariantGrowthProtocolSwapFees import InvariantGrowthProtocolSwapFees

import contracts.utils.math.FixedPoint as FixedPoint

from contracts.pool_weighted.WeightedMath import WeightedMath

from contracts.interfaces.IRateProvider import IRateProvider

ONE = sp.nat(10**18)


class IExternalWeightedProtocolFees:
    PreJoinExitParamsType = sp.TRecord(
        preJoinExitSupply=sp.TNat,
        preJoinExitInvariant=sp.TNat,
        swapFee=sp.TNat,
        postJoinExitInvariant=sp.TNat,
        normalizedWeights=sp.TMap(sp.TNat, sp.TNat),
        rateProviders=sp.TMap(sp.TNat, sp.TOption(sp.TAddress)),
        athRateProduct=sp.TNat,
        yieldFee=sp.TNat,
        exemptFromYieldFees=sp.TBool,
    )

    PostJoinExitParamsType = sp.TRecord(
        preJoinExitSupply=sp.TNat,
        postJoinExitSupply=sp.TNat,
        preJoinExitInvariant=sp.TNat,
        preBalances=sp.TMap(sp.TNat, sp.TNat),
        balanceDeltas=sp.TMap(sp.TNat, sp.TNat),
        normalizedWeights=sp.TMap(sp.TNat, sp.TNat),
        swapFee=sp.TNat,
    )

    GetRateProductParamsType = sp.TRecord(
        normalizedWeights=sp.TMap(sp.TNat, sp.TNat),
        rateProviders=sp.TMap(sp.TNat, sp.TOption(sp.TAddress)),
    )

    def getPreJoinExitProtocolFees(lib, params):
        sp.set_type(params, IExternalWeightedProtocolFees.PreJoinExitParamsType)
        return sp.compute(sp.view('getPreJoinExitProtocolFees', lib, params,
                                  t=sp.TPair(sp.TNat, sp.TNat)).open_some("Invalid view"))

    def getPostJoinExitProtocolFees(lib, params):
        sp.set_type(
            params, IExternalWeightedProtocolFees.PostJoinExitParamsType)
        return sp.compute(sp.view('getPostJoinExitProtocolFees', lib, params,
                                  t=sp.TPair(sp.TNat, sp.TNat)).open_some("Invalid view"))

    def getRateProduct(lib, params):
        sp.set_type(
            params, IExternalWeightedProtocolFees.GetRateProductParamsType)
        return sp.compute(sp.view('getRateProduct', lib, params,
                                  t=sp.TNat).open_some("Invalid view"))


class ExternalWeightedProtocolFees(sp.Contract):
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
    def getPreJoinExitProtocolFees(self, params):
        sp.set_type(params, IExternalWeightedProtocolFees.PreJoinExitParamsType)
        fpm = sp.compute(self.data.fixedPoint)
        protocolSwapFeesPoolPercentage = sp.compute(self._getSwapProtocolFeesPoolPercentage(
            params.preJoinExitInvariant,
            sp.compute(params.swapFee),
            params.postJoinExitInvariant,
            fpm
        ))
        (protocolYieldFeesPoolPercentage,  athRateProduct) = self._getYieldProtocolFeesPoolPercentage(
            params.normalizedWeights,
            params.rateProviders,
            params.athRateProduct,
            params.yieldFee,
            params.exemptFromYieldFees,
            fpm
        )

        sp.result((
            InvariantGrowthProtocolSwapFees.sptForPoolOwnershipPercentage(
                params.preJoinExitSupply,
                (protocolSwapFeesPoolPercentage + protocolYieldFeesPoolPercentage),
            ),
            athRateProduct
        ))

    @sp.onchain_view()
    def getPostJoinExitProtocolFees(
        self,
        params
    ):
        sp.set_type(
            params, IExternalWeightedProtocolFees.PostJoinExitParamsType)
        fpm = sp.compute(self.data.fixedPoint)
        isJoin = (params.postJoinExitSupply >= params.preJoinExitSupply)
        balances = sp.compute(sp.map({}, sp.TNat, sp.TNat))
        with sp.for_('i', sp.range(0, sp.len(params.preBalances))) as i:
            balances[i] = sp.eif(
                isJoin,
                (params.preBalances[i] + params.balanceDeltas[i]),
                (sp.as_nat(params.preBalances[i] - params.balanceDeltas[i])),
            )

        postJoinExitInvariant = sp.compute(WeightedMath._calculateInvariant(
            params.normalizedWeights,
            balances,
            fpm,
        ))

        # self.data.entries['postJoinExitInvariant'] = postJoinExitInvariant

        protocolFeeAmount = sp.local('protocolSwapFeeAmount', 0)
        with sp.if_(params.swapFee != 0):
            protocolFeeAmount.value = InvariantGrowthProtocolSwapFees.calcDueProtocolFees(
                sp.compute(fpm['divDown']((
                    postJoinExitInvariant, params.preJoinExitInvariant))),
                params.preJoinExitSupply,
                params.postJoinExitSupply,
                params.swapFee,
                fpm,
            )

        sp.result((protocolFeeAmount.value, postJoinExitInvariant))

    @sp.onchain_view()
    def getRateProduct(self, params):
        sp.set_type(
            params, IExternalWeightedProtocolFees.GetRateProductParamsType)
        fpm = sp.compute(self.data.fixedPoint)
        sp.result(self._getRateProduct(
            normalizedWeights=params.normalizedWeights,
            rateProviders=params.rateProviders,
            fpm=fpm,
        ))

    def _getSwapProtocolFeesPoolPercentage(
            self,
            preJoinExitInvariant,
            protocolSwapFeePercentage,
            postJoinExitInvariant,
            fpm,

    ):
        return InvariantGrowthProtocolSwapFees.getProtocolOwnershipPercentage(
            sp.compute(fpm['divDown']((preJoinExitInvariant,
                                       postJoinExitInvariant))),
            ONE,
            protocolSwapFeePercentage,
            fpm,
        )

    def _getYieldProtocolFeesPoolPercentage(
            self,
            normalizedWeights,
            rateProviders,
            athRateProduct,
            yieldFee,
            exemptFromYieldFees,
            fpm,
    ):
        percentages = sp.local('percentages', sp.nat(0))
        rateProduct = sp.local('rateProduct', sp.nat(0))
        with sp.if_(exemptFromYieldFees == False):
            rateProduct.value = self._getRateProduct(
                normalizedWeights, rateProviders, fpm)
            with sp.if_(rateProduct.value > athRateProduct):
                percentages.value = InvariantGrowthProtocolSwapFees.getProtocolOwnershipPercentage(
                    fpm['divDown']((rateProduct.value, athRateProduct)),
                    ONE,
                    yieldFee,
                    fpm,
                )
        return (
            percentages.value,
            rateProduct.value,
        )

    def _getRateFactor(self, weight, provider, fpm):
        powDown = fpm['powDown']
        return (powDown((IRateProvider.getRate(provider.open_some()), weight)))

    def _getRateProduct(self, normalizedWeights, rateProviders, fpm):
        def rateFactor(rp, i): return sp.eif(
            rp == sp.none,
            sp.nat(1000000000000000000),
            self._getRateFactor(normalizedWeights[i], rp, fpm),
        )
        rps = sp.compute(rateProviders)
        product = sp.local('product', fpm['mulDown']((
            sp.compute(rateFactor(rps[0], 0)),
            sp.compute(rateFactor(rps[1], 1)),
        )))

        with sp.if_(sp.len(normalizedWeights) > 2):
            with sp.for_('i', sp.range(2, sp.len(normalizedWeights))) as i:
                product.value = fpm['mulDown']((
                    product.value,
                    sp.compute(rateFactor(rps[i], i))
                ))

        return product.value
