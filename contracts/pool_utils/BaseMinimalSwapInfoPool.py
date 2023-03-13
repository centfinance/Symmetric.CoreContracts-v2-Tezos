import smartpy as sp

import contracts.utils.helpers.ScalingHelpers as ScalingHelpers

from contracts.pool_utils.BasePool import BasePool


class Types:
    TOKEN = sp.TRecord(
        address=sp.TAddress,
        id=sp.TNat,
        FA2=sp.TBool,
    )

    t_onSwap_params = sp.TRecord(
        balanceTokenIn=sp.TNat,
        balanceTokenOut=sp.TNat,
        request=sp.TRecord(
            kind=sp.TString,
            tokenIn=TOKEN,
            tokenOut=TOKEN,
            amount=sp.TNat,
        ),
    )


class BaseMinimalSwapInfoPool(BasePool):
    def __init__(
        self,
        vault,
        name,
        symbol,
    ):
        BasePool.__init__(
            self,
            vault,
            name,
            symbol,
        )

    @sp.onchain_view()
    def onSwap(
        self,
        params
    ):
        sp.set_type(params, Types.t_onSwap_params)
        # TODO: Check it's not paused
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

        balanceTokenIn = ScalingHelpers._upscale(
            params.balanceTokenIn, scalingFactorTokenIn)
        balanceTokenOut = ScalingHelpers._upscale(
            params.balanceTokenOut, scalingFactorTokenOut)

        swapAmount = sp.local('swapAmount.value', 0)
        with sp.if_(params.request.kind == 'GIVEN_IN'):
            swapAmount.value = self._subtractSwapFeeAmount(
                params.request.amount)

            swapAmount.value = ScalingHelpers._upscale(
                swapAmount.value, scalingFactorTokenIn)

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

            swapAmount.value = ScalingHelpers._downscaleDown(
                amountOut, scalingFactorTokenOut)

        with sp.else_():
            swapAmount.value = ScalingHelpers._upscale(
                params.request.amount, scalingFactorTokenOut)

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

            downscaleAmount = ScalingHelpers._downscaleUp(
                amountIn, scalingFactorTokenIn)

            swapAmount.value = self._addSwapFeeAmount(downscaleAmount)

        sp.result(swapAmount.value)
