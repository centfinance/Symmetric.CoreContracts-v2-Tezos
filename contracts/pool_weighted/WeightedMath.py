import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

import contracts.utils.math.FixedPoint as FixedPoint


class WeightedMath:
    _MIN_WEIGHT = 10000000000000000  # 0.01e18

    _MAX_WEIGHTED_TOKENS = 100

    # Swap limits: amounts swapped may not be larger than this percentage of total balance.
    _MAX_IN_RATIO = 300000000000000000  # 0.3e18

    _MAX_OUT_RATIO = 300000000000000000  # 0.3e18

    # Invariant growth limit: non-proportional joins cannot cause the invariant to increase by more than this ratio.
    _MAX_INVARIANT_RATIO = 3000000000000000000  # 3e18
    # Invariant shrink limit: non-proportional exits cannot cause the invariant to decrease by less than this ratio.
    _MIN_INVARIANT_RATIO = 700000000000000000  # 0.7e18

    def complement(x):
        return sp.as_nat(FixedPoint.ONE - x)

    def _calculateInvariant(normalizedWeights, balances, math):
        """Calculates the invariant of normalized weights and balances

        Args:
            normalizedWeights (map):  The normalized weights
            balances (map): A map of balances

        Returns:
            Fixed Point: The calculated invariant value

        """
        # Set the type of the variables
        sp.set_type(normalizedWeights, sp.TMap(sp.TNat, sp.TNat))
        sp.set_type(balances, sp.TMap(sp.TNat, sp.TNat))

        # Create an initial invariant

        invariant = sp.local('invariant', FixedPoint.ONE)
        # invariant = sp.local('invariant', 1)

        # Iterate through each index in the normalized weights
        with sp.for_('i', sp.range(0, sp.len(normalizedWeights))) as i:
            # Calculate the power of down from the balance and normalized weight
            power = math['powDown']((balances[i], normalizedWeights[i]))
            # Multiply the previous invariant to give a new invariant
            invariant.value = math['mulDown']((
                invariant.value, power))

            # invariant.value *= power

        # Verify that the new invariant is larger 0
        sp.verify(invariant.value > 0)
        # Return the new invariant
        return invariant.value

    def _calcOutGivenIn(
        balanceIn,
        weightIn,
        balanceOut,
        weightOut,
        amountIn,
        math
    ):
        sp.verify(amountIn <= math['mulDown']((balanceIn,
                                               WeightedMath._MAX_IN_RATIO)), Errors.MAX_IN_RATIO)

        denominator = balanceIn + amountIn
        base = math['divUp']((balanceIn, denominator))
        exponent = math['divDown']((weightIn, weightOut))
        power = math['powUp']((base, exponent))
        return math['mulDown']((balanceOut, WeightedMath.complement(power)))

    def _calcInGivenOut(
        balanceIn,
        weightIn,
        balanceOut,
        weightOut,
        amountOut,
        math,
    ):
        sp.verify(amountOut <= math['mulDown']((balanceOut,
                                                WeightedMath._MAX_IN_RATIO)), Errors.MAX_IN_RATIO)

        base = math['divUp']((
            (balanceOut, sp.as_nat(balanceOut - amountOut))))
        exponent = math['divUp']((weightOut, weightIn))
        power = math['powUp']((base, exponent))

        ratio = sp.as_nat(power - FixedPoint.ONE)

        return math['mulUp']((balanceIn, ratio))

    def _calcSptOutGivenExactTokensIn(
            balances,
            normalizedWeights,
            amountsIn,
            totalSupply,
            swapFeePercentage,
            math,
    ):
        # SPT out, so we round down overall.

        balanceRatiosWithFee = sp.local(
            'balanceRatiosWithFee', sp.map(l={}, tkey=sp.TNat, tvalue=sp.TNat))

        invariantRatioWithFees = sp.local('invariantRatioWithFees', 0)

        with sp.for_('i', sp.range(0, sp.len(balances))) as i:
            balanceRatiosWithFee.value[i] = math['divDown']((
                (balances[i] + amountsIn[i]), balances[i]))
            invariantRatioWithFees.value = invariantRatioWithFees.value + \
                math['mulDown'](
                    (balanceRatiosWithFee.value[i], normalizedWeights[i]))

        invariantRatio = WeightedMath._computeJoinExactTokensInInvariantRatio(
            balances,
            normalizedWeights,
            amountsIn,
            balanceRatiosWithFee.value,
            invariantRatioWithFees.value,
            swapFeePercentage,
            math
        )

        sptOut = sp.local('sptOut', 0)
        with sp.if_(invariantRatio > FixedPoint.ONE):
            sptOut.value = math['mulDown']((
                totalSupply, sp.as_nat(invariantRatio - FixedPoint.ONE)))

        return sptOut.value

    def _calcTokenInGivenExactSptOut(
        balance,
        normalizedWeight,
        sptAmountOut,
        sptTotalSupply,
        swapFeePercentage,
        math,
    ):
        # ******************************************************************************************
        #  tokenInForExactSPTOut
        #  a = amountIn
        #  b = balance                      /  /    totalSPT + sptOut      \    (1 / w)       \
        #  bptOut = bptAmountOut   a = b * |  | --------------------------  | ^          - 1  |
        #  bpt = totalSPT                   \  \       totalSPT            /                  /
        #  w = weight
        # ******************************************************************************************
        def complement(x):
            return sp.as_nat(FixedPoint.ONE - x)

        #  Token in, so we round up overall.

        #  Calculate the factor by which the invariant will increase after minting SPTAmountOut

        invariantRatio = math['divUp']((
            (sptTotalSupply + sptAmountOut), sptTotalSupply))

        sp.verify(invariantRatio <= WeightedMath._MAX_INVARIANT_RATIO,
                  Errors.MAX_OUT_SPT_FOR_TOKEN_IN)

        #  Calculate by how much the token balance has to increase to match the invariantRatio
        balanceRatio = math['powUp']((invariantRatio,
                                      math['divUp']((FixedPoint.ONE, normalizedWeight))))

        amountInWithoutFee = math['mulUp']((
            balance, sp.as_nat(balanceRatio - FixedPoint.ONE)))

        #  We can now compute how much extra balance is being deposited and used in virtual swaps, and charge swap fees
        #  accordingly.
        taxableAmount = math['mulUp']((
            amountInWithoutFee, complement(normalizedWeight)))

        nonTaxableAmount = sp.as_nat(amountInWithoutFee - taxableAmount)

        taxableAmountPlusFees = math['divUp']((
            taxableAmount, complement(swapFeePercentage)))

        return (nonTaxableAmount + taxableAmountPlusFees)

    def _computeJoinExactTokensInInvariantRatio(
        balances,
        normalizedWeights,
        amountsIn,
        balanceRatiosWithFee,
        invariantRatioWithFees,
        swapFeePercentage,
        math,
    ):
        ir = sp.local('ir', FixedPoint.ONE)
        # ir = sp.local('ir', 1)

        with sp.for_('i', sp.range(0, sp.len(balances))) as i:
            amountInWithoutFee = sp.local('amountInWithoutFee', 0)

            with sp.if_(balanceRatiosWithFee[i] > invariantRatioWithFees):

                nta = sp.local('nta', 0)
                with sp.if_(invariantRatioWithFees > FixedPoint.ONE):
                    nta.value = math['mulDown']((
                        balances[i], sp.as_nat(invariantRatioWithFees - FixedPoint.ONE)))
                swapFee = math['mulUp']((
                    sp.as_nat(amountsIn[i] - nta.value), swapFeePercentage))
                amountInWithoutFee.value = sp.as_nat(
                    amountsIn[i] - swapFee)
            with sp.else_():
                amountInWithoutFee.value = amountsIn[i]

            balanceRatio = math['divDown']((
                (balances[i] + amountInWithoutFee.value), balances[i]))

            ir.value = math['mulDown']((ir.value, math['powDown']((
            balanceRatio, normalizedWeights[i]))))
            # ir.value *= math['powDown']((
            #     balanceRatio, normalizedWeights[i]))

        return ir.value

    def _calcSptInGivenExactTokensOut(
        balances,
        normalizedWeights,
        amountsOut,
        totalSupply,
        swapFeePercentage,
        math,
    ):
        def complement(x):
            return sp.as_nat(FixedPoint.ONE - x)
        # SPT in, so we round up overall.

        balanceRatiosWithoutFee = sp.local(
            'balanceRatiosWithoutFee', sp.map(l={}, tkey=sp.TNat, tvalue=sp.TNat))

        invariantRatioWithoutFees = sp.local('invariantRatioWithoutFees', 0)
        with sp.for_('i', sp.range(0, sp.len(balances))) as i:
            balanceRatiosWithoutFee.value[i] = math['divUp']((
                sp.as_nat(balances[i] - amountsOut[i]), balances[i]))
            invariantRatioWithoutFees.value = invariantRatioWithoutFees.value + \
                math['mulUp']((
                    balanceRatiosWithoutFee.value[i], normalizedWeights[i]))

        invariantRatio = WeightedMath._computeExitExactTokensOutInvariantRatio(
            balances,
            normalizedWeights,
            amountsOut,
            balanceRatiosWithoutFee.value,
            invariantRatioWithoutFees.value,
            swapFeePercentage,
            math,
        )

        return math['mulUp']((
            totalSupply, complement(invariantRatio)))

    def _calcTokenOutGivenExactSptIn(
        balance,
        normalizedWeight,
        sptAmountIn,
        sptTotalSupply,
        swapFeePercentage,
        math,
    ):
        # ******************************************************************************************
        #  tokenInForExactSPTOut
        #  a = amountIn
        #  b = balance                      /  /    totalSPT + sptOut      \    (1 / w)       \
        #  bptOut = bptAmountOut   a = b * |  | --------------------------  | ^          - 1  |
        #  bpt = totalSPT                   \  \       totalSPT            /                  /
        #  w = weight
        # ******************************************************************************************
        def complement(x):
            return sp.as_nat(FixedPoint.ONE - x)

        #  Token in, so we round up overall.

        #  Calculate the factor by which the invariant will increase after minting SPTAmountOut

        invariantRatio = math['divUp']((
            sp.as_nat(sptTotalSupply - sptAmountIn), sptTotalSupply))

        sp.verify(invariantRatio >= WeightedMath._MIN_INVARIANT_RATIO,
                  Errors.MIN_SPT_IN_FOR_TOKEN_OUT)

        #  Calculate by how much the token balance has to increase to match the invariantRatio
        balanceRatio = math['powUp']((invariantRatio,
                                      math['divDown']((FixedPoint.ONE, normalizedWeight))))

        amountOutWithoutFee = math['mulDown']((
            balance, complement(balanceRatio)))

        #  We can now compute how much extra balance is being deposited and used in virtual swaps, and charge swap fees
        #  accordingly.
        taxableAmount = math['mulUp']((
            amountOutWithoutFee, complement(normalizedWeight)))

        nonTaxableAmount = sp.as_nat(amountOutWithoutFee - taxableAmount)

        taxableAmountMinusFees = math['mulUp']((
            taxableAmount, complement(swapFeePercentage)))

        return (nonTaxableAmount + taxableAmountMinusFees)

    def _computeExitExactTokensOutInvariantRatio(
        balances,
        normalizedWeights,
        amountsOut,
        balanceRatiosWithoutFee,
        invariantRatioWithoutFees,
        swapFeePercentage,
        math,
    ):

        ir = sp.local('ir', FixedPoint.ONE)
        # ir = sp.local('ir', 1)

        with sp.for_('i', sp.range(0, sp.len(balances))) as i:
            amountOutWithFee = sp.local('amountInWithoutFee', 0)

            with sp.if_(invariantRatioWithoutFees > balanceRatiosWithoutFee[i]):

                nonTaxableAmount = math['mulDown']((
                    balances[i], WeightedMath.complement(invariantRatioWithoutFees)))
                taxableAmount = sp.as_nat(amountsOut[i] - nonTaxableAmount)
                taxableAmountPlusFees = math['divUp']((
                    taxableAmount, WeightedMath.complement(swapFeePercentage)))

                amountOutWithFee.value = nonTaxableAmount + taxableAmountPlusFees
            with sp.else_():
                amountOutWithFee.value = amountsOut[i]

            balanceRatio = math['divDown']((
                sp.as_nat(balances[i] - amountOutWithFee.value), balances[i]))

            ir.value = math['mulDown']((ir.value, math['powDown']((
            balanceRatio, normalizedWeights[i]))))
            # ir.value *= math['powDown']((
            #     balanceRatio, normalizedWeights[i]))

        return ir.value
