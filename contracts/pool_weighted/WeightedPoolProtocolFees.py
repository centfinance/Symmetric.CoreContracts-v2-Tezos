"""
WeightedPoolProtocolFees

This class encapsulates the methods related to protocol fees for the WeightedPool contract. It provides mechanisms to calculate pre-join, post-join, pre-exit, and post-exit protocol fees.

The class interfaces with the ExternalWeightedPoolProtocolFees contract to fetch fee-related values using on-chain views.

Classes:
- WeightedPoolProtocolFees: Class responsible for protocol fee-related operations in the context of a WeightedPool.

"""

import smartpy as sp

import contracts.interfaces.SymmetricEnums as Enums

from contracts.pool_weighted.ExternalWeightedProtocolFees import IExternalWeightedProtocolFees


class WeightedPoolProtocolFees:
    """
    WeightedPoolProtocolFees Class

    This class defines methods that interact with protocol fees for the WeightedPool contract. It utilizes the ExternalWeightedPoolProtocolFees contract's on-chain views to fetch and compute various fee-related metrics.

    Attributes:
        exemptFromYieldFees: Flag to determine if the pool is exempt from yield fees.
        rateProviders: Optional mapping of token index to rate provider addresses.
        feeCache: A tuple containing cached values of swap fee and yield fee.

    Methods:
        __init__: Initializes a new instance of the WeightedPoolProtocolFees class.
        _getPreJoinExitProtocolFees: Calculates protocol fees related to pre-join and pre-exit.
        _getPostJoinExitProtocolFees: Calculates protocol fees related to post-join and post-exit.
    """
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
            postJoinExitInvariant=entries[Enums.POST_JOIN_EXIT_INVARIANT],
            normalizedWeights=normalizedWeights,
            rateProviders=sp.compute(self.data.rateProviders),
            athRateProduct=entries[Enums.ATH_RATE_PRODUCT],
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

        self.data.entries[Enums.POST_JOIN_EXIT_INVARIANT] = sp.snd(pair)

        return sp.fst(pair)
