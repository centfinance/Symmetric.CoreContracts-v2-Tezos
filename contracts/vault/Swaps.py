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
        poolId=sp.Tbytes,
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
        deadline=sp.TNat,
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

        poolRequest = sp.record(
            poolId=singleSwap.poolId,
            kind=singleSwap.kind,
            tokenIn=singleSwap.assetIn,
            tokenOut=singleSwap.assetOut,
            amount=singleSwap.amount,
            userData=singleSwap.userData,
            from_=funds.sender,
            to_=funds.recipient,
        )

        (amountCalculated, amountIn, amountOut) = self._swapWithPool(poolRequest)

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
