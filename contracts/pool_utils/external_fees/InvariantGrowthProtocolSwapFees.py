import smartpy as sp

import contracts.utils.math.FixedPoint as FixedPoint


class InvariantGrowthProtocolSwapFees:

    def getProtocolOwnershipPercentage(
        invariantGrowthRatio,
        supplyGrowthRatio,
        protocolSwapFeePercentage,
    ):
        percentage = sp.local('percentage', sp.nat(0))
        with sp.if_((supplyGrowthRatio < invariantGrowthRatio) | (protocolSwapFeePercentage != sp.nat(0))):
            percentage.value = sp.as_nat(
                FixedPoint.ONE - FixedPoint.divDown(supplyGrowthRatio, invariantGrowthRatio))
            percentage.value = FixedPoint.mulDown(
                percentage.value, protocolSwapFeePercentage)

        return percentage.value
