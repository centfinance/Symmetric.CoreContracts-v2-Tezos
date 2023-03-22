import smartpy as sp

import contracts.utils.math.FixedPoint as FixedPoint


class InvariantGrowthProtocolSwapFees:

    # def getProtocolOwnershipPercentage(invariantGrowthRatio, supplyGrowthRatio, protocolSwapFeePercentage, math):
    #     with sp.if_((supplyGrowthRatio < invariantGrowthRatio) | (protocolSwapFeePercentage != sp.nat(0))):
    #         percent = sp.as_nat(
    #             FixedPoint.ONE - math['divDown']((supplyGrowthRatio, invariantGrowthRatio)))

    #         percent = math['mulDown']((percent, protocolSwapFeePercentage))
    #         return percent
    #     return sp.nat(0)  # or any default value if conditions are not met

    def getProtocolOwnershipPercentage(
        invariantGrowthRatio,
        supplyGrowthRatio,
        protocolSwapFeePercentage,
        math,
    ):
        with sp.if_((supplyGrowthRatio < invariantGrowthRatio) | (protocolSwapFeePercentage != sp.nat(0))):
            percent = sp.as_nat(
                FixedPoint.ONE - math['divDown']((supplyGrowthRatio, invariantGrowthRatio)))
            percent = math['mulDown']((
                percent, protocolSwapFeePercentage))
            return percent

        return sp.nat(0)

    def calcDueProtocolFees(
        invariantGrowthRatio,
        previousSupply,
        currentSupply,
        protocolSwapFeePercentage,
        math,
    ):
        protocolOwnershipPercentage = InvariantGrowthProtocolSwapFees.getProtocolOwnershipPercentage(
            invariantGrowthRatio,
            math['divDown']((currentSupply, previousSupply)),
            protocolSwapFeePercentage,
            math,
        )

        return InvariantGrowthProtocolSwapFees.sptForPoolOwnershipPercentage(
            currentSupply, protocolOwnershipPercentage, math['divDown'])

    def sptForPoolOwnershipPercentage(
            totalSupply,
            poolOwnershipPercentage,
            divDown
    ):

        return divDown(((totalSupply * poolOwnershipPercentage),
                        sp.as_nat(FixedPoint.ONE - poolOwnershipPercentage)))
