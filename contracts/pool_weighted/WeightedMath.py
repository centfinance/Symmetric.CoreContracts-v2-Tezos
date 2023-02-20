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
        invariant = sp.local('inavariant', FixedPoint.ONE)

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
