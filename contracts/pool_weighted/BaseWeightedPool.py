import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

import contracts.interfaces.SymmetricEnums as Enums

import contracts.utils.helpers.ScalingHelpers as ScalingHelpers

from contracts.pool_weighted.ExternalWeightedMath import IExternalWeightedMath

from contracts.pool_utils.BaseMinimalSwapInfoPool import BaseMinimalSwapInfoPool

from contracts.pool_utils.lib.BasePoolMath import BasePoolMath

# ///
TOKEN = sp.TPair(sp.TAddress, sp.TOption(sp.TNat))


class BaseWeightedPool(
    BaseMinimalSwapInfoPool
):
    def __init__(
        self,
        owner,
        vault,
        name,
        symbol,
        protocolFeesCollector,
    ):
        BaseMinimalSwapInfoPool.__init__(
            self,
            owner,
            vault,
            name,
            symbol,
            protocolFeesCollector,
        )

    def _getInvariant(self):
        p = sp.compute(sp.view('getPoolTokens', self.data.vault, self.data.poolId.open_some(), t=sp.TPair(
            sp.TMap(sp.TNat, TOKEN),
            sp.TMap(sp.TNat, sp.TNat),
        )).open_some(Errors.GET_POOL_TOKENS_INVALID))

        upscaledBalances = sp.compute(self.data.scaling_helpers[0]((
            sp.snd(p), self.data.scalingFactors, self.data.fixedPoint[Enums.MUL_DOWN])))

        invariant = IExternalWeightedMath.calculateInvariant(self.data.weightedMathLib, sp.record(
            normalizedWeights=self.data.normalizedWeights,
            balances=upscaledBalances
        ))
        return invariant

    @sp.onchain_view()
    def getInvariant(self):
        invariant = self._getInvariant()
        sp.result(invariant)

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

    def _beforeInitializePool(self, params):
        kind = params.userData.kind
        # TODO: Use an enum
        sp.verify(kind == Enums.INIT, Errors.UNINITIALIZED)

        amountsIn = params.userData.amountsIn.open_some()

        length = sp.len(amountsIn)
        sp.verify(length == sp.len(params.scalingFactors))

        upscaledAmounts = sp.compute(self.data.scaling_helpers[0]((
            amountsIn, params.scalingFactors, self.data.fixedPoint[Enums.MUL_DOWN])))

        invariantAfterJoin = IExternalWeightedMath.calculateInvariant(
            self.data.weightedMathLib,
            sp.record(
                normalizedWeights=self.data.normalizedWeights,
                balances=upscaledAmounts,
            ))

        sptAmountOut = invariantAfterJoin * length

        return (sptAmountOut, amountsIn, invariantAfterJoin)

    def _afterInitializePool(self, invariant):

        self.data.entries[Enums.POST_JOIN_EXIT_INVARIANT] = invariant

        # return (sptAmountOut, amountsIn)

    def _beforeJoinPool(self, params):
        weights = sp.compute(self.data.normalizedWeights)

        (preJoinExitSupply, invariant) = self._beforeJoinExit(
            params.balances, weights)
        (sptAmpountOut, amountsIn) = self._doJoin(
            sp.record(
                balances=params.balances,
                normalizedWeights=weights,
                scalingFactors=params.scalingFactors,
                totalSupply=preJoinExitSupply,
                userData=params.userData
            )
        )

        return (sptAmpountOut, amountsIn, invariant)

    def _afterJoinPool(self, params):
        weights = sp.compute(self.data.normalizedWeights)
        preJoinExitSupply = self._beforeOnJoinExit(
            params.invariant, weights)

        self._afterJoinExit(
            params.invariant,
            params.balances,
            params.amountsIn,
            weights,
            preJoinExitSupply,
            (preJoinExitSupply + params.sptAmountOut),
        )

    def _doJoin(self, params):
        doJoin = sp.local('doJoin', (0, {}))
        with sp.if_(params.userData.kind == Enums.EXACT_TOKENS_IN_FOR_SPT_OUT):
            doJoin.value = self._joinExactTokensInForSPTOut(params)
        with sp.if_(params.userData.kind == Enums.TOKEN_IN_FOR_EXACT_SPT_OUT):
            doJoin.value = self._joinTokenInForExactSPTOut(
                sp.record(
                    balances=params.balances,
                    normalizedWeights=params.normalizedWeights,
                    totalSupply=params.totalSupply,
                    userData=params.userData
                )
            )
        with sp.if_(params.userData.kind == Enums.ALL_TOKENS_IN_FOR_EXACT_SPT_OUT):
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

        upscaledAmounts = sp.compute(self.data.scaling_helpers[0]((
            amountsIn, params.scalingFactors, self.data.fixedPoint[Enums.MUL_DOWN])))

        sptAmountOut = IExternalWeightedMath.calcSptOutGivenExactTokensIn(
            self.data.weightedMathLib,
            sp.record(
                balances=params.balances,
                normalizedWeights=params.normalizedWeights,
                amountsIn=upscaledAmounts,
                totalSupply=params.totalSupply,
                swapFeePercentage=self.data.entries[Enums.SWAP_FEE_PERCENTAGE],
            )
        )

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

        amountIn = IExternalWeightedMath.calcTokenInGivenExactSptOut(
            self.data.weightedMathLib,
            sp.record(
                balance=params.balances[tokenIndex],
                normalizedWeight=params.normalizedWeights[tokenIndex],
                sptAmountOut=sptAmountOut,
                sptTotalSupply=params.totalSupply,
                swapFeePercentage=self.data.entries[Enums.SWAP_FEE_PERCENTAGE],
            )
        )

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

    def _beforeExitPool(self, params):
        weights = self.data.normalizedWeights

        (preJoinExitSupply, invariant) = self._beforeJoinExit(
            params.balances, weights)

        (sptAmpountIn, amountsOut) = self._doExit(
            sp.record(
                balances=params.balances,
                normalizedWeights=weights,
                scalingFactors=params.scalingFactors,
                totalSupply=preJoinExitSupply,
                userData=params.userData
            )
        )

        return (sptAmpountIn, amountsOut, invariant)

    def _afterExitPool(self, params):
        weights = sp.compute(self.data.normalizedWeights)

        preJoinExitSupply = self._beforeOnJoinExit(
            params.invariant, weights)

        self._afterJoinExit(
            params.invariant,
            params.balances,
            params.amountsOut,
            weights,
            preJoinExitSupply,
            sp.as_nat(preJoinExitSupply - params.sptAmountIn),
        )

    def _doExit(self, params):
        doExit = sp.local('doExit', (0, {}))
        with sp.if_(params.userData.kind == Enums.EXACT_SPT_IN_FOR_ONE_TOKEN_OUT):
            (doExit.value) = self._exitExactSPTInForTokenOut(
                sp.record(
                    balances=params.balances,
                    normalizedWeights=params.normalizedWeights,
                    totalSupply=params.totalSupply,
                    userData=params.userData
                )
            )
        with sp.if_(params.userData.kind == Enums.EXACT_SPT_IN_FOR_TOKENS_OUT):
            doExit.value = self._exitExactSPTInForTokensOut(
                sp.record(
                    balances=params.balances,
                    totalSupply=params.totalSupply,
                    userData=params.userData
                )
            )
        with sp.if_(params.userData.kind == Enums.SPT_IN_FOR_EXACT_TOKENS_OUT):
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
                swapFeePercentage=self.data.entries[Enums.SWAP_FEE_PERCENTAGE],
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

        upscaledAmounts = sp.compute(self.data.scaling_helpers[0]((
            amountsOut, params.scalingFactors, self.data.fixedPoint[Enums.MUL_DOWN])))

        sptAmountIn = IExternalWeightedMath.calcSptInGivenExactTokensOut(
            self.data.weightedMathLib,
            sp.record(
                balances=params.balances,
                normalizedWeights=params.normalizedWeights,
                amountsOut=upscaledAmounts,
                totalSupply=params.totalSupply,
                swapFeePercentage=self.data.entries[Enums.SWAP_FEE_PERCENTAGE],
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
