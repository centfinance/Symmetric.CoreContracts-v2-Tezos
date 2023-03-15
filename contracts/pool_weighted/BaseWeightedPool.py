import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

import contracts.utils.helpers.ScalingHelpers as ScalingHelpers

from contracts.pool_weighted.ExternalWeightedMath import IExternalWeightedMath

from contracts.pool_utils.BaseMinimalSwapInfoPool import BaseMinimalSwapInfoPool

from contracts.pool_utils.lib.BasePoolMath import BasePoolMath


class BaseWeightedPool(
    BaseMinimalSwapInfoPool
):
    def __init__(
        self,
        vault,
        name,
        symbol,
    ):
        BaseMinimalSwapInfoPool.__init__(
            self,
            vault,
            name,
            symbol,
        )

    def _onSwapGivenIn(self, params):
        tokens = self.data.tokens
        normalizedWeights = self.data.normalizedWeights
        getTokenValue = self.data.getTokenValue

        return IExternalWeightedMath.calcOutGivenIn(
            self.data.weightedMathLib,
            sp.record(
                balanceIn=params.currentBalanceTokenIn,
                weightIn=sp.compute(getTokenValue((
                    params.swapRequest.tokenIn,
                    tokens,
                    normalizedWeights,
                ))),
                balanceOut=params.currentBalanceTokenOut,
                weightOut=sp.compute(getTokenValue((
                    params.swapRequest.tokenOut,
                    tokens,
                    normalizedWeights,
                ))),
                amountIn=params.swapRequest.amount,
            )
        )

    def _onSwapGivenOut(self, params):
        tokens = self.data.tokens
        normalizedWeights = self.data.normalizedWeights
        getTokenValue = self.data.getTokenValue

        return IExternalWeightedMath.calcInGivenOut(
            self.data.weightedMathLib,
            sp.record(
                balanceIn=params.currentBalanceTokenIn,
                weightIn=sp.compute(getTokenValue((
                    params.swapRequest.tokenIn,
                    tokens,
                    normalizedWeights,
                ))),
                balanceOut=params.currentBalanceTokenOut,
                weightOut=sp.compute(getTokenValue((
                    params.swapRequest.tokenOut,
                    tokens,
                    normalizedWeights,
                ))),
                amountOut=params.swapRequest.amount,
            )
        )

    def _onInitializePool(self, params):
        kind = params.userData.kind
        # TODO: Use an enum
        sp.verify(kind == 'INIT', Errors.UNINITIALIZED)

        amountsIn = params.userData.amountsIn.open_some()

        length = sp.len(amountsIn)
        sp.verify(length == sp.len(params.scalingFactors))

        upscaledAmounts = sp.compute(ScalingHelpers._upscaleArray(
            amountsIn, params.scalingFactors, self.data.fixedPoint['mulDown']))

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
        # TODO: Used for protocol Fees
        # self._updatePostJoinExit(invariantAfterJoin)

        return (sptAmountOut, amountsIn)

    def _onJoinPool(self, params):
        # TODO: Implement protocol fees
        # (preJoinExitSupply,  preJoinExitInvariant) = self._beforeJoinExit(params.balances, params.normalizedWeights);

        (sptAmpountOut, amountsIn) = self._doJoin(
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

        return (sptAmpountOut, amountsIn)

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
        # TODO: add fail if no kind matches
        return (sp.fst(doJoin.value), sp.snd(doJoin.value))

    def _joinExactTokensInForSPTOut(
        self,
        params,
    ):
        amountsIn = params.userData.amountsIn.open_some()
        sp.verify(sp.len(params.balances) == sp.len(amountsIn))

        upscaledAmounts = sp.compute(ScalingHelpers._upscaleArray(
            amountsIn, params.scalingFactors, self.data.fixedPoint['mulDown']))

        sptAmountOut = sp.compute(IExternalWeightedMath.calcSptOutGivenExactTokensIn(
            self.data.weightedMathLib,
            sp.record(
                balances=params.balances,
                normalizedWeights=params.normalizedWeights,
                amountsIn=upscaledAmounts,
                totalSupply=params.totalSupply,
                swapFeePercentage=self.data.entries['swapFeePercentage'],
            )
        ))

        sp.verify(sptAmountOut >= params.userData.minSPTAmountOut.open_some(),
                  Errors.SPT_OUT_MIN_AMOUNT)

        return (sptAmountOut, upscaledAmounts)

    def _joinTokenInForExactSPTOut(
        self,
        params
    ):
        # Note that there is no maximum amountIn parameter: this is handled by `IVault.joinPool`.
        tokenIndex = params.userData.tokenIndex.open_some()
        sptAmountOut = params.userData.sptAmountOut.open_some()
        sp.verify(tokenIndex < sp.len(
            params.balances), Errors.OUT_OF_BOUNDS)

        amountIn = sp.compute(IExternalWeightedMath.calcTokenInGivenExactSptOut(
            self.data.weightedMathLib,
            sp.record(
                balance=params.balances[tokenIndex],
                normalizedWeight=params.normalizedWeights[tokenIndex],
                sptAmountOut=sptAmountOut,
                sptTotalSupply=params.totalSupply,
                swapFeePercentage=self.data.entries['swapFeePercentage'],
            )
        ))

        # // We join in a single token, so we initialize amountsIn with zeros
        amountsIn = sp.compute(sp.map({}, tkey=sp.TNat, tvalue=sp.TNat))
        # // And then assign the result to the selected token
        amountsIn[tokenIndex] = amountIn

        return (sptAmountOut, amountsIn)

    def _joinAllTokensInForExactSPTOut(
        self,
        params
    ):
        sptAmountOut = params.userData.allT.open_some()
        # // Note that there is no maximum amountsIn parameter: this is handled by `IVault.joinPool`.

        amountsIn = sp.compute(BasePoolMath.computeProportionalAmountsIn(
            params.balances, params.totalSupply, sptAmountOut, self.data.fixedPoint))

        return (sptAmountOut, amountsIn)

    def _onExitPool(self, params):
        # TODO: Implement protocol fees
        # (preJoinExitSupply,  preJoinExitInvariant) = self._beforeJoinExit(params.balances, params.normalizedWeights);

        (sptAmpountIn, amountsOut) = self._doExit(
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

        return (sptAmpountIn, amountsOut)

    def _doExit(self, params):
        doExit = sp.local('doExit', (0, {}))
        with sp.if_(params.userData.kind == 'EXACT_SPT_IN_FOR_ONE_TOKEN_OUT'):
            (doExit.value) = self._exitExactSPTInForTokenOut(
                sp.record(
                    balances=params.balances,
                    normalizedWeights=params.normalizedWeights,
                    totalSupply=params.totalSupply,
                    userData=params.userData
                )
            )
        with sp.if_(params.userData.kind == 'EXACT_SPT_IN_FOR_TOKENS_OUT'):
            doExit.value = self._exitExactSPTInForTokensOut(
                sp.record(
                    balances=params.balances,
                    totalSupply=params.totalSupply,
                    userData=params.userData
                )
            )
        with sp.if_(params.userData.kind == 'SPT_IN_FOR_EXACT_TOKENS_OUT'):
            doExit.value = self._exitSPTInForExactTokensOut(params)

        # TODO: add fail if no kind matches
        return (sp.fst(doExit.value), sp.snd(doExit.value))

    def _exitExactSPTInForTokenOut(
        self,
        params
    ):
        # Note that there is no minimum amountOut parameter: this is handled by `IVault.exitPool`.
        tokenIndex = params.userData.tokenIndex.open_some()
        sptAmountIn = params.userData.sptAmountIn.open_some()

        sp.verify(tokenIndex < sp.len(
            params.balances), Errors.OUT_OF_BOUNDS)

        amountOut = IExternalWeightedMath.calcTokenOutGivenExactSptIn(
            self.data.weightedMathLib,
            sp.record(
                balance=params.balances[tokenIndex],
                normalizedWeight=params.normalizedWeights[tokenIndex],
                sptAmountIn=sptAmountIn,
                sptTotalSupply=params.totalSupply,
                swapFeePercentage=self.data.entries['swapFeePercentage'],
            )
        )

        # // We join in a single token, so we initialize amountsIn with zeros
        amountsOut = sp.compute(sp.map({}, tkey=sp.TNat, tvalue=sp.TNat))
        # // And then assign the result to the selected token
        amountsOut[tokenIndex] = amountOut

        return (sptAmountIn, amountsOut)

    def _exitExactSPTInForTokensOut(
        self,
        params
    ):
        sptAmountIn = params.userData.sptAmountIn.open_some()
        # Note that there is no minimum amountOut parameter: this is handled by `IVault.exitPool`.
        amountsOut = BasePoolMath.computeProportionalAmountsOut(
            params.balances, params.totalSupply, sptAmountIn, self.data.fixedPoint)

        return (sptAmountIn, amountsOut)

    def _exitSPTInForExactTokensOut(
        self,
        params,
    ):
        amountsOut = params.userData.amountsOut.open_some()
        sp.verify(sp.len(params.balances) ==
                  sp.len(amountsOut))

        upscaledAmounts = ScalingHelpers._upscaleArray(
            amountsOut, params.scalingFactors, self.data.fixedPoint['mulDown'])

        sptAmountIn = IExternalWeightedMath.calcSptInGivenExactTokensOut(
            self.data.weightedMathLib,
            sp.record(
                balances=params.balances,
                normalizedWeights=params.normalizedWeights,
                amountsOut=upscaledAmounts,
                totalSupply=params.totalSupply,
                swapFeePercentage=self.data.entries['swapFeePercentage'],
            )
        )

        sp.verify(sptAmountIn >= params.userData.maxSPTAmountIn.open_some(),
                  Errors.SPT_OUT_MIN_AMOUNT)

        return (sptAmountIn, upscaledAmounts)

    def _doRecoveryModeExit(
        self,
        params
    ):
        sptAmountIn = params.userData.sptAmountIn.open_some()
        amountsOut = BasePoolMath.computeProportionalAmountsOut(
            params.balances, params.totalSupply, sptAmountIn, self.data.fixedPoint)
        return (sptAmountIn, amountsOut)
