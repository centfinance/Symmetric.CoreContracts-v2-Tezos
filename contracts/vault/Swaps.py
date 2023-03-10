import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

import contracts.vault.balances.BalanceAllocation as BalanceAllocation

from contracts.vault.PoolBalances import PoolBalances

from contracts.vault.AssetTransfersHandler import AssetTransfersHandler


class ISwaps:
    TOKEN = sp.TRecord(
        address=sp.TAddress,
        id=sp.TNat,
        FA2=sp.TBool,
    )

    SINGLE_SWAP = sp.TRecord(
        poolId=sp.TBytes,
        kind=sp.TString,
        assetIn=TOKEN,
        assetOut=TOKEN,
        amount=sp.TNat,
    )

    FUND_MANAGEMENT = sp.TRecord(
        sender=sp.TAddress,
        fromInternalBalance=sp.TBool,
        recipient=sp.TAddress,
        toInternalBalance=sp.TBool,
    )

    t_swap_params = sp.TRecord(
        singleSwap=SINGLE_SWAP,
        funds=FUND_MANAGEMENT,
        limit=sp.TNat,
        deadline=sp.TTimestamp,
    )

    BATCH_SWAP_STEP = sp.TRecord(
        poolId=sp.TBytes,
        assetInIndex=sp.TNat,
        assetOutIndex=sp.TNat,
        amount=sp.TNat,
    )

    t_batch_swap_params = sp.TRecord(
        kind=sp.TString,
        swaps=sp.TMap(sp.TNat, BATCH_SWAP_STEP),
        assets=sp.TMap(sp.TNat, TOKEN),
        funds=FUND_MANAGEMENT,
        limits=sp.TMap(sp.TNat, sp.TInt),
        deadline=sp.TTimestamp,
    )


