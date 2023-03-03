import smartpy as sp

import contracts.utils.helpers.ScalingHelpers as ScalingHelpers


class BaseMinimalSwapInfoPool:

    def onSwap(
        self,
        request,
        balanceTokenIn,
        balanceTokenOut
    ):
        # TODO: Check it's not paused

        scalingFactorTokenIn = self._scalingFactor(request.tokenIn)
        scalingFactorTokenOut = self._scalingFactor(request.tokenOut)

        balanceTokenIn = ScalingHelpers._upscale(
            balanceTokenIn, scalingFactorTokenIn)
        balanceTokenOut = ScalingHelpers._upscale(
            balanceTokenOut, scalingFactorTokenOut)

        swapAmount = sp.compute(0)
        with sp.if_(request.kind == 'GIVEN_IN'):
            swapAmount = self._subtractSwapFeeAmount(request.amount)

            swapAmount = ScalingHelpers._upscale(
                swapAmount, scalingFactorTokenIn)

            swapRequest = sp.record(
                tokenIn=request.tokenIn,
                tokenOut=request.tokenOut,
                amount=swapAmount,
            )

            amountOut = self._onSwapGivenIn(sp.record(
                swapRequest=swapRequest,
                currentBalanceTokenIn=balanceTokenIn,
                currentBalanceTokenOut=balanceTokenOut,
            ))

            swapAmount = ScalingHelpers._downscaleDown(
                amountOut, scalingFactorTokenOut)
        with sp.else_():
            swapAmount = ScalingHelpers._upscale(
                request.amount, scalingFactorTokenOut)

            swapRequest = sp.record(
                tokenIn=request.tokenIn,
                tokenOut=request.tokenOut,
                amount=swapAmount,
            )

            amountIn = self._onSwapGivenOut(sp.record(
                swapRequest=swapRequest,
                currentBalanceTokenIn=balanceTokenIn,
                currentBalanceTokenOut=balanceTokenOut,
            ))

            downscaleAmount = ScalingHelpers._downscaleUp(
                amountIn, scalingFactorTokenIn)

            swapAmount = self._addSwapFeeAmount(downscaleAmount)

        return swapAmount
