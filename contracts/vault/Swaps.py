import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

import contracts.interfaces.SymmetricEnums as Enums

import contracts.vault.balances.BalanceAllocation as BalanceAllocation

from contracts.vault.PoolBalances import PoolBalances

from contracts.vault.AssetTransfersHandler import AssetTransfersHandler


class ISwaps:
    TOKEN = sp.TPair(sp.TAddress, sp.TOption(sp.TNat))

    SINGLE_SWAP = sp.TRecord(
        poolId=sp.TPair(sp.TAddress, sp.TNat),
        kind=sp.TNat,
        assetIn=TOKEN,
        assetOut=TOKEN,
        amount=sp.TNat,
    )

    FUND_MANAGEMENT = sp.TRecord(
        sender=sp.TAddress,
        recipient=sp.TAddress,
    )

    t_swap_params = sp.TRecord(
        singleSwap=SINGLE_SWAP,
        funds=FUND_MANAGEMENT,
        limit=sp.TNat,
        deadline=sp.TTimestamp,
    )

    BATCH_SWAP_STEP = sp.TRecord(
        poolId=sp.TPair(sp.TAddress, sp.TNat),
        assetInIndex=sp.TNat,
        assetOutIndex=sp.TNat,
        amount=sp.TNat,
    )

    t_batch_swap_params = sp.TRecord(
        kind=sp.TNat,
        swaps=sp.TMap(sp.TNat, BATCH_SWAP_STEP),
        assets=sp.TMap(sp.TNat, TOKEN),
        funds=FUND_MANAGEMENT,
        limits=sp.TMap(sp.TNat, sp.TInt),
        deadline=sp.TTimestamp,
    )


