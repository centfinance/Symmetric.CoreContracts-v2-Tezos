import smartpy as sp

from contracts.pool_utils.external_fees.InvariantGrowthProtocolSwapFees import InvariantGrowthProtocolSwapFees

from contracts.interfaces.IRateProvider import IRateProvider

import contracts.utils.math.FixedPoint as FixedPoint

from contracts.pool_weighted.WeightedMath import WeightedMath

from contracts.pool_weighted.ExternalWeightedProtocolFees import IExternalWeightedProtocolFees


class WeightedPoolProtocolFees:
    def __init__(
        self,
        exemptFromYieldFees=True,
        rateProviders=sp.none,
        feeCache=(sp.nat(0), sp.nat(0)),
    ):
        self.update_initial_storage(
            exemptFromYieldFees=exemptFromYieldFees,
            rateProviders=sp.set_type_expr(rateProviders, sp.TOption(
                sp.TMap(sp.TNat, sp.TOption(sp.TAddress)))),
            feeCache=feeCache,
        )

    def _getPreJoinExitProtocolFees(
        self,
        preJoinExitInvariant,
        normalizedWeights,
        preJoinExitSupply,
    ):
        swapFee, yieldFee = sp.match_pair(self.data.feeCache)

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
        pair = IExternalWeightedProtocolFees.getPostJoinExitProtocolFees(self.data.weightedProtocolFeesLib, sp.record(
            preJoinExitSupply=preJoinExitSupply,
            postJoinExitSupply=postJoinExitSupply,
            preJoinExitInvariant=preJoinExitInvariant,
            preBalances=preBalances,
            balanceDeltas=balanceDeltas,
            normalizedWeights=normalizedWeights,
            swapFee=sp.fst(self.data.feeCache),
        ))

        self.data.entries['postJoinExitInvariant'] = sp.snd(pair)

        return sp.fst(pair)
