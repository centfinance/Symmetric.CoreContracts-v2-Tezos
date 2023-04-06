import smartpy as sp

MIN_AMP = 1
MAX_AMP = 5000
AMP_PRECISION = 1000

MAX_STABLE_TOKENS = 5


class StableMath(sp.Contract):

    def calculateInvariant(self, amplificationParameter, balances, roundUp):
        sum = sp.tez(0)
        numTokens = len(balances)
        for balance in balances:
            sum += balance
        if sum == sp.tez(0):
            sp.result(sp.tez(0))
        prevInvariant = sp.tez(0)
        invariant = sum
        ampTimesTotal = amplificationParameter * numTokens

        for _ in range(255):
            P_D = numTokens * balances[0]
            for j in range(1, len(balances)):
                P_D = (P_D * balances[j] * numTokens) // invariant if roundUp else (
                    P_D * balances[j] * numTokens) // invariant + 1
            prevInvariant = invariant
            invariant = (
                (numTokens * invariant * invariant + (ampTimesTotal * sum * P_D) // AMP_PRECISION) if roundUp
                else (numTokens * invariant * invariant + ((ampTimesTotal * sum * P_D) + AMP_PRECISION - 1) // AMP_PRECISION)
            ) // (
                (numTokens + 1) * invariant + (ampTimesTotal - AMP_PRECISION) * P_D // AMP_PRECISION if not roundUp
                else ((numTokens + 1) * invariant + ((ampTimesTotal - AMP_PRECISION) * P_D + AMP_PRECISION - 1) // AMP_PRECISION)
            )

            if invariant > prevInvariant:
                if invariant - prevInvariant <= sp.tez(1):
                    sp.result(invariant)
            elif prevInvariant - invariant <= sp.tez(1):
                sp.result(invariant)

        sp.failwith("STABLE_GET_BALANCE_DIDNT_CONVERGE")

    def calcBptInGivenExactTokensOut(
        self,
        amplificationParameter,
        balances,
        amountsOut,
        bptTotalSupply,
        swapFee
    ):
        currentInvariants = self.calculateInvariant(
            amplificationParameter, balances, True)
        sumBalances = sp.tez(0)
        for balance in balances:
            sumBalances += balance

        tokenBalanceRatiosWithoutFee = [None] * len(balances)
        weightedBalanceRatio = sp.tez(0)

        for i in range(len(balances)):
            currentWeight = balances[i] // sumBalances if balances[i] % sumBalances == 0 else (
                balances[i] // sumBalances) + 1
            tokenBalanceRatiosWithoutFee[i] = balances[i] - \
                amountsOut[i] // balances[i] if amountsOut[i] % balances[i] == 0 else (
                    amountsOut[i] // balances[i]) + 1
            weightedBalanceRatio += tokenBalanceRatiosWithoutFee[i] * \
                currentWeight

        newBalances = []
        for i in range(len(balances)):
            tokenBalancePercentageExcess = 0
            if weightedBalanceRatio <= tokenBalanceRatiosWithoutFee[i]:
                tokenBalancePercentageExcess = 0
            else:
                tokenBalancePercentageExcess = weightedBalanceRatio - tokenBalanceRatiosWithoutFee[i] // (1 - tokenBalanceRatiosWithoutFee[i]) if tokenBalanceRatiosWithoutFee[i] % (
                    1 - tokenBalanceRatiosWithoutFee[i]) == 0 else (tokenBalanceRatiosWithoutFee[i] // (1 - tokenBalanceRatiosWithoutFee[i])) + 1

            swapFeeExcess = swapFee * tokenBalancePercentageExcess
            amountOutBeforeFee = amountsOut[i] // (1 - swapFeeExcess) if amountsOut[i] % (
                1 - swapFeeExcess) == 0 else (amountsOut[i] // (1 - swapFeeExcess)) + 1
            newBalances.append(balances[i] - amountOutBeforeFee)

        newInvariant = self._calculateInvariant(
            amplificationParameter, newBalances, True)
        sp.result(bptTotalSupply * (newInvariant // (1 - currentInvariants) if newInvariant %
                  (1 - currentInvariants) == 0 else (newInvariant // (1 - currentInvariants)) + 1))

    def calcBptOutGivenExactTokensIn(self, amplificationParameter, balances, amountsIn, bptTotalSupply, swapFee, swapFeePercentage):
        currentInvariant = self.calculateInvariant(
            amplificationParameter, balances, True)

        sumBalances = sp.tez(0)
        for balance in balances:
            sumBalances += balance

        tokenBalanceRatiosWithoutFee = []
        weightedBalanceRatio = sp.tez(0)
        for i in range(len(balances)):
            currentWeight = balances[i] // sumBalances
            tokenBalanceRatiosWithoutFee.append(
                balances[i] + amountsIn[i] // balances[i] if amountsIn[i] % balances[i] == 0 else (amountsIn[i] // balances[i]) + 1)
            weightedBalanceRatio += tokenBalanceRatiosWithoutFee[i] * \
                currentWeight

        tokenBalancePercentageExcess = sp.tez(0)
        newBalances = []
        for i in range(len(balances)):
            if weightedBalanceRatio >= tokenBalanceRatiosWithoutFee[i]:
                tokenBalancePercentageExcess = sp.tez(0)
            else:
                tokenBalancePercentageExcess = tokenBalanceRatiosWithoutFee[i] - weightedBalanceRatio // tokenBalanceRatiosWithoutFee[
                    i] if tokenBalanceRatiosWithoutFee[i] % weightedBalanceRatio == 0 else (weightedBalanceRatio // tokenBalanceRatiosWithoutFee[i]) + 1

            swapFeeExcess = swapFeePercentage * tokenBalancePercentageExcess
            amountInAfterFee = amountsIn[i] * (1 - swapFeeExcess)
            newBalances.append(balances[i] + amountInAfterFee)

        newInvariant = self._calculateInvariant(
            amplificationParameter, newBalances, True)
        sp.result(bptTotalSupply * (newInvariant // currentInvariant if newInvariant % currentInvariant ==
                  0 else (newInvariant // currentInvariant) + 1))  # TODO: Omitted subtracting ONE from current_invariant

    def calcDueTokenProtocolSwapFeeAmount(self, amplificationParameter, balances, lastInvariant, tokenIndex, protocolSwapFeePercentage):
        finalBalanceFeeToken = self.getTokenBalanceGivenInvariantAndAllOtherBalances(
            amplificationParameter, balances, lastInvariant, tokenIndex)

        if balances[tokenIndex] > finalBalanceFeeToken:
            accumulatedTokenSwapFees = balances[tokenIndex] - \
                finalBalanceFeeToken
        else:
            accumulatedTokenSwapFees = sp.tez(0)

        sp.result((accumulatedTokenSwapFees * protocolSwapFeePercentage) // 1)

    def calcInGivenOut(self, amplificationParameter, balances, tokenIndexIn, tokenIndexOut, tokenAmountOut):
        invariant = self.calculateInvariant(
            amplificationParameter, balances, True)
        balances[tokenIndexOut] = balances[tokenIndexOut] - tokenAmountOut

        finalBalanceIn = self.getTokenBalanceGivenInvariantAndAllOtherBalances(
            amplificationParameter, balances, invariant, tokenIndexIn)

        balances[tokenIndexOut] = balances[tokenIndexOut] + tokenAmountOut
        result = finalBalanceIn - \
            balances[tokenIndexIn] + sp.tez(1) // (10 ** 18)
        sp.result(result)

    def calcOutGivenIn(self, amplificationParameter, balances, tokenIndexIn, tokenIndexOut, tokenAmountIn):
        invariant = self.calculateInvariant(
            amplificationParameter, balances, True)
        balances[tokenIndexIn] = balances[tokenIndexIn] + tokenAmountIn

        finalBalanceOut = self.getTokenBalanceGivenInvariantAndAllOtherBalances(
            amplificationParameter, balances, invariant, tokenIndexOut)

        balances[tokenIndexIn] = balances[tokenIndexIn] - tokenAmountIn

        result = balances[tokenIndexOut] - finalBalanceOut
        sp.result(result)

    def calcTokenInGivenExactBptOut(self, amplificationParameter, balances, tokenIndex, bptAmountOut, bptTotalSupply, swapFeePercentage):
        currentInvariant = self.calculateInvariant(
            amplificationParameter, balances, True)

        newInvariant = ((bptTotalSupply + bptAmountOut) * bptTotalSupply *
                        currentInvariant + currentInvariant - 1) // currentInvariant

        sumBalances = sp.tez(0)
        for balance in balances:
            sumBalances += balance

        newBalanceTokenIndex = self.getTokenBalanceGivenInvariantAndAllOtherBalances(
            amplificationParameter, balances, newInvariant, tokenIndex)
        amountInAfterFee = newBalanceTokenIndex - balances[tokenIndex]

        currentWeight = balances[tokenIndex] // sumBalances
        tokenBalancePercentageExcess = 1 - currentWeight
        swapFeeExcess = swapFeePercentage * tokenBalancePercentageExcess

        sp.result((amountInAfterFee * 1) // (1 - (1 - swapFeeExcess)))

    def calcTokensOutGivenExactBptIn(self, balances, bptAmountIn, bptTotalSupply):
        bptRatio = bptAmountIn // bptTotalSupply
        amountsOut = sp.map(lambda balance: balance * bptRatio, balances)
        sp.result(amountsOut)

    def calcTokenOutGivenExactBptIn(self, amplificationParameter, balances, tokenIndex, bptAmountIn, bptTotalSupply, swapFeePercentage):
        currentInvariant = self.calculateInvariant(
            amplificationParameter, balances, True)
        newInvariant = bptTotalSupply - \
            ((bptAmountIn * bptTotalSupply * currentInvariant +
             currentInvariant - 1) // currentInvariant)

        sumBalances = sp.tez(0)
        for balance in balances:
            sumBalances += balance

        newBalanceTokenIndex = self.getTokenBalanceGivenInvariantAndAllOtherBalances(
            amplificationParameter, balances, newInvariant, tokenIndex)
        amountOutBeforeFee = balances[tokenIndex] - newBalanceTokenIndex

        currentWeight = balances[tokenIndex] // sumBalances
        tokenbalancePercentageExcess = 1 - currentWeight

        swapFeeExcess = swapFeePercentage * tokenbalancePercentageExcess

        sp.result(amountOutBeforeFee * (1 - swapFeeExcess))

    def getTokenBalanceGivenInvariantAndAllOtherBalances(self, amplificationParameter, balances, invariant, tokenIndex):
        ampTimesTotal = amplificationParameter * len(balances)
        bal_sum = sp.tez(0)
        for balance in balances:
            bal_sum += balance

        bal_sum -= balances[tokenIndex]

        P_D = len(balances) * balances[0]
        for i in range(1, len(balances)):
            P_D = (P_D * balances[i] * len(balances)) // invariant

        c = (invariant * invariant *
             balances[tokenIndex]) // (ampTimesTotal * P_D)
        b = bal_sum + invariant // ampTimesTotal

        prevTokenbalance = sp.tez(0)
        tokenBalance = (invariant * invariant + c) // (invariant + b)
        for _ in range(255):
            prevTokenbalance = tokenBalance
            tokenBalance = ((tokenBalance * tokenBalance) +
                            c) // ((tokenBalance * 2) + b - invariant)
            if tokenBalance > prevTokenbalance:
                if tokenBalance - prevTokenbalance <= sp.tez(1) / (10 ** 18):
                    break
            elif prevTokenbalance - tokenBalance <= sp.tez(1) / (10 ** 18):
                break

        sp.result(tokenBalance)
