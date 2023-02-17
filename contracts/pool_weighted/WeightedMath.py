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
        invariant = sp.compute(FixedPoint.ONE)

        with sp.for_('i', sp.range(0, sp.len(normalizedWeights))) as i:
            invariant = FixedPoint.mulDown(
                invariant, FixedPoint.powDown(balances[i], normalizedWeights[i]))

        sp.verify(invariant > 0)
