import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

import contracts.interfaces.SymmetricEnums as Enums

import contracts.utils.math.FixedPoint as FixedPoint

import contracts.utils.helpers.ScalingHelpers as ScalingHelpers

from contracts.pool_weighted.BaseWeightedPool import BaseWeightedPool

from contracts.pool_weighted.WeightedPoolProtocolFees import WeightedPoolProtocolFees

from contracts.pool_weighted.ExternalWeightedMath import IExternalWeightedMath

from contracts.pool_weighted.ExternalWeightedProtocolFees import IExternalWeightedProtocolFees

from contracts.vault.ProtocolFeesCollector import IProtocolFeesCollector

class IWeightedPool:
    def initialize(pool, params):
        initialize = sp.contract(Types.INITIALIZE_PARAMS, pool, "initialize").open_some(
            "INTERFACE_MISMATCH")
        sp.transfer(params, sp.tez(0), initialize)

    def updateProtocolFeePercentageCache(pool):
        update_protocol_fee_cache = sp.contract(sp.TUnit, pool, "updateProtocolFeePercentageCache").open_some(
            "INTERFACE_MISMATCH")
        sp.transfer(sp.unit, sp.tez(0), update_protocol_fee_cache)


class Types:

    TOKEN = sp.TPair(sp.TAddress, sp.TOption(sp.TNat))
    FEE_CACHE = sp.TPair(sp.TNat, sp.TNat)

    getRateFactor = sp.TLambda(
        sp.TTuple(
            sp.TNat,
            sp.TOption(sp.TAddress),
            sp.TLambda(
                sp.TPair(sp.TNat, sp.TNat), sp.TNat)
        ),
        sp.TNat
    )

    helper = sp.TLambda(
        sp.TTuple(
            sp.TMap(sp.TNat, sp.TNat),
            sp.TMap(sp.TNat, sp.TNat),
            sp.TLambda(
                sp.TPair(sp.TNat, sp.TNat), sp.TNat)
        ),
        sp.TMap(sp.TNat, sp.TNat)
    )

    scaling_helpers = sp.TBigMap(sp.TNat, helper)

    STORAGE = sp.TRecord(
        normalizedWeights=sp.TMap(sp.TNat, sp.TNat),
        scalingFactors=sp.TMap(sp.TNat, sp.TNat),
        tokens=sp.TMap(sp.TNat, TOKEN),
        balances=sp.TBigMap(sp.TAddress, sp.TRecord(
            approvals=sp.TMap(sp.TAddress, sp.TNat),
            balance=sp.TNat)),
        exemptFromYieldFees=sp.TBool,
        feeCache=FEE_CACHE,
        initialized=sp.TBool,
        metadata=sp.TBigMap(sp.TString, sp.TBytes),
        poolId=sp.TOption(sp.TPair(sp.TAddress, sp.TNat)),
        protocolFeesCollector=sp.TOption(sp.TAddress),
        rateProviders=sp.TOption(sp.TMap(sp.TNat, sp.TOption(sp.TAddress))),
        recoveryMode=sp.TBool,
        scaling_helpers=scaling_helpers,
        token_metadata=sp.TBigMap(sp.TNat, sp.TRecord(
            token_id=sp.TNat,
            token_info=sp.TMap(sp.TString, sp.TBytes))),
        totalSupply=sp.TNat,
        vault=sp.TAddress,
        getTokenValue=sp.TLambda(sp.TTuple(
            TOKEN,
            sp.TMap(sp.TNat, TOKEN),
            sp.TMap(sp.TNat, sp.TNat)), sp.TNat),
        fixedPoint=sp.TBigMap(sp.TNat, sp.TLambda(
            sp.TPair(sp.TNat, sp.TNat), sp.TNat)),
        entries=sp.TBigMap(sp.TNat, sp.TNat),
        weightedMathLib=sp.TAddress,
        weightedProtocolFeesLib=sp.TAddress
    )

    INITIALIZE_PARAMS = sp.TRecord(
        tokens=STORAGE.tokens,
        normalizedWeights=STORAGE.normalizedWeights,
        tokenDecimals=sp.TMap(sp.TNat, sp.TNat),
        swapFeePercentage=sp.TNat,
        rateProviders=STORAGE.rateProviders,
    )


