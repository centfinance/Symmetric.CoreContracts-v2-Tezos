import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

import contracts.utils.math.FixedPoint as FixedPoint

from contracts.pool_weighted.BaseWeightedPool import BaseWeightedPool

from contracts.pool_weighted.WeightedMath import WeightedMath


class WeightedPool(
    BaseWeightedPool
):

    def __init__(
        self,
        vault,
        tokens,
        normalizedWeights,
        name,
        symbol,
        owner,
    ):
        self.init(
            tokens=tokens,
            scalingFactors=sp.none,
            normalizedWeights=normalizedWeights,
            totalTokens=sp.nat(0),
            maxTokens=sp.nat(8),
            initialized=sp.bool(False),
        )
        self.init_type(
            sp.TRecord(
                tokens=sp.TMap(sp.TNat, sp.TRecord(
                    address=sp.TAddress, id=sp.TNat)),
                scalingFactors=sp.TOption(sp.TMap(sp.TNat, sp.TNat)),
                normalizedWeights=sp.TOption(sp.TMap(sp.TNat, sp.TNat)),
                totalTokens=sp.TNat
            )
        )
        # TODO: ProtocolFeeCache

        # TODO: WeightedPoolProtocolFees

        BaseWeightedPool.__init__(
            self,
            vault,
            name,
            symbol,
            owner,
        )

    @sp.entry_point
    def initialize(
        self,
        vault,
        tokens,
        tokenDecimals,
        normalizedWeights,
        assetManagers,
        swapFeePercentage,
    ):
        sp.verify(self.data.initialized == False)

        numTokens = sp.len(tokens)
        sp.verify((numTokens == sp.len(normalizedWeights))
                  & (numTokens == sp.len(tokenDecimals)))

        self.data._totalTokens = numTokens

        # // Ensure each normalized weight is above the minimum
        normalizedSum = 0
        with sp.for_('i', sp.range(0, numTokens)) as i:
            normalizedWeight = normalizedWeights[i]

            sp.verify(normalizedWeight >=
                      WeightedMath._MIN_WEIGHT, Errors.MIN_WEIGHT)
            normalizedSum = sp.compute(normalizedSum + normalizedWeight)

        # // Ensure that the normalized weights sum to ONE
        sp.verify(normalizedSum == FixedPoint.ONE,
                  Errors.NORMALIZED_WEIGHT_INVARIANT)

        with sp.for_('i', sp.range(0, numTokens)) as i:
            self.data.scalingFactors[i] = self._computeScalingFactor(
                tokenDecimals[i])
        specialization = sp.compute(sp.nat(1)
                                    )
        with sp.if_(numTokens == sp.nat(2)):
            specialization = sp.compute(sp.nat(1))

        super().initialize.f(
            self,
            vault,
            specialization,
            tokens,
            assetManagers,
            swapFeePercentage,
        )

        self.data.initialized = True
