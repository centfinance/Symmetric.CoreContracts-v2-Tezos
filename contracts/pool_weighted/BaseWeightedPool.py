import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

import contracts.utils.helpers.ScalingHelpers as ScalingHelpers

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

        sp.verify(sp.len(amountsIn.length) == sp.len(params.scalingFactors))
        ScalingHelpers._upscaleArray(amountsIn, params.scalingFactors)

        invariantAfterJoin = WeightedMath._calculateInvariant(
            self.data.normalizedWeights, amountsIn)

        # // Set the initial BPT to the value of the invariant times the number of tokens. This makes BPT supply more
        # // consistent in Pools with similar compositions but different number of tokens.
        sptAmountOut = Math.mul(invariantAfterJoin, amountsIn.length)

        # // Initialization is still a join, so we need to do post-join work. Since we are not paying protocol fees,
        # // and all we need to do is update the invariant, call `_updatePostJoinExit` here instead of `_afterJoinExit`.
        self._updatePostJoinExit(invariantAfterJoin)

        return (sptAmountOut, amountsIn)
