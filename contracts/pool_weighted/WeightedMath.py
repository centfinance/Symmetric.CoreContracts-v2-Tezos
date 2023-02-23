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

    def _calculateInvariant(normalizedWeights, balances):
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
        # TODO: Fix LogExpMath
        # invariant = sp.local('invariant', FixedPoint.ONE)
        invariant = sp.local('invariant', 1)

        # Iterate through each index in the normalized weights
        with sp.for_('i', sp.range(0, sp.len(normalizedWeights))) as i:
            # Calculate the power of down from the balance and normalized weight
            powDown = FixedPoint.powDown(balances[i], normalizedWeights[i])
            # Multiply the previous invariant to give a new invariant
            # TODO: Fix LogExpMath
            # invariant.value = FixedPoint.mulDown(
            #     invariant.value, powDown)

            invariant.value *= powDown

        # Verify that the new invariant is larger 0
        sp.verify(invariant.value > 0)
        # Return the new invariant
        return invariant.value

    def _calcSptOutGivenExactTokensIn(balances, normalizedWeights, amountsIn, totalSupply, swapFeePercentage):
        def mulDown(x, y):
            return FixedPoint.mulDown(x, y)

        # SPT out, so we round down overall.

        balanceRatiosWithFee = sp.local(
            'balanceRatiosWithFee', sp.map(l={}, tkey=sp.TNat, tvalue=sp.TNat))

        invariantRatioWithFees = sp.local('invariantRatioWithFees', 0)

        with sp.for_('i', sp.range(0, sp.len(balances))) as i:
            balanceRatiosWithFee.value[i] = FixedPoint.divDown(
                (balances[i] + amountsIn[i]), balances[i])
            invariantRatioWithFees.value = invariantRatioWithFees.value + \
                mulDown(balanceRatiosWithFee.value[i], normalizedWeights[i])

        invariantRatio = WeightedMath._computeJoinExactTokensInInvariantRatio(
            balances,
            normalizedWeights,
            amountsIn,
            balanceRatiosWithFee.value,
            invariantRatioWithFees.value,
            swapFeePercentage
        )

        sptOut = sp.local('sptOut', 0)
        with sp.if_(invariantRatio > FixedPoint.ONE):
            sptOut.value = mulDown(
                totalSupply, sp.as_nat(invariantRatio - FixedPoint.ONE))

        return sptOut.value

    def _calcTokenInGivenExactSptOut(
        balance,
        normalizedWeight,
        sptAmountOut,
        sptTotalSupply,
        swapFeePercentage
    ):
        # ******************************************************************************************
        #  tokenInForExactSPTOut
        #  a = amountIn
        #  b = balance                      /  /    totalSPT + sptOut      \    (1 / w)       \
        #  bptOut = bptAmountOut   a = b * |  | --------------------------  | ^          - 1  |
        #  bpt = totalSPT                   \  \       totalSPT            /                  /
        #  w = weight
        # ******************************************************************************************
        def divUp(x, y):
            return FixedPoint.divUp(x, y)

        def mulUp(x, y):
            return FixedPoint.mulUp(x, y)

        def complement(x):
            return sp.as_nat(FixedPoint.ONE - x)

        #  Token in, so we round up overall.

        #  Calculate the factor by which the invariant will increase after minting SPTAmountOut

        invariantRatio = divUp(
            (sptTotalSupply + sptAmountOut), sptTotalSupply)

        sp.verify(invariantRatio <= WeightedMath._MAX_INVARIANT_RATIO,
                  Errors.MAX_OUT_SPT_FOR_TOKEN_IN)

        #  Calculate by how much the token balance has to increase to match the invariantRatio
        balanceRatio = FixedPoint.powUp(invariantRatio,
                                        divUp(FixedPoint.ONE, normalizedWeight))

        amountInWithoutFee = mulUp(
            balance, sp.as_nat(balanceRatio - FixedPoint.ONE))

        #  We can now compute how much extra balance is being deposited and used in virtual swaps, and charge swap fees
        #  accordingly.
        taxableAmount = mulUp(
            amountInWithoutFee, complement(normalizedWeight))

        nonTaxableAmount = sp.as_nat(amountInWithoutFee - taxableAmount)

        taxableAmountPlusFees = divUp(
            taxableAmount, complement(swapFeePercentage))

        return (nonTaxableAmount + taxableAmountPlusFees)

    def _computeJoinExactTokensInInvariantRatio(
        balances,
        normalizedWeights,
        amountsIn,
        balanceRatiosWithFee,
        invariantRatioWithFees,
        swapFeePercentage,
    ):
        def mulDown(x, y):
            return FixedPoint.mulDown(x, y)

        # ir = sp.local('ir', FixedPoint.ONE)
        ir = sp.local('ir', 1)

        with sp.for_('i', sp.range(0, sp.len(balances))) as i:
            amountInWithoutFee = sp.local('amountInWithoutFee', 0)

            with sp.if_(balanceRatiosWithFee[i] > invariantRatioWithFees):

                nta = sp.local('nta', 0)
                with sp.if_(invariantRatioWithFees > FixedPoint.ONE):
                    nta.value = mulDown(
                        balances[i], sp.as_nat(invariantRatioWithFees - FixedPoint.ONE))
                swapFee = FixedPoint.mulUp(
                    sp.as_nat(amountsIn[i] - nta.value), swapFeePercentage)
                amountInWithoutFee.value = sp.as_nat(
                    amountsIn[i] - swapFee)
            with sp.else_():
                amountInWithoutFee.value = amountsIn[i]

            balanceRatio = FixedPoint.divDown(
                (balances[i] + amountInWithoutFee.value), balances[i])

            # ir.value = mulDown(ir.value, FixedPoint.powDown(
            # balanceRatio, normalizedWeights[i]))
            ir.value *= FixedPoint.powDown(
                balanceRatio, normalizedWeights[i])

        return ir.value
