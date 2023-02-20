import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

import contracts.utils.helpers.ScalingHelpers as ScalingHelpers

from contracts.pool_weighted.WeightedMath import WeightedMath

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

        (bptAmountOut, amountsIn) = self._doJoin(
            sp.record(
                sender=params.sender,
                balances=params.balances,
                normalizedWeights=self.data.normalizedWeights,
                scalingFactors=params.scalingFactors,
                preJoinExitSupply=self.data.totalSupply,
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

        return (bptAmountOut, amountsIn)

    def _doJoin(self, params):
        doJoin = sp.local('doJoin', sp.none)
        with sp.if_(params.userData.kind == 'EXACT_TOKENS_IN_FOR_BPT_OUT'):
            doJoin.value = self._joinExactTokensInForBPTOut(params)
        with sp.if_(params.userData.kind == 'TOKEN_IN_FOR_EXACT_BPT_OUT'):
            doJoin.value = self._joinTokenInForExactBPTOut(
                sp.record(
                    balances=params.balances,
                    normalizedWeights=params.normalizedWeights,
                    totalSupply=params.totalSupply,
                    userData=params.userData
                )
            )
        with sp.if_(params.userData.kind == 'ALL_TOKENS_IN_FOR_EXACT_BPT_OUT'):
            doJoin.value = self._joinAllTokensInForExactBPTOut(
                sp.record(
                    balances=params.balances,
                    totalSupply=params.totalSupply,
                    userData=params.userData
                )
            )

    def _joinExactTokensInForBPTOut(
        self,
        params,
    ):
        (amountsIn, minBPTAmountOut) = params.userData.exactTokensInForBptOut()
        sp.verify(sp.len(params.balances) == sp.len(amountsIn))

        self._upscaleArray(amountsIn, params.scalingFactors)

        bptAmountOut = WeightedMath._calcBptOutGivenExactTokensIn(
            balances,
            normalizedWeights,
            amountsIn,
            totalSupply,
            getSwapFeePercentage()
        )

        sp.verify(bptAmountOut >= minBPTAmountOut, Errors.BPT_OUT_MIN_AMOUNT)

        return (bptAmountOut, amountsIn)

    def _joinTokenInForExactBPTOut(
        self,
        params
    ):
        (bptAmountOut, tokenIndex) = params.userData.tokenInForExactBptOut()
        # Note that there is no maximum amountIn parameter: this is handled by `IVault.joinPool`.

        sp.verify(params.tokenIndex < sp.len(
            params.balances), Errors.OUT_OF_BOUNDS)

        amountIn = WeightedMath._calcTokenInGivenExactBptOut(
            balances[tokenIndex],
            normalizedWeights[tokenIndex],
            bptAmountOut,
            totalSupply,
            self.getSwapFeePercentage()
        )

        # // We join in a single token, so we initialize amountsIn with zeros
        amountsIn = sp.map({}, tkey=sp.TNat, tvalue=sp.TNat)
        # // And then assign the result to the selected token
        amountsIn[params.tokenIndex] = amountIn

        return (bptAmountOut, amountsIn)

    def _joinAllTokensInForExactBPTOut(
        self,
        params
    ):
        bptAmountOut = params.userData.allT
        # // Note that there is no maximum amountsIn parameter: this is handled by `IVault.joinPool`.

        amountsIn = BasePoolMath.computeProportionalAmountsIn(
            balances, totalSupply, bptAmountOut)

        return (bptAmountOut, amountsIn)
