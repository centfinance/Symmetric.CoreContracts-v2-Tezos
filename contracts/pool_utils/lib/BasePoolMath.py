import smartpy as sp

import contracts.utils.math.FixedPoint as FixedPoint


class BasePoolMath:

    def computeProportionalAmountsIn(
        balances,
        sptTotalSupply,
        sptAmountOut
    ):
        # ************************************************************************************
        #  computeProportionalAmountsIn
        #  (per token)
        #  aI = amountIn                   /      sptOut      \
        #  b = balance           aI = b * | ----------------- |
        #  sptOut = sptAmountOut           \  sptTotalSupply  /
        #  spt = sptTotalSupply
        # ************************************************************************************

        #  Since we're computing amounts in, we round up overall. This means rounding up on both the
        #  multiplication and division.

        sptRatio = FixedPoint.divUp(sptAmountOut, sptTotalSupply)

        amountsIn = sp.compute(sp.map({}, tkey=sp.TNat, tvalue=sp.TNat))
        with sp.for_('i', sp.range(0, sp.len(balances)))as i:
            amountsIn[i] = FixedPoint.mulUp(balances[i], sptRatio)

        return amountsIn

    def computeProportionalAmountsOut(
        balances,
        sptTotalSupply,
        sptAmountIn
    ):
        # ************************************************************************************
        #  computeProportionalAmountsIn
        #  (per token)
        #  aI = amountIn                   /      sptOut      \
        #  b = balance           aI = b * | ----------------- |
        #  sptOut = sptAmountOut           \  sptTotalSupply  /
        #  spt = sptTotalSupply
        # ************************************************************************************

        #  Since we're computing amounts in, we round up overall. This means rounding up on both the
        #  multiplication and division.

        sptRatio = FixedPoint.divDown(sptAmountIn, sptTotalSupply)

        amountsOut = sp.compute(sp.map({}, tkey=sp.TNat, tvalue=sp.TNat))
        with sp.for_('i', sp.range(0, sp.len(balances)))as i:
            amountsOut[i] = FixedPoint.mulDown(balances[i], sptRatio)

        return amountsOut
