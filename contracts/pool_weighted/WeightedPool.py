import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

import contracts.utils.math.FixedPoint as FixedPoint

from contracts.pool_weighted.BaseWeightedPool import BaseWeightedPool

from contracts.pool_weighted.WeightedMath import WeightedMath


class Types:

    TOKEN = sp.TRecord(
        address=sp.TAddress,
        id=sp.TNat,
    )

    STORAGE = sp.TRecord(
        normalizedWeights=sp.TMap(sp.TNat, sp.TNat),
        scalingFactors=sp.TMap(sp.TNat, sp.TNat),
        tokens=sp.TMap(sp.TNat, TOKEN),
        totalTokens=sp.TNat,
        balances=sp.TBigMap(sp.TAddress, sp.TRecord(
            approvals=sp.TMap(sp.TAddress, sp.TNat),
            balance=sp.TNat)),
        initialized=sp.TBool,
        metadata=sp.TBigMap(sp.TString, sp.TBytes),
        poolId=sp.TOption(sp.TBytes),
        protocolFeesCollector=sp.TOption(sp.TAddress),
        swapFeePercentage=sp.TNat,
        token_metadata=sp.TBigMap(sp.TNat, sp.TRecord(
            token_id=sp.TNat,
            token_info=sp.TMap(sp.TString, sp.TBytes))),
        totalSupply=sp.TNat,
        vault=sp.TAddress
    )

    INITIALIZE_PARAMS = sp.TRecord(
        tokens=STORAGE.tokens,
        normalizedWeights=STORAGE.normalizedWeights,
        tokenDecimals=sp.TMap(sp.TNat, sp.TNat),
        swapFeePercentage=STORAGE.swapFeePercentage,
    )


class WeightedPool(
    BaseWeightedPool
):
    MAX_TOKENS = 8

    def __init__(
        self,
        vault,
        name,
        symbol,
        owner,
    ):
        self.init(
            tokens=sp.map(l={}, tkey=sp.TNat, tvalue=Types.TOKEN),
            scalingFactors=sp.map(l={}, tkey=sp.TNat, tvalue=sp.TNat),
            normalizedWeights=sp.map(l={}, tkey=sp.TNat, tvalue=sp.TNat),
            totalTokens=sp.nat(0),
            initialized=sp.bool(False),
        )
        self.init_type(Types.STORAGE)
        # TODO: ProtocolFeeCache

        # TODO: WeightedPoolProtocolFees

        BaseWeightedPool.__init__(
            self,
            vault,
            name,
            symbol,
            owner,
        )

    @sp.entry_point(parameter_type=Types.INITIALIZE_PARAMS)
    def initialize(self, params):

        sp.verify(self.data.initialized == False)

        numTokens = sp.len(params.tokens)
        sp.verify((numTokens == sp.len(params.normalizedWeights))
                  & (numTokens == sp.len(params.tokenDecimals)))

        self.data.tokens = params.tokens
        self.data.totalTokens = numTokens

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

        with sp.for_('i', sp.range(0, numTokens)) as i:
            self.data.scalingFactors[i] = self._computeScalingFactor(
                params.tokenDecimals[i])

        specialization = sp.local('specialization', sp.nat(1))
        with sp.if_(numTokens == sp.nat(2)):
            specialization.value = sp.nat(2)

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
