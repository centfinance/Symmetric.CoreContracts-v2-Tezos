import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

import contracts.utils.math.FixedPoint as FixedPoint

import contracts.utils.helpers.ScalingHelpers as ScalingHelpers

from contracts.pool_weighted.BaseWeightedPool import BaseWeightedPool

from contracts.pool_weighted.WeightedPoolProtocolFees import WeightedPoolProtocolFees

from contracts.pool_weighted.WeightedMath import WeightedMath

from contracts.pool_weighted.ExternalWeightedMath import IExternalWeightedMath


class Types:

    TOKEN = sp.TRecord(
        address=sp.TAddress,
        id=sp.TNat,
        FA2=sp.TBool,
    )

    FEE_CACHE = sp.TRecord(
        swapFee=sp.TNat,
        yieldFee=sp.TNat,
        aumFee=sp.TNat,
    )
    # TOKEN = sp.TTuple(sp.TAddress, sp.TNat, sp.TBool)
    # FEE_CACHE = sp.TTuple(sp.TNat, sp.TNat, sp.TNat)

    helper = sp.TLambda(
        sp.TTuple(
            sp.TMap(sp.TNat, sp.TNat),
            sp.TMap(sp.TNat, sp.TNat),
            sp.TLambda(
                sp.TPair(sp.TNat, sp.TNat), sp.TNat)
        ),
        sp.TMap(sp.TNat, sp.TNat)
    )

    scaling_helpers = sp.TBigMap(sp.TString, helper)

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
        poolId=sp.TOption(sp.TBytes),
        protocolFeesCollector=sp.TOption(sp.TAddress),
        rateProviders=sp.TMap(sp.TNat, sp.TOption(sp.TAddress)),
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
        fixedPoint=sp.TBigMap(sp.TString, sp.TLambda(
            sp.TPair(sp.TNat, sp.TNat), sp.TNat)),
        entries=sp.TBigMap(sp.TString, sp.TNat),
        weightedMathLib=sp.TAddress
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
        vault=sp.address('KT1N5Qpp5DaJzEgEXY1TW6Zne6Eehbxp83XF'),
        name='Symmetric Weighted Pool',
        symbol='SYMMLP',
        weightedMathLib=sp.address('KT1SJtRC6xTfrrhx2ys1bkR3BSCrLNHrmHpy'),
    ):
        self.init(
            tokens=sp.map(l={}, tkey=sp.TNat, tvalue=Types.TOKEN),
            scalingFactors=sp.map(l={}, tkey=sp.TNat, tvalue=sp.TNat),
            normalizedWeights=sp.map(l={}, tkey=sp.TNat, tvalue=sp.TNat),
            initialized=sp.bool(False),
            recoveryMode=sp.bool(False),
            getTokenValue=getTokenValue,
            fixedPoint=sp.big_map({
                "mulDown": FixedPoint.mulDown,
                "mulUp": FixedPoint.mulUp,
                "divDown": FixedPoint.divDown,
                "divUp": FixedPoint.divUp,
                "powDown": FixedPoint.powDown,
                "powUp": FixedPoint.powUp,
                "pow": FixedPoint.pow,
            }, tkey=sp.TString, tvalue=sp.TLambda(sp.TPair(sp.TNat, sp.TNat), sp.TNat)),
            entries=sp.big_map({
                'totalTokens': sp.nat(0),
                'athRateProduct': sp.nat(0),
                'postJoinExitInvariant': sp.nat(0),
                'swapFeePercentage': sp.nat(0),
            }),
            scaling_helpers=sp.big_map({
                "scale": ScalingHelpers.scale_amounts,
            }),
            weightedMathLib=weightedMathLib,
        )
        # self.init_type(Types.STORAGE)
        # TODO: ProtocolFeeCache

        WeightedPoolProtocolFees.__init__(self)
        BaseWeightedPool.__init__(
            self,
            vault,
            name,
            symbol,
        )

    @sp.entry_point(parameter_type=Types.INITIALIZE_PARAMS, lazify=False)
    def initialize(self, params):

        sp.verify(self.data.initialized == False)

        numTokens = sp.len(params.tokens)
        sp.verify((numTokens == sp.len(params.normalizedWeights))
                  & (numTokens == sp.len(params.tokenDecimals)))

        self.data.tokens = params.tokens
        self.data.entries['totalTokens'] = numTokens

        # // Ensure each normalized weight is above the minimum
        normalizedSum = sp.local('normalizedSum', 0)
        with sp.for_('i', sp.range(0, numTokens)) as i:
            normalizedWeight = params.normalizedWeights[i]

            sp.verify(normalizedWeight >=
                      WeightedMath._MIN_WEIGHT, Errors.MIN_WEIGHT)
            normalizedSum.value = normalizedSum.value + normalizedWeight

        # // Ensure that the normalized weights sum to ONE
        sp.verify(normalizedSum.value == FixedPoint.ONE,
                  Errors.NORMALIZED_WEIGHT_INVARIANT)

        self.data.normalizedWeights = params.normalizedWeights

        with sp.for_('i', sp.range(0, numTokens)) as i:
            self.data.scalingFactors[i] = self._computeScalingFactor(
                params.tokenDecimals[i])

        specialization = sp.local('specialization', sp.nat(1))
        with sp.if_(numTokens == sp.nat(2)):
            specialization.value = sp.nat(2)

        self._initializeProtocolFees(sp.record(
            numTokens=numTokens,
            rateProviders=params.rateProviders,
        ))

        super().initialize.f(
            self,
            sp.record(
                vault=self.data.vault,
                specialization=specialization.value,
                tokens=params.tokens,
                assetManagers=sp.none,
                swapFeePercentage=params.swapFeePercentage,
            )
        )

        self.data.initialized = True

    def _onInitializePool(
        self,
        params,
    ):
        with sp.if_(self.data.exemptFromYieldFees == False):
            self.data.entries['athRateProduct'] = self._getRateProduct(
                self.data.normalizedWeights)

        kind = params.userData.kind
        # TODO: Use an enum
        sp.verify(kind == 'INIT', Errors.UNINITIALIZED)

        amountsIn = params.userData.amountsIn.open_some()

        length = sp.len(amountsIn)
        sp.verify(length == sp.len(params.scalingFactors))

        upscaledAmounts = sp.compute(self.data.scaling_helpers['scale']((
            amountsIn, params.scalingFactors, self.data.fixedPoint['mulDown'])))

        invariantAfterJoin = sp.compute(IExternalWeightedMath.calculateInvariant(
            self.data.weightedMathLib,
            sp.record(
                normalizedWeights=self.data.normalizedWeights,
                balances=upscaledAmounts,
            )))

        # Set the initial SPT to the value of the invariant times the number of tokens. This makes SPT supply more
        # consistent in Pools with similar compositions but different number of tokens.
        # sptAmountOut = Math.mul(invariantAfterJoin, amountsIn.length)
        sptAmountOut = invariantAfterJoin * length

        # Initialization is still a join, so we need to do post-join work. Since we are not paying protocol fees,
        # and all we need to do is update the invariant, call `_updatePostJoinExit` here instead of `_afterJoinExit`.
        self.data.entries['postJoinExitInvariant'] = invariantAfterJoin

        return (sptAmountOut, amountsIn)

    def _beforeJoinExit(
        self,
        preBalances,
        normalizedWeights,
    ):
        supplyBeforeFeeCollection = sp.compute(self.data.totalSupply)

        invariant = IExternalWeightedMath.calculateInvariant(self.data.weightedMathLib, sp.record(
            normalizedWeights=normalizedWeights,
            balances=preBalances,
        ))

        (protocolFeesToBeMinted, athRateProduct) = self._getPreJoinExitProtocolFees(
            invariant,
            normalizedWeights,
            supplyBeforeFeeCollection
        )

        return (supplyBeforeFeeCollection + protocolFeesToBeMinted)

    def _beforeOnJoinExit(
        self,
        preBalances,
        normalizedWeights,
    ):
        supplyBeforeFeeCollection = sp.compute(self.data.totalSupply)

        invariant = IExternalWeightedMath.calculateInvariant(self.data.weightedMathLib, sp.record(
            normalizedWeights=normalizedWeights,
            balances=preBalances,
        ))

        (protocolFeesToBeMinted, athRateProduct) = self._getPreJoinExitProtocolFees(
            invariant,
            normalizedWeights,
            supplyBeforeFeeCollection
        )

        with sp.if_(athRateProduct > 0):
            self.data.entries['athRateProduct'] = sp.compute(athRateProduct)

        self._payProtocolFees(sp.compute(protocolFeesToBeMinted))

        return ((supplyBeforeFeeCollection + protocolFeesToBeMinted), invariant)

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

    def _onDisableRecoveryMode(self):
        self.data.entries['postJoinExitInvariant'] = self.getInvariant()

        with sp.if_(self.data.exemptFromYieldFees == False):
            athRateProduct = self.data.entries['athRateProduct']
            rateProduct = self._getRateProduct(
                sp.compute(self.data.normalizedWeights))

            with sp.if_(rateProduct > athRateProduct):
                self.data.entries['athRateProduct'] = rateProduct
