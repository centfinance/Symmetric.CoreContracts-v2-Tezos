import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

import contracts.vault.balances.BalanceAllocation as BalanceAllocation

from contracts.vault.PoolBalances import PoolBalances

from contracts.vault.AssetTransfersHandler import AssetTransfersHandler


class Swaps(PoolBalances):

    def __init__(self):
        PoolBalances.__init__(self)

    @sp.entry_point
    def swap(self, params):
        sp.verify(sp.now <= params.deadline, Errors.SWAP_DEADLINE)

        sp.verify(params.singleSwap.amount > 0,
                  Errors.UNKNOWN_AMOUNT_IN_FIRST_SWAP)

        sp.verify(params.tokenIn != params.tokenOut,
                  Errors.CANNOT_SWAP_SAME_TOKEN)

        poolRequest = sp.record(
            poolId=params.singleSwap.poolId,
            kind=params.singleSwap.kind,
            tokenIn=params.tokenIn,
            tokenOut=params.tokenOut,
            amount=params.singleSwap.amount,
            userData=params.singleSwap.userData,
            from_=params.funds.sender,
            to_=params.funds.recipient,
        )

        (amountCalculated, amountIn, amountOut) = self._swapWithPool(poolRequest)

        checkLimits = sp.eif(
            params.singleSwap.kind == 'GIVEN_IN',
            (amountOut >= params.limit),
            (amountIn <= params.limit),
        )
        sp.verify(checkLimits, Errors.SWAP_LIMIT)

        AssetTransfersHandler._receiveAsset(
            params.singleSwap.assetIn,
            amountIn,
            params.funds.sender,
            params.funds.fromInternalBalance
        )

        AssetTransfersHandler._sendAsset(
            params.singleSwap.assetOut,
            amountOut,
            params.funds.recipient,
            params.funds.toInternalBalance
        )
        # TODO: Handle remaining Tez

    def _swapWithPool(self, params):
        pool = self._getPoolAddress(params.poolId)
        specialization = self._getPoolSpecialization(params.poolId)

        amountCalculated = sp.local('amountCalculated', 0)
        # with sp.if_(specialization == sp.nat(2)):
        #     amountCalculated = self._processTwoTokenPoolSwapRequest(
        #         request, pool)
        # with sp.else_():
        #     with sp.if_(specialization == sp.nat(1)):
        amountCalculated.value = self._processMinimalSwapInfoPoolSwapRequest(
            sp.record(
                request=params.request,
                poolId=params.poolId,
                pool=pool))
        # with sp.else_():
        #     amountCalculated = self._processGeneralPoolSwapRequest(
        #         request, pool)

        amountsIn, amountsOut = sp.match_pair(sp.eif(
            params.request.kind == 'GIVEN_IN',
            (params.request.amount, amountCalculated.value),
            (amountCalculated.value, params.request.amount),
        ))

        sp.emit(sp.record(
            poolId=params.poolId,
            tokenIn=(params.request.tokenIn.address,
                     params.request.tokenIn.id),
            tokenOut=(params.request.tokenOut.address,
                      params.request.tokenOut.id),
            amountIn=amountsIn,
            amountOut=amountsOut
        ), tag='Swap', with_type=True)

        return sp.tuple(l=(amountCalculated.value, amountsIn, amountsOut))

    def _processMinimalSwapInfoPoolSwapRequest(self, params):
        tokenInBalance = self._getMinimalSwapInfoPoolBalance(
            sp.record(poolId=params.poolId, token=params.request.tokenIn))
        tokenOutBalance = self._getMinimalSwapInfoPoolBalance(
            sp.record(poolId=params.poolId, token=params.request.tokenOut))

        (tokenInBalance, tokenOutBalance, amountCalculated) = self._callMinimalSwapInfoPoolOnSwapHook(
            sp.record(
                request=params.request,
                pool=params.pool,
                tokenInBalance=tokenInBalance,
                tokenOutBalance=tokenOutBalance,
            ))

        self.data._minimalSwapInfoPoolsBalances[params.poolId][params.request.tokenIn] = tokenInBalance
        self.data._minimalSwapInfoPoolsBalances[params.poolId][params.request.tokenOut] = tokenOutBalance

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
