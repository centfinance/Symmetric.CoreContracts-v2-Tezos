import smartpy as sp

import contracts.vault.balances.BalanceAllocation as BalanceAllocation

from contracts.vault.PoolBalances import PoolBalances


class Swaps(PoolBalances):

    def __init__(self):
        PoolBalances.__init__(self)

    @sp.entry_point
    def swap(self, params):
        (
            newTokenInBalance,
            newTokenOutBalance,
            amountCalculated
        ) = self._callMinimalSwapInfoPoolOnSwapHook(params)
        sp.trace(newTokenInBalance)

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

        amounts = sp.eif(
            params.request.kind == 'GIVEN_IN',
            (params.request.amount, amountCalculated),
            (amountCalculated, params.request.amount),
        )

        newTokenInBalance = BalanceAllocation.toBalance(
            (params.tokenInBalance.cash + sp.fst(amounts)),
            params.tokenInBalance.managed,
            lastChangeBlock,
        )

        newTokenOutBalance = BalanceAllocation.toBalance(
            sp.as_nat(params.tokenOutBalance.cash - sp.snd(amounts)),
            params.tokenInBalance.managed,
            lastChangeBlock,
        )

        return (newTokenInBalance, newTokenOutBalance, amountCalculated)
