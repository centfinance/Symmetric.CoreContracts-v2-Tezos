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
    """
    Base class for WeightedPools.
    
    Contains swap, join, and exit logic, while delegating the storage and management of the weights to subclasses.
    Derived contracts can opt to:
    - Make weights immutable
    - Allow weights to be mutable
    - Make weights dynamic based on local or external logic.
    """
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
        """
        Returns the current value of the invariant.
        """
        invariant = self._getInvariant()
        sp.result(invariant)

    ###########
    # Base Pool Handlers
    ###########

    ###########
    # Swap
    ###########
    def _onSwapGivenIn(self, params):
        """
        Called when a swap with the Pool occurs, where the amount of tokens entering the Pool is known.
        
        Returns the amount of tokens that will be taken from the Pool in return.

        All amounts inside `swapRequest`, `balanceTokenIn`, and `balanceTokenOut` are upscaled. The swap fee has already
        been deducted from `swapRequest.amount`.

        The return value is also considered upscaled and will be downscaled (rounding down) before returning it to the
        Vault.
        """
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
        """
        Called when a swap with the Pool occurs, where the amount of tokens exiting the Pool is known.
        
        Returns the amount of tokens that will be granted to the Pool in return.

        All amounts inside `swapRequest`, `balanceTokenIn`, and `balanceTokenOut` are upscaled.

        The return value is also considered upscaled and will be downscaled (rounding up) before applying the swap fee
        and returning it to the Vault.
        """
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
    ###########
    # Initialize 
    ###########
    def _beforeInitializePool(self, params):
        """
        Called when the Pool is joined for the first time, i.e., when the SPT total supply is zero.
        
        Returns the amount of SPT to mint and the token amounts the Pool will receive in return.

        Minted SPT will be sent to `recipient`, except for `_getMinimumSpt()`, which will be deducted from this amount 
        and sent to the zero address instead. This ensures that a portion of the SPT remains forever locked there, 
        preventing the total SPT from ever dropping below that value, and ensuring `_onInitializePool` can only be 
        called once in the Pool's lifetime.

        The tokens granted to the Pool will be transferred from `sender`. These amounts are considered upscaled and will
        be downscaled (rounding up) before being returned to the Vault.
        """
        kind = params.userData.kind

        sp.verify(kind == Enums.INIT, Errors.UNINITIALIZED)

        amountsIn = params.userData.amountsIn.open_some()

        length = sp.len(amountsIn)
        sp.verify(length == sp.len(params.scalingFactors))

        upscaledAmounts = sp.compute(self.data.scaling_helpers[0]((
            amountsIn, params.scalingFactors, self.data.fixedPoint[Enums.MUL_DOWN])))
        # Set the initial SPT to the value of the invariant times the number of tokens. This makes SPT supply more
        # consistent in Pools with similar compositions but different number of tokens.
        invariantAfterJoin = IExternalWeightedMath.calculateInvariant(
            self.data.weightedMathLib,
            sp.record(
                normalizedWeights=self.data.normalizedWeights,
                balances=upscaledAmounts,
            ))

        sptAmountOut = invariantAfterJoin * length

        return (sptAmountOut, upscaledAmounts, invariantAfterJoin)

    def _afterInitializePool(self, invariant):
        # Initialization is still a join, so we need to do post-join work. Since we are not paying protocol fees,
        # and all we need to do is update the invariant
        self.data.entries[Enums.POST_JOIN_EXIT_INVARIANT] = invariant


    ###########
    # Join
    ###########
    def _beforeJoinPool(self, params):
        """
        Called whenever the Pool is joined after its first initialization (see `_onInitializePool`).

        Returns:
            - The amount of SPT to mint.
            - The token amounts that the Pool will receive in return.

        Minted SPT will be sent to `recipient`.

        Tokens granted to the Pool will be transferred from `sender`. These amounts are considered upscaled and will 
        be downscaled (rounding up) before being returned to the Vault.

        """
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
        """
        Dispatch code which decodes the provided userdata to perform the specified join type.
        Inheriting contracts may override this function to add additional join types or extra conditions to allow
        or disallow joins under certain circumstances.
        """
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

        with sp.if_(sp.fst(doJoin.value) == 0):
            sp.failwith(Errors.UNHANDLED_JOIN_KIND)

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

        # We join in a single token, so we initialize amountsIn with zeros
        amountsIn = sp.compute(sp.map({}, tkey=sp.TNat, tvalue=sp.TNat))
        with sp.for_('x', sp.range(0, sp.len(params.balances))) as x:
            amountsIn[x] =sp.nat(0)
        # And then assign the result to the selected token
        amountsIn[tokenIndex] = amountIn

        return (sptAmountOut, amountsIn)

    def _joinAllTokensInForExactSPTOut(
        self,
        params
    ):
        sptAmountOut = params.userData.allT.open_some()
        # Note that there is no maximum amountsIn parameter: this is handled by `IVault.joinPool`.

        amountsIn = sp.compute(BasePoolMath.computeProportionalAmountsIn(
            params.balances, params.totalSupply, sptAmountOut, self.data.fixedPoint))

        return (sptAmountOut, amountsIn)

    ###########
    # Exit
    ###########
    def _beforeExitPool(self, params):
        """
        Called whenever the Pool is exited.

        Returns:
            - The amount of SPT to burn.
            - The token amounts for each Pool token that the Pool will grant in return.

        SPT will be burnt from `sender`.

        The Pool will grant tokens to `recipient`. These amounts are considered upscaled and will be downscaled 
        (rounding down) before being returned to the Vault.

        """
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
        """
        Dispatch code which decodes the provided userdata to perform the specified exit type.
        Inheriting contracts may override this function to add additional exit types or extra conditions to allow
        or disallow exit under certain circumstances.
        """
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

        with sp.if_(sp.fst(doExit.value) == 0):
            sp.failwith(Errors.UNHANDLED_EXIT_KIND)

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

        # This is an exceptional situation in which the fee is charged on a token out instead of a token in.
        # We exit in a single token, so we initialize amountsOut with zeros
        amountsOut = sp.compute(sp.map({}, tkey=sp.TNat, tvalue=sp.TNat))
        with sp.for_('x', sp.range(0, sp.len(params.balances))) as x:
            amountsOut[x] =sp.nat(0)
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
        # This is an exceptional situation in which the fee is charged on a token out instead of a token in.
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

        sp.verify(sptAmountIn <= params.userData.maxSPTAmountIn.open_some(),
                  Errors.SPT_OUT_MIN_AMOUNT)

        return (sptAmountIn, upscaledAmounts)
    
    ###########
    # Recovery Mode
    ###########
    def _doRecoveryModeExit(
        self,
        params
    ):
        sptAmountIn = params.userData.sptAmountIn.open_some()
        amountsOut = BasePoolMath.computeProportionalAmountsOut(
            params.balances, params.totalSupply, sptAmountIn, self.data.fixedPoint)
        return (sptAmountIn, amountsOut, 0)