def getTokenValue(t):
    sp.set_type(t, sp.TTuple(
        Types.TOKEN,
        sp.TMap(sp.TNat, Types.TOKEN),
        sp.TMap(sp.TNat, sp.TNat)))

    token, tokens, entries,  = sp.match_tuple(
        t, 'token', 'tokens', 'entries')

    entry = sp.local('entry', sp.nat(0))
    with sp.for_('i', sp.range(0, sp.len(entries))) as i:
        with sp.if_(tokens[i] == token):
            entry.value = entries[i]

    with sp.if_(entry.value == 0):
        sp.failwith(Errors.INVALID_TOKEN)

    sp.result(entry.value)


class WeightedPool(
    WeightedPoolProtocolFees,
    BaseWeightedPool,
):
    MAX_TOKENS = 8

    def __init__(
        self,
        owner=sp.address('KT1N5Qpp5DaJzEgEXY1TW6Zne6Eehbxp83XF'),
        vault=sp.address('KT1N5Qpp5DaJzEgEXY1TW6Zne6Eehbxp83XF'),
        name='Symmetric Weighted Pool',
        symbol='SYMMLP',
        weightedMathLib=sp.address('KT1SJtRC6xTfrrhx2ys1bkR3BSCrLNHrmHpy'),
        weightedProtocolFeesLib=sp.address(
            'KT1SJtRC6xTfrrhx2ys1bkR3BSCrLNHrmHpy'),
        tokens=sp.map(l={}, tkey=sp.TNat, tvalue=Types.TOKEN),
        normalizedWeights=sp.map(l={}, tkey=sp.TNat, tvalue=sp.TNat),
        scalingFactors=sp.map(l={}, tkey=sp.TNat, tvalue=sp.TNat),
        swapFeePercentage=sp.nat(1500000000000000),
        rateProviders=sp.none,
        exemptFromYieldFees=True,
        feeCache=(sp.nat(0), sp.nat(0)),
        protocolFeesCollector=sp.address(
            'KT1N5Qpp5DaJzEgEXY1TW6Zne6Eehbxp83XF'),
    ):
        self.init(
            tokens=tokens,
            scalingFactors=scalingFactors,
            normalizedWeights=normalizedWeights,
            initialized=sp.bool(False),
            recoveryMode=sp.bool(False),
            getTokenValue=getTokenValue,
            fixedPoint=sp.big_map({
                Enums.MUL_DOWN: FixedPoint.mulDown,
                Enums.MUL_UP: FixedPoint.mulUp,
                Enums.DIV_DOWN: FixedPoint.divDown,
                Enums.DIV_UP: FixedPoint.divUp,
            }, tkey=sp.TNat, tvalue=sp.TLambda(sp.TPair(sp.TNat, sp.TNat), sp.TNat)),
            entries=sp.big_map({
                Enums.ATH_RATE_PRODUCT: sp.nat(0),
                Enums.POST_JOIN_EXIT_INVARIANT: sp.nat(0),
                Enums.SWAP_FEE_PERCENTAGE: swapFeePercentage,
            }),
            scaling_helpers=sp.big_map({
                0: ScalingHelpers.scale_amounts,
            }),
            weightedMathLib=weightedMathLib,
            weightedProtocolFeesLib=weightedProtocolFeesLib,
        )
        # self.init_type(Types.STORAGE)
        WeightedPoolProtocolFees.__init__(
            self,
            exemptFromYieldFees,
            rateProviders,
            feeCache,
        )
        BaseWeightedPool.__init__(
            self,
            owner,
            vault,
            name,
            symbol,
            protocolFeesCollector,
        )

    @sp.entry_point(lazify = False)
    def updateProtocolFeePercentageCache(self):
        self._beforeProtocolFeeCacheUpdate()

        swapFee = IProtocolFeesCollector.getSwapFeePercentage(self.data.protocolFeesCollector)
        yieldFee = IProtocolFeesCollector.getYieldFeePercentage(self.data.protocolFeesCollector)

        self.data.feeCache = (swapFee, yieldFee)

        

    def _afterInitializePool(
        self,
        invariant,
    ):
        with sp.if_(self.data.exemptFromYieldFees == False):

            self.data.entries[Enums.ATH_RATE_PRODUCT] = IExternalWeightedProtocolFees.getRateProduct(
                self.data.weightedProtocolFeesLib,
                sp.record(
                    normalizedWeights=self.data.normalizedWeights,
                    rateProviders=self.data.rateProviders.open_some(),
                )
            )

        self.data.entries[Enums.POST_JOIN_EXIT_INVARIANT] = invariant

    def _beforeJoinExit(
        self,
        preBalances,
        normalizedWeights,
    ):
        supplyBeforeFeeCollection = self.data.totalSupply

        invariant = IExternalWeightedMath.calculateInvariant(self.data.weightedMathLib, sp.record(
            normalizedWeights=normalizedWeights,
            balances=preBalances,
        ))
        pair = self._getPreJoinExitProtocolFees(
            invariant,
            normalizedWeights,
            supplyBeforeFeeCollection
        )
        protocolFeesToBeMinted, athRateProduct = sp.match_pair(pair)

        return ((supplyBeforeFeeCollection + protocolFeesToBeMinted), invariant)

    def _beforeOnJoinExit(
        self,
        invariant,
        normalizedWeights,
    ):
        supplyBeforeFeeCollection = self.data.totalSupply

        pair = self._getPreJoinExitProtocolFees(
            invariant,
            normalizedWeights,
            supplyBeforeFeeCollection
        )
        protocolFeesToBeMinted, athRateProduct = sp.match_pair(pair)
        with sp.if_(athRateProduct > 0):
            self.data.entries[Enums.ATH_RATE_PRODUCT] = sp.compute(athRateProduct)

        self._payProtocolFees(sp.compute(protocolFeesToBeMinted))

        return (supplyBeforeFeeCollection + protocolFeesToBeMinted)

    def _afterJoinExit(
        self,
        preJoinExitInvariant,
        preBalances,
        balanceDeltas,
        normalizedWeights,
        preJoinExitSupply,
        postJoinExitSupply
    ):

        protocolFeesToBeMinted = self._getPostJoinExitProtocolFees(
            preJoinExitInvariant,
            preBalances,
            balanceDeltas,
            normalizedWeights,
            preJoinExitSupply,
            postJoinExitSupply
        )
        self._payProtocolFees(sp.compute(protocolFeesToBeMinted))

    @sp.onchain_view()
    def getActualSupply(self):
        supply = sp.compute(self.data.totalSupply)

        invariant = self._getInvariant()

        (protocolFeesToBeMinted, athRateProduct) = self._getPreJoinExitProtocolFees(
            invariant,
            sp.compute(self.data.scalingFactors),
            supply
        )

        sp.result(supply + protocolFeesToBeMinted)

    def _beforeProtocolFeeCacheUpdate(self):
        self.onlyUnpaused()

        supply = sp.compute(self.data.totalSupply)

        invariant = self._getInvariant()

        (protocolFeesToBeMinted, athRateProduct) = self._getPreJoinExitProtocolFees(
            invariant,
            sp.compute(self.data.scalingFactors),
            supply,
        )

        self._payProtocolFees(protocolFeesToBeMinted)

        self.data.entries[Enums.POST_JOIN_EXIT_INVARIANT] = invariant

        with sp.if_(self.data.entries[Enums.ATH_RATE_PRODUCT] > 0):
            self.data.entries[Enums.ATH_RATE_PRODUCT] = athRateProduct

    def _onDisableRecoveryMode(self):
        self.data.entries[Enums.POST_JOIN_EXIT_INVARIANT] = self._getInvariant()

        with sp.if_(self.data.exemptFromYieldFees == False):
            athRateProduct = self.data.entries[Enums.ATH_RATE_PRODUCT]
            rateProduct = IExternalWeightedProtocolFees.getRateProduct(
                self.data.weightedProtocolFeesLib,
                sp.record(
                    normalizedWeights=self.data.normalizedWeights,
                    rateProviders=self.data.rateProviders.open_some(),
                )
            )

            with sp.if_(rateProduct > athRateProduct):
                self.data.entries[Enums.ATH_RATE_PRODUCT] = rateProduct


sp.add_compilation_target('Symmetric', WeightedPool())