class Swaps(PoolBalances):

    def __init__(self):
        PoolBalances.__init__(self)

    @sp.entry_point(parameter_type=ISwaps.t_swap_params)
    def swap(
        self,
        singleSwap,
        funds,
        limit,
        deadline,
    ):
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
            singleSwap.kind == 'GIVEN_IN',
            (amountOut >= limit),
            (amountIn <= limit),
        )
        sp.verify(checkLimits, Errors.SWAP_LIMIT)

        AssetTransfersHandler._receiveAsset(
            singleSwap.assetIn,
            amountIn,
            funds.sender,
            funds.fromInternalBalance
        )

        AssetTransfersHandler._sendAsset(
            singleSwap.assetOut,
            amountOut,
            funds.recipient,
            funds.toInternalBalance
        )
        # TODO: Handle remaining Tez

    @sp.entry_point(parameter_type=ISwaps.t_batch_swap_params)
    def batchSwap(
        self,
        kind,
        swaps,
        assets,
        funds,
        limits,
        deadline,
    ):
        sp.verify(sp.now <= deadline, Errors.SWAP_DEADLINE)

        sp.verify(sp.len(assets) == sp.len(limits),
                  Errors.INPUT_LENGTH_MISMATCH)

        assetDeltas = self._swapWithPools(
            sp.record(
                swaps=swaps,
                assets=assets,
                funds=funds,
                kind=kind))
        # TODO: Handle remaining Tez
        # wrappedTez = 0
        with sp.for_('i', sp.range(0, sp.len(assets))) as i:
            asset = assets[i]
            delta = assetDeltas[i]
            sp.verify(delta <= limits[i], Errors.SWAP_LIMIT)

            with sp.if_(delta > 0):
                toReceive = sp.as_nat(delta)
                AssetTransfersHandler._receiveAsset(
                    asset, toReceive, funds.sender, funds.fromInternalBalance)
                # TODO: Handle remaining Tez
                # if (_isETH(asset)) {
                #     wrappedEth = wrappedEth.add(toReceive);
            with sp.if_(delta < 0):
                toSend = abs(delta)
                AssetTransfersHandler._sendAsset(asset, toSend, funds.recipient,
                                                 funds.toInternalBalance)

    def _swapWithPools(self, params):
        assetDeltas = sp.compute(sp.map({}, tkey=sp.TNat, tvalue=sp.TInt))

        previousTokenCalculated = sp.local(
            'previousTokenCalculated', sp.record(address=sp.address('tz1'), id=sp.nat(0), FA2=False))
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
                sp.verify(i > 0, Errors.UNKNOWN_AMOUNT_IN_FIRST_SWAP)
                usingPreviousToken = (previousTokenCalculated.value == sp.compute(
                    sp.eif(params.kind == 'GIVEN_IN', tokenIn, tokenOut)))
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
                sp.eif(params.kind == 'GIVEN_IN', tokenOut, tokenIn))

            assetDeltas[params.swaps[i].assetInIndex] = (assetDeltas.get(
                params.swaps[i].assetInIndex, default_value=sp.int(0)) + sp.to_int(amountIn))
            assetDeltas[params.swaps[i].assetOutIndex] = (assetDeltas.get(
                params.swaps[i].assetOutIndex, default_value=sp.int(0)) - sp.to_int(amountOut))

        return assetDeltas

    def _swapWithPool(self, request):
        pool = self._getPoolAddress(request.poolId)
        specialization = self._getPoolSpecialization(request.poolId)

        amountCalculated = sp.local('amountCalculated', 0)
        # with sp.if_(specialization == sp.nat(2)):
        #     amountCalculated = self._processTwoTokenPoolSwapRequest(
        #         request, pool)
        # with sp.else_():
        #     with sp.if_(specialization == sp.nat(1)):
        amountCalculated.value = self._processMinimalSwapInfoPoolSwapRequest(
            sp.record(
                request=request,
                pool=pool,
            ))
        # with sp.else_():
        #     amountCalculated = self._processGeneralPoolSwapRequest(
        #         request, pool)

        amountsIn, amountsOut = sp.match_pair(sp.eif(
            request.kind == 'GIVEN_IN',
            (request.amount, amountCalculated.value),
            (amountCalculated.value, request.amount),
        ))

        sp.emit(sp.record(
            poolId=request.poolId,
            tokenIn=(request.tokenIn.address,
                     request.tokenIn.id),
            tokenOut=(request.tokenOut.address,
                      request.tokenOut.id),
            amountIn=amountsIn,
            amountOut=amountsOut
        ), tag='Swap', with_type=True)

        return (amountCalculated.value, amountsIn, amountsOut)

    def _processMinimalSwapInfoPoolSwapRequest(self, params):
        tokenInBalance = self._getMinimalSwapInfoPoolBalance(
            sp.record(poolId=params.request.poolId, token=params.request.tokenIn))
        tokenOutBalance = self._getMinimalSwapInfoPoolBalance(
            sp.record(poolId=params.request.poolId, token=params.request.tokenOut))

        (tokenInBalance, tokenOutBalance, amountCalculated) = self._callMinimalSwapInfoPoolOnSwapHook(
            sp.record(
                request=params.request,
                pool=params.pool,
                tokenInBalance=tokenInBalance,
                tokenOutBalance=tokenOutBalance,
            ))

        self.data._minimalSwapInfoPoolsBalances[params.request.poolId][params.request.tokenIn] = tokenInBalance
        self.data._minimalSwapInfoPoolsBalances[params.request.poolId][params.request.tokenOut] = tokenOutBalance

        return amountCalculated

    def _callMinimalSwapInfoPoolOnSwapHook(self, params):
        tokenInTotal = (params.tokenInBalance.cash +
                        params.tokenInBalance.managed)
        tokenOutTotal = (params.tokenOutBalance.cash +
                         params.tokenOutBalance.managed)

        lastChangeBlock = sp.max(
            params.tokenInBalance.lastChangeBlock, params.tokenOutBalance.lastChangeBlock)

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

        amountCalculated = sp.view('onSwap', params.pool,
                                   swapParams, t=sp.TNat).open_some("Invalid view")

        amountsIn, amountsOut = sp.match_pair(sp.compute(sp.eif(
            params.request.kind == 'GIVEN_IN',
            (params.request.amount, amountCalculated),
            (amountCalculated, params.request.amount),
        )))

        newTokenInBalance = BalanceAllocation.toBalance(
            (params.tokenInBalance.cash + amountsIn),
            params.tokenInBalance.managed,
            lastChangeBlock,
        )

        newTokenOutBalance = BalanceAllocation.toBalance(
            sp.as_nat(params.tokenOutBalance.cash - amountsOut),
            params.tokenOutBalance.managed,
            lastChangeBlock,
        )

        return (newTokenInBalance, newTokenOutBalance, amountCalculated)
