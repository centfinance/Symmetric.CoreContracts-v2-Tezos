import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

import contracts.utils.helpers.ScalingHelpers as ScalingHelpers

from contracts.pool_weighted.WeightedMath import WeightedMath

from contracts.pool_utils.BasePool import BasePool

from contracts.pool_utils.lib.BasePoolMath import BasePoolMath


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
        sp.set_type(params, sp.TRecord(
            userData=sp.TRecord(
                amountsIn=sp.TMap(sp.TNat, sp.TNat),
                kind=sp.TString,
            ),
            scalingFactors=sp.TMap(sp.TNat, sp.TNat),
        ))
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
        # TODO: Used for protocol Fees
        # self._updatePostJoinExit(invariantAfterJoin)

        return (sptAmountOut, amountsIn)

    def _onJoinPool(self, params):
        # TODO: Implement protocol fees
        # (preJoinExitSupply,  preJoinExitInvariant) = self._beforeJoinExit(params.balances, params.normalizedWeights);

        pair = self._doJoin(
            sp.record(
                balances=params.balances,
                normalizedWeights=self.data.normalizedWeights,
                scalingFactors=params.scalingFactors,
                totalSupply=self.data.totalSupply,
                userData=params.userData
            )
        )
        # TODO: Implement protocol fees
        # self._afterJoinExit(
        #     preJoinExitInvariant= preJoinExitInvariant,
        #     balances = params.balances,
        #     amountsIn = amountsIn,
        #     normalizedWeights = self.data.normalizedWeights,
        #     preJoinExitSupply = preJoinExitInvariant,
        #     preJoinExitSupply.add(bptAmountOut)
        # );

        return (0, {})

    def _doJoin(self, params):
        doJoin = sp.local('doJoin', (0, {}))
        with sp.if_(params.userData.kind == 'EXACT_TOKENS_IN_FOR_SPT_OUT'):
            doJoin.value = self._joinExactTokensInForSPTOut(params)
        with sp.if_(params.userData.kind == 'TOKEN_IN_FOR_EXACT_SPT_OUT'):
            doJoin.value = self._joinTokenInForExactSPTOut(
                sp.record(
                    balances=params.balances,
                    normalizedWeights=params.normalizedWeights,
                    totalSupply=params.totalSupply,
                    userData=params.userData
                )
            )
        with sp.if_(params.userData.kind == 'ALL_TOKENS_IN_FOR_EXACT_SPT_OUT'):
            doJoin.value = self._joinAllTokensInForExactSPTOut(
                sp.record(
                    balances=params.balances,
                    totalSupply=params.totalSupply,
                    userData=params.userData
                )
            )
        return doJoin.value

    def _joinExactTokensInForSPTOut(
        self,
        params,
    ):
        sp.verify(sp.len(params.balances) == sp.len(params.userData.amountsIn))

        ScalingHelpers._upscaleArray(
            params.userData.amountsIn, params.scalingFactors)

        sptAmountOut = WeightedMath._calcSptOutGivenExactTokensIn(
            balances=params.balances,
            normalizedWeights=params.normalizedWeights,
            amountsIn=params.userData.amountsIn,
            totalSupply=params.totalSupply,
            swapFeePercentage=self.data.swapFeePercentage,
        )

        sp.verify(sptAmountOut >= params.userData.minSPTAmountOut,
                  Errors.SPT_OUT_MIN_AMOUNT)

        return (0, params.userData.amountsIn)

    def _joinTokenInForExactSPTOut(
        self,
        params
    ):
        # Note that there is no maximum amountIn parameter: this is handled by `IVault.joinPool`.

        sp.verify(params.userData.tokenIndex < sp.len(
            params.balances), Errors.OUT_OF_BOUNDS)

        amountIn = WeightedMath._calcTokenInGivenExactSptOut(
            params.balances[params.userData.tokenIndex],
            params.normalizedWeights[params.userData.tokenIndex],
            params.userData.sptAmountOut,
            params.totalSupply,
            self.data.swapFeePercentage
        )

        # // We join in a single token, so we initialize amountsIn with zeros
        amountsIn = sp.map({}, tkey=sp.TNat, tvalue=sp.TNat)
        # // And then assign the result to the selected token
        amountsIn[params.userData.tokenIndex] = amountIn

        return (params.userData.sptAmountOut, amountsIn)

    def _joinAllTokensInForExactSPTOut(
        self,
        params
    ):
        sptAmountOut = params.userData.allT
        # // Note that there is no maximum amountsIn parameter: this is handled by `IVault.joinPool`.

        amountsIn = BasePoolMath.computeProportionalAmountsIn(
            params.balances, params.totalSupply, sptAmountOut)

        return (sptAmountOut, amountsIn)
