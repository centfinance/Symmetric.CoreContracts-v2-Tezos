import smartpy as sp

from contracts.pool_utils.external_fees.InvariantGrowthProtocolSwapFees import InvariantGrowthProtocolSwapFees

import contracts.utils.math.FixedPoint as FixedPoint

from contracts.pool_weighted.ExternalWeightedMath import IExternalWeightedMath


class WeightedPoolProtocolFees:
    def __init__(self):
        self.update_initial_storage(
            exemptFromYieldFees=False,
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

    def _getSwapProtocolFeesPoolPercentage(self, params):
        return InvariantGrowthProtocolSwapFees.getProtocolOwnershipPercentage(
            FixedPoint.divDown((params.preJoinExitInvariant,
                               self.data.entries['postJoinExitInvariant'])),
            FixedPoint.ONE,
            params.protocolSwapFeePercentage,
            self.data.fixedPoint,
        )

    def _getYieldProtocolFeesPoolPercentage(self, normalizedWeights):
        percentages = sp.local('percentages', (0, 0))
        with sp.if_(self.data.exemptFromYieldFees == False):
            rateProduct = self._getRateProduct(normalizedWeights)
            with sp.if_(rateProduct > self.data.entries['athRateProduct']):
                percentages.value = InvariantGrowthProtocolSwapFees.getProtocolOwnershipPercentage(
                    FixedPoint.divDown((rateProduct,
                                       self.data.entries['athRateProduct'])),
                    FixedPoint.ONE,
                    self.data.feeCache.yieldFee,
                    self.data.fixedPoint,
                )

        return percentages.value

    def _getPreJoinExitProtocolFees(
        self,
        preJoinExitInvariant,
        normalizedWeights,
        preJoinExitSupply,
    ):
        protocolSwapFeesPoolPercentage = self._getSwapProtocolFeesPoolPercentage(
            preJoinExitInvariant,
            sp.compute(self.data.feeCache.swapFee),
        )

        (protocolYieldFeesPoolPercentage,  athRateProduct) = self._getYieldProtocolFeesPoolPercentage(
            normalizedWeights
        )

        return (
            InvariantGrowthProtocolSwapFees.sptForPoolOwnershipPercentage(
                preJoinExitSupply,
                (protocolSwapFeesPoolPercentage + protocolYieldFeesPoolPercentage)
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
        isJoin = (postJoinExitSupply >= preJoinExitSupply)

        with sp.for_('i', sp.range(0, sp.len(preBalances))) as i:
            preBalances[i] = sp.eif(
                isJoin,
                (preBalances[i] + balanceDeltas[i]),
                sp.as_nat(preBalances[i] - balanceDeltas[i]),
            )

        postJoinExitInvariant = IExternalWeightedMath.calculateInvariant(
            sp.compute(self.data.weightedMathLib),
            sp.record(
                normalizedWeights=normalizedWeights,
                preBalances=preBalances,
            ))

        protocolSwapFeePercentage = sp.compute(self.data.feeCache.swapFee)

        self.data.entries['postJoinExitInvariant'] = postJoinExitInvariant

        protocolFeeAmount = sp.local('protocolSwapFeeAmount', 0)

        with sp.if_(protocolSwapFeePercentage != 0):
            protocolFeeAmount.value = InvariantGrowthProtocolSwapFees.calcDueProtocolFees(
                sp.compute(self.data.fixedPoint['divDown'](
                    postJoinExitInvariant, preJoinExitInvariant)),
                preJoinExitSupply,
                postJoinExitSupply,
                protocolSwapFeePercentage
            )

        return protocolFeeAmount.value

    def _getRateFactor(self, params):
        return sp.nat(1)

    def _getRateProduct(self, normalizedWeights):
        rateProduct = sp.local('rateProduct', self.data.fixedPoint['mulDown']((
            self._getRateFactor(sp.record(
                normalizedWeights=normalizedWeights, provider=self.data.rateProviders[0])),
            self._getRateFactor(sp.record(
                normalizedWeights=normalizedWeights, provider=self.data.rateProviders[1])),
        )))
        with sp.if_(sp.len(normalizedWeights) > 2):
            with sp.for_('i', sp.range(2, sp.len(normalizedWeights))) as i:
                rateProduct.value = self.data.fixedPoint['mulDown']((
                    rateProduct.value,
                    self._getRateFactor(sp.record(
                        normalizedWeights=normalizedWeights, provider=self.data.rateProviders[i]))
                ))

        return rateProduct.value