class Swaps(PoolBalances):
    """
    Implements the Vault's high-level swap functionality.
  
    Users can swap tokens with Pools by calling the `swap` and `batchSwap` functions. They need not trust the Pool
    contracts to do this: all security checks are made by the Vault.
  
    The `swap` function executes a single swap, while `batchSwap` can perform multiple swaps in sequence.
    In each individual swap, tokens of one kind are sent from the sender to the Pool (this is the 'token in'),
    and tokens of another kind are sent from the Pool to the recipient in exchange (this is the 'token out').
    More complex swaps, such as one 'token in' to multiple tokens out can be achieved by batching together
    individual swaps.
    """

    def __init__(self):
        PoolBalances.__init__(self)

    @sp.entry_point(parameter_type=ISwaps.t_swap_params, lazify=False)
    def swap(
        self,
        singleSwap,
        funds,
        limit,
        deadline,
    ):
        """
        Executes a single token swap between a sender and a Pool.
        
        Args:
            singleSwap (ISwaps.SINGLE_SWAP): The details of the swap including pool ID, kind of swap, assets involved, and amount to swap.
            funds (ISwaps.FUND_MANAGEMENT): Addresses of the sender and recipient of the swap.
            limit (sp.TNat): Minimum or maximum amount of tokens for the swap, depending on the kind.
            deadline (sp.TTimestamp): Timestamp by which the swap must be completed, otherwise it will fail.
            
        Raises:
            Errors.SENDER_NOT_ALLOWED: If the sender is not the caller of the function.
            Errors.SWAP_DEADLINE: If the current time is past the deadline.
            Errors.UNKNOWN_AMOUNT_IN_FIRST_SWAP: If the swap amount is 0 or not provided.
            Errors.CANNOT_SWAP_SAME_TOKEN: If input and output tokens are the same.
            Errors.SWAP_LIMIT: If the swapped amount does not meet the given limit.
        """
        self.onlyUnpaused()
        sp.verify(funds.sender == sp.source, Errors.SENDER_NOT_ALLOWED )

        sp.verify(sp.now <= deadline, Errors.SWAP_DEADLINE)

        sp.verify(singleSwap.amount > 0,
                  Errors.UNKNOWN_AMOUNT_IN_FIRST_SWAP)

        sp.verify(singleSwap.assetIn != singleSwap.assetOut,
                  Errors.CANNOT_SWAP_SAME_TOKEN)

        request = sp.record(
            poolId=singleSwap.poolId,
            kind=singleSwap.kind,
            tokenIn=singleSwap.assetIn,
            tokenOut=singleSwap.assetOut,
            amount=singleSwap.amount,
            from_=funds.sender,
            to_=funds.recipient,
        )

        (amountCalculated, amountIn, amountOut) = self._swapWithPool(request)
        checkLimits = sp.eif(
            singleSwap.kind == Enums.GIVEN_IN,
            (amountOut >= limit),
            (amountIn <= limit),
        )
        sp.verify(checkLimits, Errors.SWAP_LIMIT)

        AssetTransfersHandler._receiveAsset(
            singleSwap.assetIn,
            amountIn,
            funds.sender,
        )

        AssetTransfersHandler._sendAsset(
            singleSwap.assetOut,
            amountOut,
            funds.recipient,
        )

    @sp.entry_point(parameter_type=ISwaps.t_batch_swap_params, lazify=False)
    def batchSwap(
        self,
        kind,
        swaps,
        assets,
        funds,
        limits,
        deadline,
    ):
        """
        Executes multiple token swaps in a sequence between a sender and multiple Pools.
        
        Args:
            kind (sp.TNat): Kind of swap, determining how amounts are calculated.
            swaps (sp.TMap): A sequence of individual swaps with details for each.
            assets (sp.TMap): A map of tokens involved in the batch swap.
            funds (ISwaps.FUND_MANAGEMENT): Addresses of the sender and recipient of the swap.
            limits (sp.TMap): Minimum or maximum amounts for each token, depending on the kind.
            deadline (sp.TTimestamp): Timestamp by which all swaps in the batch must be completed, otherwise they will fail.
            
        Raises:
            Errors.SENDER_NOT_ALLOWED: If the sender is not the caller of the function.
            Errors.SWAP_DEADLINE: If the current time is past the deadline.
            Errors.INPUT_LENGTH_MISMATCH: If the lengths of assets and limits don't match.
            Errors.SWAP_LIMIT: If any swapped amount in the batch does not meet the given limits.
        """
        self.onlyUnpaused()
        
        sp.verify(funds.sender == sp.source, Errors.SENDER_NOT_ALLOWED )
        
        sp.verify(sp.now <= deadline, Errors.SWAP_DEADLINE)

        sp.verify(sp.len(assets) == sp.len(limits),
                  Errors.INPUT_LENGTH_MISMATCH)
        # Perform the swaps, updating the Pool token balances and computing the net Vault asset deltas.
        assetDeltas = self._swapWithPools(
            sp.record(
                swaps=swaps,
                assets=assets,
                funds=funds,
                kind=kind))
        # Process asset deltas, by either transferring assets from the sender (for positive deltas) or to the recipient
        # (for negative deltas).
        with sp.for_('i', sp.range(0, sp.len(assets))) as i:
            asset = assets[i]
            delta = assetDeltas[i]
            sp.verify(delta <= limits[i], Errors.SWAP_LIMIT)

            with sp.if_(delta > 0):
                toReceive = sp.as_nat(delta)
                AssetTransfersHandler._receiveAsset(
                    asset, toReceive, funds.sender)

            with sp.if_(delta < 0):
                toSend = abs(delta)
                AssetTransfersHandler._sendAsset(
                    asset, toSend, funds.recipient)

    def _swapWithPools(self, params):
        """
        Performs all `swaps`, calling swap hooks on the Pool contracts and updating their balances. Does not cause
        any transfer of tokens - instead it returns the net Vault token deltas: positive if the Vault should receive
        tokens, and negative if it should send them.
        """
        assetDeltas = sp.compute(sp.map({}, tkey=sp.TNat, tvalue=sp.TInt))

        previousTokenCalculated = sp.local(
            'previousTokenCalculated', (sp.address('tz1burnburnburnburnburnburnburjAYjjX'), sp.none))
        previousAmountCalculated = sp.local(
            'previousAmountCalculated', sp.nat(0))

        with sp.for_('i', sp.range(0, sp.len(params.swaps))) as i:
            withinBounds = (params.swaps[i].assetInIndex < sp.len(params.assets)) & (
                params.swaps[i].assetOutIndex < sp.len(params.assets))

            sp.verify(withinBounds, Errors.OUT_OF_BOUNDS)

            tokenIn = params.assets[params.swaps[i].assetInIndex]
            tokenOut = params.assets[params.swaps[i].assetOutIndex]
            sp.verify(tokenIn != tokenOut, Errors.CANNOT_SWAP_SAME_TOKEN)

            amount = sp.local('amount', params.swaps[i].amount)

            with sp.if_(params.swaps[i].amount == sp.nat(0)):
                # When the amount given is zero, we use the calculated amount for the previous swap, as long as the
                # current swap's given token is the previous calculated token. This makes it possible to swap a
                # given amount of token A for token B, and then use the resulting token B amount to swap for token C.
                sp.verify(i > 0, Errors.UNKNOWN_AMOUNT_IN_FIRST_SWAP)
                usingPreviousToken = (previousTokenCalculated.value == sp.compute(
                    sp.eif(params.kind == Enums.GIVEN_IN, tokenIn, tokenOut)))

                sp.verify(usingPreviousToken,
                          Errors.MALCONSTRUCTED_MULTIHOP_SWAP)
                amount.value = previousAmountCalculated.value

            poolRequest = sp.record(
                poolId=params.swaps[i].poolId,
                kind=params.kind,
                tokenIn=tokenIn,
                tokenOut=tokenOut,
                amount=amount.value,
                from_=params.funds.sender,
                to_=params.funds.recipient,
            )

            (amountCalculated, amountIn, amountOut) = self._swapWithPool(poolRequest)
            previousAmountCalculated.value = amountCalculated

            previousTokenCalculated.value = sp.compute(
                sp.eif(params.kind == Enums.GIVEN_IN, tokenOut, tokenIn))
            
            # Accumulate Vault deltas across swaps
            assetDeltas[params.swaps[i].assetInIndex] = (assetDeltas.get(
                params.swaps[i].assetInIndex, default_value=sp.int(0)) + sp.to_int(amountIn))
            assetDeltas[params.swaps[i].assetOutIndex] = (assetDeltas.get(
                params.swaps[i].assetOutIndex, default_value=sp.int(0)) - sp.to_int(amountOut))

        return assetDeltas

    def _swapWithPool(self, request):
        """
        Performs a swap according to the parameters specified in `request`, calling the Pool's contract hook and
        updating the Pool's balance.
     
        Returns the amount of tokens going into or out of the Vault as a result of this swap, depending on the swap kind.
        """
        pool = sp.fst(request.poolId)
        # Get the calculated amount from the Pool and update its balances
        amountCalculated = self._processMinimalSwapInfoPoolSwapRequest(
            sp.record(
                request=request,
                pool=pool,
            ))

        amountsIn, amountsOut = sp.match_pair(sp.eif(
            request.kind == Enums.GIVEN_IN,
            (request.amount, amountCalculated),
            (amountCalculated, request.amount),
        ))

        sp.emit(sp.record(
            poolId=request.poolId,
            tokenIn=(sp.fst(request.tokenIn),
                     sp.snd(request.tokenIn)),
            tokenOut=(sp.fst(request.tokenOut),
                      sp.snd(request.tokenOut)),
            amountIn=amountsIn,
            amountOut=amountsOut
        ), tag='Swap', with_type=True)

        return (amountCalculated, amountsIn, amountsOut)

    def _processMinimalSwapInfoPoolSwapRequest(self, params):
        tokenInBalance = self._getPoolBalance(
            sp.record(poolId=params.request.poolId, token=params.request.tokenIn))
        tokenOutBalance = self._getPoolBalance(
            sp.record(poolId=params.request.poolId, token=params.request.tokenOut))

        (tokenInBalance, tokenOutBalance, amountCalculated) = self._callMinimalSwapInfoPoolOnSwapHook(
            sp.record(
                request=params.request,
                pool=params.pool,
                tokenInBalance=tokenInBalance,
                tokenOutBalance=tokenOutBalance,
            ))
        self.data.poolsBalances[params.request.poolId][params.request.tokenIn] = tokenInBalance
        self.data.poolsBalances[params.request.poolId][params.request.tokenOut] = tokenOutBalance

        return amountCalculated

    def _callMinimalSwapInfoPoolOnSwapHook(self, params):
        """
        Calls the onSwap hook for a Pool that implements IMinimalSwapInfoPool
        """
        tokenInTotal = (sp.fst(params.tokenInBalance) +
                        sp.snd(params.tokenInBalance))
        tokenOutTotal = (sp.fst(params.tokenOutBalance) +
                         sp.snd(params.tokenOutBalance))

        swapParams = sp.record(
            balanceTokenIn=tokenInTotal,
            balanceTokenOut=tokenOutTotal,
            request=sp.record(
                kind=params.request.kind,
                tokenIn=params.request.tokenIn,
                tokenOut=params.request.tokenOut,
                amount=params.request.amount,
            ),
        )
        # Perform the swap request callback, and compute the new balances for 'token in' and 'token out' after the swap
        amountCalculated = sp.compute(sp.view('onSwap', params.pool,
                                              swapParams, t=sp.TNat).open_some(Errors.ON_SWAP_INVALID))

        amountIn, amountOut = sp.match_pair(sp.compute(sp.eif(
            params.request.kind == Enums.GIVEN_IN,
            (params.request.amount, amountCalculated),
            (amountCalculated, params.request.amount),
        )))

        newTokenInBalance = (
            (sp.fst(params.tokenInBalance) + amountIn), sp.snd(params.tokenInBalance))

        newTokenOutBalance = (sp.as_nat(
            sp.fst(params.tokenOutBalance) - amountOut), sp.snd(params.tokenOutBalance))

        return (newTokenInBalance, newTokenOutBalance, amountCalculated)
