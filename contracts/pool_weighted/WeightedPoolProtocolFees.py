import smartpy as sp

from contracts.pool_utils.external_fees.InvariantGrowthProtocolSwapFees import InvariantGrowthProtocolSwapFees

from contracts.interfaces.IRateProvider import IRateProvider

import contracts.utils.math.FixedPoint as FixedPoint

from contracts.pool_weighted.WeightedMath import WeightedMath

from contracts.pool_weighted.ExternalWeightedProtocolFees import IExternalWeightedProtocolFees


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

        self.data.feeCache = params.feeCache

        self.data.rateProviders = params.rateProviders

    def _getYieldFeeExemption(self, rateProviders):
        exempt = sp.local('exempt', True)

        with sp.for_('i', sp.range(0, sp.len(rateProviders)))as i:
            with sp.if_(rateProviders[i] != sp.none):
                exempt.value = False

        return exempt.value

    def _getPreJoinExitProtocolFees(
        self,
        preJoinExitInvariant,
        normalizedWeights,
        preJoinExitSupply,
    ):
        swapFee, yieldFee = sp.match_record(sp.compute(
            self.data.feeCache), 'swapFee', 'yieldFee')
        entries = sp.compute(self.data.entries)
        pair = IExternalWeightedProtocolFees.getPreJoinExitProtocolFees(self.data.weightedProtocolFeesLib, sp.record(
            preJoinExitSupply=preJoinExitSupply,
            preJoinExitInvariant=preJoinExitInvariant,
            swapFee=swapFee,
            postJoinExitInvariant=entries['postJoinExitInvariant'],
            normalizedWeights=normalizedWeights,
            rateProviders=sp.compute(self.data.rateProviders),
            athRateProduct=entries['athRateProduct'],
            yieldFee=yieldFee,
            exemptFromYieldFees=self.data.exemptFromYieldFees
        ))
        return (sp.fst(pair), sp.snd(pair))

    def _getPostJoinExitProtocolFees(
        self,
        preJoinExitInvariant,
        preBalances,
        balanceDeltas,
        normalizedWeights,
        preJoinExitSupply,
        postJoinExitSupply
    ):
        feeCache = sp.compute(self.data.feeCache)
        pair = IExternalWeightedProtocolFees.getPostJoinExitProtocolFees(self.data.weightedProtocolFeesLib, sp.record(
            preJoinExitSupply=preJoinExitSupply,
            postJoinExitSupply=postJoinExitSupply,
            preJoinExitInvariant=preJoinExitInvariant,
            preBalances=preBalances,
            balanceDeltas=balanceDeltas,
            normalizedWeights=normalizedWeights,
            swapFee=feeCache.swapFee,
        ))

        self.data.entries['postJoinExitInvariant'] = sp.snd(pair)

        return sp.fst(pair)
