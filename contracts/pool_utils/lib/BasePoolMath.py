import smartpy as sp

import contracts.interfaces.SymmetricEnums as Enums


class BasePoolMath:

    def computeProportionalAmountsIn(
        balances,
        sptTotalSupply,
        sptAmountOut,
        math
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

        sptRatio = math[Enums.DIV_UP]((sptAmountOut, sptTotalSupply))

        amountsIn = sp.compute(sp.map({}, tkey=sp.TNat, tvalue=sp.TNat))
        with sp.for_('i', sp.range(0, sp.len(balances)))as i:
            amountsIn[i] = math[Enums.MUL_UP]((balances[i], sptRatio))

        return amountsIn

    def computeProportionalAmountsOut(
        balances,
        sptTotalSupply,
        sptAmountIn,
        math,
    ):
        # **********************************************************************************************
        #  computeProportionalAmountsOut                                                             //
        #  (per token)                                                                               //
        #  aO = tokenAmountOut             /        sptIn         \                                  //
        #  b = tokenBalance      a0 = b * | ---------------------  |                                 //
        #  sptIn = sptAmountIn             \     sptTotalSupply    /                                 //
        #  spt = sptTotalSupply                                                                      //
        # **********************************************************************************************

        #  Since we're computing an amount out, we round down overall. This means rounding down on both the
        #  multiplication and division.

        sptRatio = math[Enums.DIV_DOWN]((sptAmountIn, sptTotalSupply))

        amountsOut = sp.compute(sp.map({}, tkey=sp.TNat, tvalue=sp.TNat))
        with sp.for_('i', sp.range(0, sp.len(balances)))as i:
            amountsOut[i] = math[Enums.MUL_DOWN]((balances[i], sptRatio))

        return amountsOut
