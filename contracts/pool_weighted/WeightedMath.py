import smartpy as sp

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
        invariant = sp.local('invariant', FixedPoint.ONE)

        # Iterate through each index in the normalized weights
        with sp.for_('i', sp.range(0, sp.len(normalizedWeights))) as i:
            # Calculate the power of down from the balance and normalized weight
            powDown = FixedPoint.powDown(balances[i], normalizedWeights[i])
            # Multiply the previous invariant to give a new invariant
            invariant.value = FixedPoint.mulDown(
                invariant.value, powDown)

        # Verify that the new invariant is larger 0
        sp.verify(invariant.value > 0)
        # Return the new invariant
        return invariant.value

    def _calcSptOutGivenExactTokensIn(balances, normalizedWeights, amountsIn, totalSupply, swapFeePercentage):
        # SPT out, so we round down overall.

        balanceRatiosWithFee = sp.map({}, tkey=sp.TNat, tvalue=sp.TNat)

        invariantRatioWithFees = sp.local('invariantRatioWithFees', 0)

        with sp.for_('i', sp.range(0, sp.len(balances))) as i:
            balanceRatiosWithFee[i] = FixedPoint.divDown(
                FixedPoint.add(balances[i], amountsIn[i]), balances[i])
            invariantRatioWithFees.value = FixedPoint.add(invariantRatioWithFees.value,
                                                          FixedPoint.mulDown(balanceRatiosWithFee[i], normalizedWeights[i]))

        invariantRatio = WeightedMath._computeJoinExactTokensInInvariantRatio(
            balances,
            normalizedWeights,
            amountsIn,
            balanceRatiosWithFee,
            invariantRatioWithFees.value,
            swapFeePercentage
        )

        sptOut = sp.local('sptOut', 0)

        with sp.if_(invariantRatio > FixedPoint.ONE):
            sptOut.value = FixedPoint.mulDown(
                totalSupply, (invariantRatio - FixedPoint.ONE))

        return sptOut

    def _computeJoinExactTokensInInvariantRatio(
        balances,
        normalizedWeights,
        amountsIn,
        balanceRatiosWithFee,
        invariantRatioWithFees,
        swapFeePercentage,
    ):
        invariantRatio = sp.local('invariantRatio', FixedPoint.ONE)

        with sp.for_('i', sp.range(0, sp.len(balances))) as i:
            amountInWithoutFee = sp.local('amountInWithoutFee', 0)
            with sp.if_(balanceRatiosWithFee[i] > invariantRatioWithFees):
                nonTaxableAmount = sp.local('nonTaxableAmount', 0)
                with sp.if_(invariantRatioWithFees > FixedPoint.ONE):
                    nonTaxableAmount.value = FixedPoint.mulDown(
                        balances[i], sp.as_nat(invariantRatioWithFees - FixedPoint.ONE))
                    swapFee = FixedPoint.mulUp(
                        sp.as_nat(amountsIn[i] - nonTaxableAmount), swapFeePercentage)
                    amountInWithoutFee.value = sp.as_nat(
                        amountsIn[i] - swapFee)
                with sp.else_():
                    amountInWithoutFee.value = amountsIn[i]

                balanceRatio = FixedPoint.divDown(
                    (balances[i] + amountInWithoutFee), balances[i])
                invariantRatio.value = FixedPoint.mulDown(
                    invariantRatio.value, FixedPoint.powDown(balanceRatio, normalizedWeights[i]))

        return invariantRatio.value
