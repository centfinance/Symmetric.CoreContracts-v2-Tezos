import smartpy as sp

from contracts.pool_utils.external_fees.InvariantGrowthProtocolSwapFees import InvariantGrowthProtocolSwapFees

import contracts.utils.math.FixedPoint as FixedPoint


class WeightedPoolProtocolFees:
    def __init__(self):
        self.update_initial_storage(
            exemptFromYieldFees=False,
            athRateProduct=sp.nat(0),
            rateProviders=sp.map(l={}, tkey=sp.TNat,
                                 tvalue=sp.TOption(sp.TAddress)),
            postJoinExitInvariant=sp.nat(0),
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
            FixedPoint.divDown(params.preJoinExitInvariant,
                               self.data.postJoinExitInvariant),
            FixedPoint.ONE,
            params.protocolSwapFeePercentage,
        )

    def _getYieldProtocolFeesPoolPercentage(self, normalizedWeights):
        percentages = sp.local('percentages', (0, 0))
        with sp.if_(self.data.exemptFromYieldFees == False):

            InvariantGrowthProtocolSwapFees.getProtocolOwnershipPercentage(
                FixedPoint.divDown(rateProduct,
                                   self.data.athRateProduct),
                FixedPoint.ONE,
                self.data.feeCache.yieldFee,
            )
