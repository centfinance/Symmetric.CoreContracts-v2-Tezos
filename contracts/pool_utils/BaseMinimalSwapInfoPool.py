import smartpy as sp

import contracts.interfaces.SymmetricEnums as Enums

import contracts.utils.helpers.ScalingHelpers as ScalingHelpers

from contracts.pool_utils.BasePool import BasePool


class Types:
    TOKEN = sp.TPair(sp.TAddress, sp.TOption(sp.TNat))

    t_onSwap_params = sp.TRecord(
        balanceTokenIn=sp.TNat,
        balanceTokenOut=sp.TNat,
        request=sp.TRecord(
            kind=sp.TNat,
            tokenIn=TOKEN,
            tokenOut=TOKEN,
            amount=sp.TNat,
        ),
    )


class BaseMinimalSwapInfoPool(BasePool):
    """
    Extension of `BasePool`, adding a handler for `IMinimalSwapInfoPool.onSwap`.
    """
    def __init__(
        self,
        owner,
        vault,
        name,
        symbol,
        protocolFeesCollector,
    ):
        BasePool.__init__(
            self,
            owner,
            vault,
            name,
            symbol,
            protocolFeesCollector,
        )

    ###########
    # Swap Hook
    ###########
    @sp.onchain_view()
    def onSwap(
        self,
        params
    ):
        sp.set_type(params, Types.t_onSwap_params)
        self.onlyUnpaused()

        scalingFactorTokenIn = sp.compute(self.data.getTokenValue((
            params.request.tokenIn,
            self.data.tokens,
            self.data.scalingFactors,
        )))
        scalingFactorTokenOut = sp.compute(self.data.getTokenValue((
            params.request.tokenOut,
            self.data.tokens,
            self.data.scalingFactors,
        )))

        balanceTokenIn = sp.compute(self.data.fixedPoint[Enums.MUL_DOWN]((
            params.balanceTokenIn, scalingFactorTokenIn)))
        balanceTokenOut = sp.compute(self.data.fixedPoint[Enums.MUL_DOWN]((
            params.balanceTokenOut, scalingFactorTokenOut)))

        swapAmount = sp.local('swapAmount', 0)
        with sp.if_(params.request.kind == Enums.GIVEN_IN):
            # Fees are subtracted before scaling, to reduce the complexity of the rounding direction analysis.
            swapAmount.value = self._subtractSwapFeeAmount(
                params.request.amount)
            # upscale
            swapAmount.value = self.data.fixedPoint[Enums.MUL_DOWN](
                (swapAmount.value, scalingFactorTokenIn))
            swapRequest = sp.record(
                tokenIn=params.request.tokenIn,
                tokenOut=params.request.tokenOut,
                amount=swapAmount.value,
            )

            amountOut = self._onSwapGivenIn(sp.record(
                swapRequest=swapRequest,
                currentBalanceTokenIn=balanceTokenIn,
                currentBalanceTokenOut=balanceTokenOut,
            ))
            # amountOut tokens are exiting the Pool, so we round down.
            swapAmount.value = self.data.fixedPoint[Enums.DIV_DOWN]((
                amountOut, scalingFactorTokenOut))

        with sp.else_():
            # upscale
            swapAmount.value = self.data.fixedPoint[Enums.MUL_DOWN]((
                params.request.amount, scalingFactorTokenOut))

            swapRequest = sp.record(
                tokenIn=params.request.tokenIn,
                tokenOut=params.request.tokenOut,
                amount=swapAmount.value,
            )

            amountIn = self._onSwapGivenOut(sp.record(
                swapRequest=swapRequest,
                currentBalanceTokenIn=balanceTokenIn,
                currentBalanceTokenOut=balanceTokenOut,
            ))

            # amountIn tokens are entering the Pool, so we round up.
            downscaleAmount = self.data.fixedPoint[Enums.DIV_UP]((
                amountIn, scalingFactorTokenIn))
            # Fees are added after scaling happens, to reduce the complexity of the rounding direction analysis.
            swapAmount.value = self._addSwapFeeAmount(downscaleAmount)

        sp.result(swapAmount.value)
