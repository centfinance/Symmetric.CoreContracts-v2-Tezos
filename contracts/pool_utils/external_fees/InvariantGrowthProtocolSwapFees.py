import smartpy as sp

import contracts.interfaces.SymmetricEnums as Enums

import contracts.utils.math.FixedPoint as FixedPoint


class InvariantGrowthProtocolSwapFees:
    """
    InvariantGrowthProtocolSwapFees calculates the protocol fees for users joining or exiting a liquidity pool.

    This class leverages a function for invariant growth to determine the proportion of protocol ownership
    when users join or exit a liquidity pool. It also provides a method to determine the exact amount of
    due protocol fees based on the pool's supply growth and the protocol's swap fee percentage.

    Methods:
        getProtocolOwnershipPercentage(
            invariantGrowthRatio: sp.TNat,
            supplyGrowthRatio: sp.TNat,
            protocolSwapFeePercentage: sp.TNat,
            math: dict
        ) -> sp.TNat:
            Calculates the percentage of the protocol ownership based on the growth ratio of the 
            invariant and supply and the protocol's swap fee percentage.

        calcDueProtocolFees(
            invariantGrowthRatio: sp.TNat,
            previousSupply: sp.TNat,
            currentSupply: sp.TNat,
            protocolSwapFeePercentage: sp.TNat,
            math: dict
        ) -> sp.TNat:
            Computes the amount of protocol fees to be paid when joining or exiting a liquidity pool.
            It leverages the getProtocolOwnershipPercentage method internally.
    """
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
            math[Enums.MUL_DOWN]((sp.as_nat(FixedPoint.ONE - math[Enums.DIV_DOWN]
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
            math[Enums.DIV_DOWN]((currentSupply, previousSupply)),
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
