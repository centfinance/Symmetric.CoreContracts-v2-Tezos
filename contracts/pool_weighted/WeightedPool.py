import smartpy as sp

from contracts.pool_weighted.BaseWeightedPool import BaseWeightedPool

from contracts.pool_weighted.WeightedMath import WeightedMath

import contracts.utils.math.FixedPoint as FixedPoint

import contracts.interfaces.SymmetricErrors as Errors


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
        specialization,
        tokens,
        tokenDecimals,
        normalizedWeights,
        rateProviders,
        assetManagers,
        swapFeePercentage,
    ):
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
            normalizedSum = normalizedSum.add(normalizedWeight)

        # // Ensure that the normalized weights sum to ONE
        sp.verify(normalizedSum == FixedPoint.ONE,
                  Errors.NORMALIZED_WEIGHT_INVARIANT)

        with sp.for_('i', sp.range(0, numTokens)) as i:
            self.data.scalingFactors[i] = self._computeScalingFactor(
                tokenDecimals[i])
