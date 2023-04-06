import smartpy as sp

MIN_AMP = 1
MAX_AMP = 5000
AMP_PRECISION = 1000

MAX_STABLE_TOKENS = 5


class StableMath:
    def calculateInvariant(t):
        amplificationParameter, balances, roundUp = sp.match_tuple(
            t, 'amplificationParameter', 'balances', 'roundUp')
        totalBalance = sp.local('totalBalance', sp.nat(0))
        numTokens = sp.len(balances)
        with sp.for_('x', sp.range(0, sp.len(balances))) as x:
            totalBalance.value += balances[x]
        # with sp.if_(totalBalance.value == sp.nat(0)):
        #     sp.result(sp.nat(0))
        prevInvariant = sp.local('priceInvariant', sp.nat(0))
        invariant = sp.local('invariant', totalBalance.value)
        ampTimesTotal = amplificationParameter * numTokens

        loop_flag = sp.local('loop_flag', True)
        i = sp.local('i', 0)
        result_value = sp.local('result_value', sp.nat(0))

        with sp.while_(loop_flag.value):
            P_D = sp.local('P_D', numTokens * balances[0])
            with sp.for_('j', sp.range(1, sp.len(balances))) as j:
                P_D.value = sp.eif(roundUp, (P_D.value * balances[j] * numTokens) // invariant.value,
                                   (P_D.value * balances[j] * numTokens) // invariant.value + 1)
            prevInvariant.value = invariant.value
            invariant.value = sp.eif(
                roundUp,
                (numTokens * invariant.value * invariant.value +
                 (ampTimesTotal * totalBalance.value * P_D.value) // AMP_PRECISION),
                (numTokens * invariant.value * invariant.value + sp.as_nat((ampTimesTotal *
                                                                            totalBalance.value * P_D.value) + AMP_PRECISION - 1) // AMP_PRECISION)
            ) // sp.eif(
                roundUp == False,
                (numTokens + 1) * invariant.value +
                sp.as_nat(ampTimesTotal - AMP_PRECISION) *
                P_D.value // AMP_PRECISION,
                ((numTokens + 1) * invariant.value + sp.as_nat(sp.as_nat(ampTimesTotal -
                                                                         AMP_PRECISION) * P_D.value + AMP_PRECISION - 1) // AMP_PRECISION)
            )

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
            sp.failwith("STABLE_GET_BALANCE_DIDNT_CONVERGE")
        sp.result(result_value.value)

    # def calcOutGivenIn(params):
    #     amplificationParameter, balances, tokenIndexIn, tokenIndexOut, tokenAmountIn, invariant = sp.match_tuple(
    #         params, "amplificationParameter", "balances", "tokenIndexIn", "tokenIndexOut", "tokenAmountIn", "invariant")

    #     balances[tokenIndexIn] = balances[tokenIndexIn] + tokenAmountIn

    #     finalBalanceOut = StableMath.getTokenBalanceGivenInvariantAndAllOtherBalances(
    #         amplificationParameter, balances, invariant, tokenIndexOut)

    #     balances[tokenIndexIn] = balances[tokenIndexIn] - tokenAmountIn

    #     result = balances[tokenIndexOut] - finalBalanceOut
    #     sp.result(result)

    # def calcInGivenOut(params):
    #     amplificationParameter, balances, tokenIndexIn, tokenIndexOut, tokenAmountOut, invariant = sp.match_tuple(
    #         params, "amplificationParameter", "balances", "tokenIndexIn", "tokenIndexOut", "tokenAmountOut", "invariant")

    #     balances[tokenIndexOut] = balances[tokenIndexOut] - tokenAmountOut

    #     finalBalanceIn = StableMath.getTokenBalanceGivenInvariantAndAllOtherBalances(
    #         amplificationParameter, balances, invariant, tokenIndexIn)

    #     balances[tokenIndexOut] = balances[tokenIndexOut] + tokenAmountOut
    #     result = finalBalanceIn - \
    #         balances[tokenIndexIn] + sp.nat(1) // (10 ** 18)
    #     sp.result(result)

    # def calcBptOutGivenExactTokensIn(self, amplificationParameter, balances, amountsIn, bptTotalSupply, swapFee, swapFeePercentage):
    #     currentInvariant = self._calculateInvariant(
    #         amplificationParameter, balances, True)

    #     sumBalances = sp.local(sp.nat(0))
    #     with sp.for_('balance', balances) as balance:
    #         sumBalances.value += balance

    #     tokenBalanceRatiosWithoutFee = []
    #     weightedBalanceRatio = sp.local(sp.nat(0))
    #     with sp.for_('i', sp.range(sp.len(balances))) as i:
    #         currentWeight = balances[i] // sumBalances.value
    #         tokenBalanceRatiosWithoutFee.append(sp.eif(
    #             amountsIn[i] % balances[i] == 0, balances[i] + amountsIn[i] // balances[i], balances[i] + (amountsIn[i] // balances[i]) + 1))
    #         weightedBalanceRatio.value += tokenBalanceRatiosWithoutFee[i] * currentWeight

    #     tokenBalancePercentageExcess = sp.local(sp.nat(0))
    #     newBalances = []
    #     with sp.for_('i', sp.range(sp.len(balances))) as i:
    #         tokenBalancePercentageExcess.value = sp.eif(weightedBalanceRatio.value >= tokenBalanceRatiosWithoutFee[i], 0, sp.eif(tokenBalanceRatiosWithoutFee[i] % weightedBalanceRatio.value == 0, tokenBalanceRatiosWithoutFee[
    #                                                     i] - weightedBalanceRatio.value // tokenBalanceRatiosWithoutFee[i], tokenBalanceRatiosWithoutFee[i] - (weightedBalanceRatio.value // tokenBalanceRatiosWithoutFee[i]) + 1))

    #         swapFeeExcess = swapFeePercentage * tokenBalancePercentageExcess.value
    #         amountInAfterFee = amountsIn[i] * (1 - swapFeeExcess)
    #         newBalances.append(balances[i] + amountInAfterFee)

    #     newInvariant = self._calculateInvariant(
    #         amplificationParameter, newBalances, True)
    #     sp.result(bptTotalSupply * (sp.eif(newInvariant % currentInvariant == 0,
    #               newInvariant // currentInvariant, (newInvariant // currentInvariant) + 1)))

    # def calcTokenInGivenExactBptOut(self, amplificationParameter, balances, tokenIndex, bptAmountOut, bptTotalSupply, swapFeePercentage):
    #     currentInvariant = self.calculateInvariant(
    #         amplificationParameter, balances, True)

    #     newInvariant = ((bptTotalSupply + bptAmountOut) * bptTotalSupply *
    #                     currentInvariant + currentInvariant - 1) // currentInvariant

    #     sumBalances = sp.local(sp.nat, 0)
    #     with sp.for_('balance', sp.range(sp.len(balances))) as balance:
    #         sumBalances.value += balances[balance]

    #     newBalanceTokenIndex = self.getTokenBalanceGivenInvariantAndAllOtherBalances(
    #         amplificationParameter, balances, newInvariant, tokenIndex)
    #     amountInAfterFee = newBalanceTokenIndex - balances[tokenIndex]

    #     currentWeight = balances[tokenIndex] // sumBalances.value
    #     tokenBalancePercentageExcess = 1 - currentWeight
    #     swapFeeExcess = swapFeePercentage * tokenBalancePercentageExcess

    #     sp.result((amountInAfterFee * 1) // (1 - (1 - swapFeeExcess)))

    # def calcBptInGivenExactTokensOut(
    #     self,
    #     amplificationParameter,
    #     balances,
    #     amountsOut,
    #     bptTotalSupply,
    #     swapFee
    # ):
    #     currentInvariants = self._calculateInvariant(
    #         amplificationParameter, balances, True)
    #     sumBalances = sp.local(sp.nat(0))
    #     with sp.for_('balance', balances) as balance:
    #         sumBalances.value += balance

    #     tokenBalanceRatiosWithoutFee = [None] * sp.len(balances)
    #     weightedBalanceRatio = sp.local(sp.nat(0))

    #     with sp.for_('i', sp.range(sp.len(balances))) as i:
    #         currentWeight = sp.eif(balances[i] % sumBalances.value == 0, balances[i] //
    #                                sumBalances.value, (balances[i] // sumBalances.value) + 1)
    #         tokenBalanceRatiosWithoutFee[i] = sp.eif(
    #             amountsOut[i] % balances[i] == 0, balances[i] - amountsOut[i] // balances[i], balances[i] - (amountsOut[i] // balances[i]) + 1)
    #         weightedBalanceRatio.value += tokenBalanceRatiosWithoutFee[i] * currentWeight

    #     newBalances = []
    #     with sp.for_('i', sp.range(sp.len(balances))) as i:
    #         tokenBalancePercentageExcess = sp.eif(weightedBalanceRatio.value <= tokenBalanceRatiosWithoutFee[i], 0, sp.eif(tokenBalanceRatiosWithoutFee[i] % (
    #             1 - tokenBalanceRatiosWithoutFee[i]) == 0, weightedBalanceRatio.value - tokenBalanceRatiosWithoutFee[i] // (1 - tokenBalanceRatiosWithoutFee[i]), (weightedBalanceRatio.value - tokenBalanceRatiosWithoutFee[i]) // (1 - tokenBalanceRatiosWithoutFee[i]) + 1))

    #         swapFeeExcess = swapFee * tokenBalancePercentageExcess
    #         amountOutBeforeFee = sp.eif(amountsOut[i] % (1 - swapFeeExcess) == 0, amountsOut[i] // (
    #             1 - swapFeeExcess), (amountsOut[i] // (1 - swapFeeExcess)) + 1)
    #         newBalances.append(balances[i] - amountOutBeforeFee)

    #     newInvariant = self._calculateInvariant(
    #         amplificationParameter, newBalances, True)
    #     sp.result(bptTotalSupply * (newInvariant // (1 - currentInvariants) if newInvariant %
    #               (1 - currentInvariants) == 0 else (newInvariant // (1 - currentInvariants)) + 1))

    # def calcTokenOutGivenExactBptIn(self, amplificationParameter, balances, tokenIndex, bptAmountIn, bptTotalSupply, swapFeePercentage):
    #     currentInvariant = self.calculateInvariant(
    #         amplificationParameter, balances, True)
    #     newInvariant = bptTotalSupply - \
    #         ((bptAmountIn * bptTotalSupply * currentInvariant +
    #          currentInvariant - 1) // currentInvariant)

    #     sumBalances = sp.local(sp.nat, 0)
    #     with sp.for_('balance', sp.range(sp.len(balances))) as balance:
    #         sumBalances.value += balances[balance]

    #     newBalanceTokenIndex = self.getTokenBalanceGivenInvariantAndAllOtherBalances(
    #         amplificationParameter, balances, newInvariant, tokenIndex)
    #     amountOutBeforeFee = balances[tokenIndex] - newBalanceTokenIndex

    #     currentWeight = balances[tokenIndex] // sumBalances.value
    #     tokenbalancePercentageExcess = 1 - currentWeight

    #     swapFeeExcess = swapFeePercentage * tokenbalancePercentageExcess

    #     sp.result(amountOutBeforeFee * (1 - swapFeeExcess))

    # def calcDueTokenProtocolSwapFeeAmount(self, amplificationParameter, balances, lastInvariant, tokenIndex, protocolSwapFeePercentage):
    #     finalBalanceFeeToken = self.getTokenBalanceGivenInvariantAndAllOtherBalances(
    #         amplificationParameter, balances, lastInvariant, tokenIndex)

    #     accumulatedTokenSwapFees = sp.eif(
    #         balances[tokenIndex] > finalBalanceFeeToken, balances[tokenIndex] - finalBalanceFeeToken, 0)

    #     sp.result((accumulatedTokenSwapFees * protocolSwapFeePercentage) // 1)

    # def calcTokensOutGivenExactBptIn(self, balances, bptAmountIn, bptTotalSupply):
    #     bptRatio = bptAmountIn // bptTotalSupply
    #     amountsOut = sp.map(lambda balance: balance * bptRatio, balances)
    #     sp.result(amountsOut)

    # def getTokenBalanceGivenInvariantAndAllOtherBalances(self, amplificationParameter, balances, invariant, tokenIndex):
    #     ampTimesTotal = amplificationParameter * sp.len(balances)
    #     bal_sum = sp.local(sp.nat, 0)
    #     with sp.for_('balance', sp.range(sp.len(balances))) as balance:
    #         bal_sum.value += balances[balance]

    #     bal_sum.value -= balances[tokenIndex]

    #     P_D = sp.local(sp.nat, sp.len(balances) * balances[0])
    #     with sp.for_('i', sp.range(1, sp.len(balances))) as i:
    #         P_D.value = (P_D.value * balances[i]
    #                      * sp.len(balances)) // invariant

    #     c = (invariant * invariant *
    #          balances[tokenIndex]) // (ampTimesTotal * P_D.value)
    #     b = bal_sum.value + invariant // ampTimesTotal

    #     prevTokenbalance = sp.local(sp.nat, 0)
    #     tokenBalance = sp.local(
    #         sp.nat, (invariant * invariant + c) // (invariant + b))
    #     iteration = sp.local(sp.nat, 0)
    #     with sp.while_(iteration.value < 255):
    #         prevTokenbalance.value = tokenBalance.value
    #         tokenBalance.value = ((tokenBalance.value * tokenBalance.value) +
    #                               c) // ((tokenBalance.value * 2) + b - invariant)
    #         diff = sp.local(sp.nat, 0)
    #         with sp.if_(tokenBalance.value > prevTokenbalance.value):
    #             diff.value = tokenBalance.value - prevTokenbalance.value
    #         with sp.else_():
    #             diff.value = prevTokenbalance.value - tokenBalance.value
    #         with sp.if_(diff.value <= 1):
    #             iteration.value = 255
    #         with sp.else_():
    #             iteration.value += 1

    #     sp.result(tokenBalance.value)
