import smartpy as sp

import contracts.utils.math.FixedPoint as FixedPoint


class InvariantGrowthProtocolSwapFees:
    def getProtocolOwnershipPercentage(
        invariantGrowthRatio,
        supplyGrowthRatio,
        protocolSwapFeePercentage,
        math,
    ):
        return sp.eif(
            ((supplyGrowthRatio >= invariantGrowthRatio)
             | (protocolSwapFeePercentage == sp.nat(0))),
            sp.nat(0),
            math['mulDown']((sp.as_nat(FixedPoint.ONE - math['divDown']
                                       ((supplyGrowthRatio, invariantGrowthRatio))), protocolSwapFeePercentage)),
        )

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
            currentSupply, protocolOwnershipPercentage)

    def sptForPoolOwnershipPercentage(
            totalSupply,
            poolOwnershipPercentage,
    ):
        return (totalSupply * poolOwnershipPercentage) // sp.as_nat(FixedPoint.ONE - poolOwnershipPercentage)
