import smartpy as sp

import contracts.utils.math.FixedPoint as FixedPoint


class InvariantGrowthProtocolSwapFees:

    def getProtocolOwnershipPercentage(
        invariantGrowthRatio,
        supplyGrowthRatio,
        protocolSwapFeePercentage,
        math,
    ):
        percentage = sp.local('percentage', sp.nat(0))
        with sp.if_((supplyGrowthRatio < invariantGrowthRatio) | (protocolSwapFeePercentage != sp.nat(0))):
            percentage.value = sp.as_nat(
                FixedPoint.ONE - math['divDown']((supplyGrowthRatio, invariantGrowthRatio)))
            percentage.value = math['mulDown']((
                percentage.value, protocolSwapFeePercentage))

        return percentage.value

    def calcDueProtocolFees(
        invariantGrowthRatio,
        previousSupply,
        currentSupply,
        protocolSwapFeePercentage,
        divDown,
    ):
        protocolOwnershipPercentage = InvariantGrowthProtocolSwapFees.getProtocolOwnershipPercentage(
            invariantGrowthRatio,
            divDown(currentSupply, previousSupply),
            protocolSwapFeePercentage
        )

        return InvariantGrowthProtocolSwapFees.sptForPoolOwnershipPercentage(
            currentSupply, protocolOwnershipPercentage, divDown)

    def sptForPoolOwnershipPercentage(totalSupply, poolOwnershipPercentage, divDown):
        return divDown((totalSupply * poolOwnershipPercentage), sp.as_nat(FixedPoint.ONE - poolOwnershipPercentage))
