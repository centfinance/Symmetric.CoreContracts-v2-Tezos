import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

import contracts.utils.helpers.ScalingHelpers as ScalingHelpers

import contracts.pool_weighted.WeightedMath as WeightedMath

from contracts.pool_utils.BasePool import BasePool


class BaseWeightedPool(
    BasePool
):
    def __init__(
        self,
        vault,
        name,
        symbol,
        owner,
    ):
        BasePool.__init__(
            self,
            vault,
            name,
            symbol,
            owner,
        )

    def _onInitializePool(self, params):
        kind = params.userData.kind
        # TODO: Use an enum
        sp.verify(kind == 'INIT', Errors.UNINITIALIZED)

        amountsIn = params.userData.amountsIn

        length = sp.len(amountsIn)
        sp.verify(length == sp.len(params.scalingFactors))

        upscaledAmounts = ScalingHelpers._upscaleArray(
            amountsIn, params.scalingFactors)

        invariantAfterJoin = WeightedMath._calculateInvariant(
            self.data.normalizedWeights, upscaledAmounts)

        # Set the initial SPT to the value of the invariant times the number of tokens. This makes SPT supply more
        # consistent in Pools with similar compositions but different number of tokens.
        # sptAmountOut = Math.mul(invariantAfterJoin, amountsIn.length)
        sptAmountOut = invariantAfterJoin * length

        # Initialization is still a join, so we need to do post-join work. Since we are not paying protocol fees,
        # and all we need to do is update the invariant, call `_updatePostJoinExit` here instead of `_afterJoinExit`.
        self._updatePostJoinExit(invariantAfterJoin)

        return (sptAmountOut, amountsIn)
