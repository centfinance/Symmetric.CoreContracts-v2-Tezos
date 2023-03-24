import smartpy as sp

from contracts.pool_utils.external_fees.InvariantGrowthProtocolSwapFees import InvariantGrowthProtocolSwapFees

from contracts.interfaces.IRateProvider import IRateProvider

import contracts.utils.math.FixedPoint as FixedPoint

from contracts.pool_weighted.WeightedMath import WeightedMath


class WeightedPoolProtocolFees:
    def __init__(self):
        self.update_initial_storage(
            exemptFromYieldFees=True,
            rateProviders=sp.map(l={}, tkey=sp.TNat,
                                 tvalue=sp.TOption(sp.TAddress)),
            feeCache=sp.record(
                swapFee=sp.nat(0),
                yieldFee=sp.nat(0),
                aumFee=sp.nat(0),
            )
        )

    def _initializeProtocolFees(self, params):
        sp.verify(params.numTokens == sp.len(params.rateProviders))

        self.data.exemptFromYieldFees = self._getYieldFeeExemption(
            params.rateProviders)

        self.data.rateProviders = params.rateProviders

    def _getYieldFeeExemption(self, rateProviders):
        exempt = sp.local('exempt', True)

        with sp.for_('i', sp.range(0, sp.len(rateProviders)))as i:
            with sp.if_(rateProviders[i] != sp.none):
                exempt.value = False

        return exempt.value

    def _getSwapProtocolFeesPoolPercentage(
            self,
            preJoinExitInvariant,
            protocolSwapFeePercentage
    ):
        fpm = self.data.fixedPoint

        #                          self.data.entries['postJoinExitInvariant'])))
        return InvariantGrowthProtocolSwapFees.getProtocolOwnershipPercentage(
            sp.compute(fpm['divDown']((preJoinExitInvariant,
                                       self.data.entries['postJoinExitInvariant']))),
            FixedPoint.ONE,
            protocolSwapFeePercentage,
            fpm,
        )

    def _getYieldProtocolFeesPoolPercentage(self, normalizedWeights):
        fpm = sp.compute(self.data.fixedPoint)
        athRateProduct = sp.compute(self.data.entries['athRateProduct'])
        percentages = sp.local('percentages', sp.nat(0))
        rateProduct = sp.local('rateProduct', sp.nat(0))
        with sp.if_(self.data.exemptFromYieldFees == False):
            rateProduct.value = self._getRateProduct(normalizedWeights)
            with sp.if_(rateProduct.value > athRateProduct):
                percentages.value = InvariantGrowthProtocolSwapFees.getProtocolOwnershipPercentage(
                    fpm['divDown']((rateProduct.value, athRateProduct)),
                    FixedPoint.ONE,
                    self.data.feeCache.yieldFee,
                    fpm,
                )
        return (
            percentages.value,
            rateProduct.value,
        )

    def _getPreJoinExitProtocolFees(
        self,
        preJoinExitInvariant,
        normalizedWeights,
        preJoinExitSupply,
    ):
        protocolSwapFeesPoolPercentage = sp.compute(self._getSwapProtocolFeesPoolPercentage(
            preJoinExitInvariant,
            sp.compute(self.data.feeCache.swapFee),
        ))

        (protocolYieldFeesPoolPercentage,  athRateProduct) = self._getYieldProtocolFeesPoolPercentage(
            normalizedWeights
        )

        return (
            InvariantGrowthProtocolSwapFees.sptForPoolOwnershipPercentage(
                preJoinExitSupply,
                (protocolSwapFeesPoolPercentage + protocolYieldFeesPoolPercentage),
                self.data.fixedPoint['divDown'],
            ),
            athRateProduct
        )

    def _getPostJoinExitProtocolFees(
        self,
        preJoinExitInvariant,
        preBalances,
        balanceDeltas,
        normalizedWeights,
        preJoinExitSupply,
        postJoinExitSupply
    ):

        fpm = self.data.fixedPoint
        isJoin = (postJoinExitSupply >= preJoinExitSupply)

        with sp.for_('i', sp.range(0, sp.len(preBalances))) as i:
            preBalances[i] = sp.eif(
                isJoin,
                (preBalances[i] + balanceDeltas[i]),
                (sp.as_nat(preBalances[i] - balanceDeltas[i])),
            )

        postJoinExitInvariant = sp.compute(WeightedMath._calculateInvariant(
            normalizedWeights,
            preBalances,
            fpm['powDown']
        ))
        protocolSwapFeePercentage = sp.compute(self.data.feeCache.swapFee)

        self.data.entries['postJoinExitInvariant'] = postJoinExitInvariant

        protocolFeeAmount = sp.local('protocolSwapFeeAmount', 0)

        with sp.if_(protocolSwapFeePercentage != 0):
            protocolFeeAmount.value = InvariantGrowthProtocolSwapFees.calcDueProtocolFees(
                sp.compute(fpm['divDown']((
                    postJoinExitInvariant, preJoinExitInvariant))),
                preJoinExitSupply,
                postJoinExitSupply,
                protocolSwapFeePercentage,
                fpm,
            )

        return protocolFeeAmount.value

    def _getRateFactor(self, rateProvider, weight):
        # with sp.if_(rateProvider):
            powDown = self.data.fixedPoint['powDown']
            return powDown((IRateProvider.getRate(rateProvider), weight))
        # return sp.nat(1000000000000000000)

    def _getRateProduct(self, normalizedWeights):
        product = sp.local('product', self.data.fixedPoint['mulDown']((
            self._getRateFactor(normalizedWeights[0], self.data.rateProviders[0]),
            self._getRateFactor(normalizedWeights[1], self.data.rateProviders[1]),
        )))
        product = sp.local('product', sp.nat(0))
        with sp.if_(sp.len(normalizedWeights) > 2):
            with sp.for_('i', sp.range(2, sp.len(normalizedWeights))) as i:
                product.value = self.data.fixedPoint['mulDown']((
                    product.value,
                    self._getRateFactor(normalizedWeights[i], self.data.rateProviders[i])
                ))

        return product.value
