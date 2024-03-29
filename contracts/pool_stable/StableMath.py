import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors
import contracts.utils.math.FixedPoint as FixedPoint

MIN_AMP = 1
MAX_AMP = 5000
AMP_PRECISION = 1000

MAX_STABLE_TOKENS = 5

ONE = sp.nat(1000000000000000000)


class StableMath:
    def calculateInvariant(p):
        amp, balances = sp.match_pair(p)
        totalBalance = sp.local('totalBalance', sp.nat(0))
        numTokens = sp.len(balances)
        with sp.for_('x', sp.range(0, sp.len(balances))) as x:
            totalBalance.value += balances[x]
        # with sp.if_(totalBalance.value == sp.nat(0)):
        #     sp.result(sp.nat(0))
        prevInvariant = sp.local('priceInvariant', sp.nat(0))
        invariant = sp.local('invariant', totalBalance.value)
        ampTimesTotal = amp * numTokens

        loop_flag = sp.local('loop_flag', True)
        i = sp.local('i', 0)
        result_value = sp.local('result_value', sp.nat(0))

        with sp.while_(loop_flag.value):
            P_D = sp.local('P_D', numTokens * balances[0])
            with sp.for_('j', sp.range(1, sp.len(balances))) as j:
                P_D.value = (
                    P_D.value * balances[j] * numTokens) // invariant.value
            prevInvariant.value = invariant.value
            invariant.value = (numTokens * invariant.value * invariant.value +
                               (ampTimesTotal * totalBalance.value * P_D.value) // AMP_PRECISION) // ((numTokens + 1) * invariant.value +
                                                                                                      sp.as_nat(ampTimesTotal - AMP_PRECISION) *
                                                                                                      P_D.value // AMP_PRECISION)

            with sp.if_(invariant.value > prevInvariant.value):
                with sp.if_(sp.as_nat(invariant.value - prevInvariant.value) <= sp.nat(1)):
                    result_value.value = invariant.value
                    loop_flag.value = False
            with sp.else_():
                with sp.if_(sp.as_nat(prevInvariant.value - invariant.value) <= sp.nat(1)):
                    result_value.value = invariant.value
                    loop_flag.value = False

            i.value += 1
            with sp.if_(i.value >= 255):
                loop_flag.value = False

        with sp.if_(result_value.value == sp.nat(0)):
            sp.failwith(Errors.STABLE_GET_BALANCE_DIDNT_CONVERGE)
        sp.result(result_value.value)

    def calcOutGivenIn(amp, balances, tokenIndexIn, tokenIndexOut, tokenAmountIn, invariant):
        temp_balances = sp.local('temp_balances', balances)
        temp_balances.value[tokenIndexIn] = temp_balances.value[tokenIndexIn] + tokenAmountIn

        finalBalanceOut = StableMath.getTokenBalanceGivenInvariantAndAllOtherBalances(
            amp, temp_balances.value, invariant, tokenIndexOut)

        result = sp.as_nat(
            temp_balances.value[tokenIndexOut] - finalBalanceOut)
        return result

    def calcInGivenOut(amp, balances, tokenIndexIn, tokenIndexOut, tokenAmountOut, invariant):
        temp_balances = sp.local('temp_balances', balances)
        temp_balances.value[tokenIndexOut] = sp.as_nat(
            temp_balances.value[tokenIndexOut] - tokenAmountOut)

        finalBalanceIn = StableMath.getTokenBalanceGivenInvariantAndAllOtherBalances(
            amp, temp_balances.value, invariant, tokenIndexIn)

        result = sp.as_nat(finalBalanceIn - balances[tokenIndexIn]) + sp.nat(1)
        return result

    def calcSptOutGivenExactTokensIn(
            amp,
            balances,
            amountsIn,
            sptTotalSupply,
            currentInvariant,
            swapFeePercentage,
            calcInvariant,
            fpm,
    ):
        sumBalances = sp.local('sumBalances', sp.nat(0))
        with sp.for_('x', sp.range(0, sp.len(balances))) as x:
            sumBalances.value += balances[x]
        balanceRatiosWithFee = sp.compute(
            sp.map({}, tkey=sp.TNat, tvalue=sp.TNat))

        invariantRatioWithFees = sp.local('invariantRatioWithFees', sp.nat(0))
        with sp.for_('i', sp.range(0, sp.len(balances))) as i:
            currentWeight = fpm['divDown']((balances[i], sumBalances.value))
            balanceRatiosWithFee[i] = balances[i] + \
                fpm['divDown']((amountsIn[i], balances[i]))
            invariantRatioWithFees.value = invariantRatioWithFees.value + \
                fpm['mulDown']((balanceRatiosWithFee[i], currentWeight))

        newBalances = sp.compute(sp.map({}, tkey=sp.TNat, tvalue=sp.TNat))
        with sp.for_('i', sp.range(0, sp.len(balances))) as i:
            amountInWithoutFee = sp.local('amountInWithoutFee', sp.nat(0))
            with sp.if_(balanceRatiosWithFee[i] > invariantRatioWithFees.value):
                nonTaxableAmount = fpm['mulDown'](
                    (balances[i], sp.as_nat(invariantRatioWithFees.value - ONE)))

                taxableAmount = sp.eif(
                    (amountsIn[i] - nonTaxableAmount) > 0,
                    sp.as_nat(amountsIn[i] - nonTaxableAmount),
                    0,
                )
                amountInWithoutFee.value = nonTaxableAmount + \
                    (fpm['mulDown']((taxableAmount, sp.as_nat(ONE - swapFeePercentage))))
            with sp.else_():
                amountInWithoutFee.value = amountsIn[i]

            newBalances[i] = balances[i] + amountInWithoutFee.value

        newInvariant = calcInvariant(
            (amp, newBalances))

        invariantRatio = fpm['divDown']((newInvariant, currentInvariant))

        return sp.eif(
            invariantRatio > ONE,
            fpm['mulDown'](
                (sptTotalSupply, (sp.as_nat(invariantRatio - ONE)))),
            sp.nat(0),
        )

    def calcSptInGivenExactTokensOut(
        amp,
        balances,
        amountsOut,
        sptTotalSupply,
        currentInvariant,
        swapFeePercentage,
        calcInvariant,
        fpm,
    ):
        sumBalances = sp.local('sumBalances', sp.nat(0))
        with sp.for_('x', sp.range(0, sp.len(balances))) as x:
            sumBalances.value += balances[x]

        balanceRatiosWithoutFee = sp.compute(
            sp.map({}, tkey=sp.TNat, tvalue=sp.TNat))
        invariantRatioWithoutFees = sp.local(
            'invariantRatioWithoutFees', sp.nat(0))
        with sp.for_('i', sp.range(0, sp.len(balances))) as i:
            currentWeight = fpm['divUp']((balances[i], sumBalances.value))
            balanceRatiosWithoutFee[i] = sp.as_nat(balances[i] -
                                                   fpm['divUp']((amountsOut[i], balances[i])))
            invariantRatioWithoutFees.value = invariantRatioWithoutFees.value + \
                fpm['mulUp']((balanceRatiosWithoutFee[i], currentWeight))

        newBalances = sp.compute(sp.map({}, tkey=sp.TNat, tvalue=sp.TNat))
        with sp.for_('i', sp.range(0, sp.len(balances))) as i:
            amountOutWithFee = sp.local('amountOutWithFee', sp.nat(0))
            with sp.if_(invariantRatioWithoutFees.value > balanceRatiosWithoutFee[i]):
                nonTaxableAmount = fpm['mulDown'](
                    (balances[i], FixedPoint.complement(invariantRatioWithoutFees.value)))
                taxableAmount = sp.eif(
                    (amountsOut[i] - nonTaxableAmount) > 0,
                    sp.as_nat(amountsOut[i] - nonTaxableAmount),
                    0,
                )
                amountOutWithFee.value = nonTaxableAmount + \
                    (fpm['divUp']((taxableAmount, sp.as_nat(ONE - swapFeePercentage))))
            with sp.else_():
                amountOutWithFee.value = amountsOut[i]

            newBalances[i] = sp.as_nat(balances[i] - amountOutWithFee.value)

        newInvariant = calcInvariant(
            (amp, newBalances))
        invariantRatio = fpm['divDown']((newInvariant, currentInvariant))

        return fpm['mulUp'](
            (sptTotalSupply, (FixedPoint.complement(invariantRatio))))

    def calcTokenInGivenExactSptOut(
            amp,
            balances,
            tokenIndex,
            sptAmountOut,
            sptTotalSupply,
            currentInvariant,
            swapFeePercentage,
            fpm,
    ):
        newInvariant = fpm['mulUp']((fpm['divUp'](
            ((sptTotalSupply + sptAmountOut),  sptTotalSupply)), currentInvariant))

        newBalanceTokenIndex = StableMath.getTokenBalanceGivenInvariantAndAllOtherBalances(
            amp, balances, newInvariant, tokenIndex)

        amountInWithoutFee = sp.as_nat(
            newBalanceTokenIndex - balances[tokenIndex])

        sumBalances = sp.local('sumBalances', 0)
        with sp.for_('x', sp.range(0, sp.len(balances))) as x:
            sumBalances.value += balances[x]

        currentWeight = fpm['divDown'](
            (balances[tokenIndex], sumBalances.value))
        taxablePercentage = FixedPoint.complement(currentWeight)
        taxableAmount = fpm['mulUp']((amountInWithoutFee, taxablePercentage))
        nonTaxableAmount = sp.as_nat(amountInWithoutFee - taxableAmount)

        return nonTaxableAmount + (fpm['divUp']((taxableAmount, sp.as_nat(ONE - swapFeePercentage))))

    def calcTokenOutGivenExactSptIn(
            amp,
            balances,
            tokenIndex,
            sptAmountIn,
            sptTotalSupply,
            currentInvariant,
            swapFeePercentage,
            fpm,
    ):
        newInvariant = fpm['mulUp']((fpm['divUp'](
            (sp.as_nat(sptTotalSupply - sptAmountIn),  sptTotalSupply)), currentInvariant))

        newBalanceTokenIndex = StableMath.getTokenBalanceGivenInvariantAndAllOtherBalances(
            amp, balances, newInvariant, tokenIndex)
        amountOutWithoutFee = sp.as_nat(
            balances[tokenIndex] - newBalanceTokenIndex)

        sumBalances = sp.local('sumBalances', 0)
        with sp.for_('x', sp.range(0, sp.len(balances))) as x:
            sumBalances.value += balances[x]

        currentWeight = fpm['divDown'](
            (balances[tokenIndex], sumBalances.value))
        taxablePercentage = FixedPoint.complement(currentWeight)
        taxableAmount = fpm['mulUp']((amountOutWithoutFee, taxablePercentage))
        nonTaxableAmount = sp.as_nat(amountOutWithoutFee - taxableAmount)

        return nonTaxableAmount + (fpm['mulDown']((taxableAmount, sp.as_nat(ONE - swapFeePercentage))))

    def getTokenBalanceGivenInvariantAndAllOtherBalances(amp, balances, invariant, tokenIndex):
        ampTimesTotal = amp * sp.len(balances)
        bal_sum = sp.local('bal_sum', 0)
        with sp.for_('balance', sp.range(0, sp.len(balances))) as balance:
            bal_sum.value += balances[balance]

        bal_sum.value = sp.as_nat(bal_sum.value - balances[tokenIndex])

        P_D = sp.local('P_D', sp.len(balances) * balances[0])
        with sp.for_('i', sp.range(1, sp.len(balances))) as i:
            P_D.value = (P_D.value * balances[i]
                         * sp.len(balances)) // invariant

        c = (invariant * invariant *
             balances[tokenIndex]) // (ampTimesTotal * P_D.value // AMP_PRECISION)
        b = bal_sum.value + invariant // ampTimesTotal

        prevTokenbalance = sp.local('prevTokenbalance', 0)
        tokenBalance = sp.local('tokenBalance',
                                (invariant * invariant + c) // (invariant + b))
        iteration = sp.local('iteration', 0)
        diff = sp.local('diff', 0)
        with sp.while_(iteration.value < 255):
            prevTokenbalance.value = tokenBalance.value
            tokenBalance.value = ((tokenBalance.value * tokenBalance.value) +
                                  c) // sp.as_nat(((tokenBalance.value * 2) + b) - invariant)

            with sp.if_(tokenBalance.value > prevTokenbalance.value):
                diff.value = sp.as_nat(
                    tokenBalance.value - prevTokenbalance.value)
            with sp.else_():
                diff.value = sp.as_nat(
                    prevTokenbalance.value - tokenBalance.value)
            with sp.if_(diff.value <= 1):
                iteration.value = 255
            with sp.else_():
                iteration.value += 1

        with sp.if_(diff.value > sp.nat(1)):
            sp.failwith(Errors.STABLE_GET_BALANCE_DIDNT_CONVERGE)

        return tokenBalance.value
