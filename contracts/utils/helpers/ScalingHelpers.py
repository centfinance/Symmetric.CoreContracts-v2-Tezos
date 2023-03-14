import smartpy as sp

import contracts.utils.math.FixedPoint as FixedPoint
import contracts.utils.helpers.InputHelpers as InputHelpers


def _upscale(amount,  scalingFactor):
    # // Upscale rounding wouldn't necessarily always go in the same direction: in a swap for example the balance of
    # // token in should be rounded up, and that of token out rounded down. This is the only place where we round in
    # // the same direction for all amounts, as the impact of this rounding is expected to be minimal.
    return FixedPoint.mulDown((amount, scalingFactor))


# /**
#  * @dev Reverses the `scalingFactor` applied to `amount`, resulting in a smaller or equal value depending on
#  * whether it needed scaling or not. The result is rounded down.
#  */
def _downscaleDown(amount, scalingFactor):
    return FixedPoint.divDown((amount, scalingFactor))

# /**
#  * @dev Reverses the `scalingFactor` applied to `amount`, resulting in a smaller or equal value depending on
#  * whether it needed scaling or not. The result is rounded up.
#  */


def _downscaleUp(amount, scalingFactor):
    return FixedPoint.divUp((amount, scalingFactor))


# /**
#  * @dev Same as `_upscale`, but for an entire array. This function does not return anything, but instead *mutates*
#  * the `amounts` array.
#  */
def _upscaleArray(amounts, scalingFactors, mulDown):
    length = sp.len(amounts)
    # InputHelpers.ensureInputLengthMatch(length, scalingFactors.length)
    upscaledAmounts = sp.compute(sp.map(
        {}, tkey=sp.TNat, tvalue=sp.TNat))
    with sp.for_('i', sp.range(0, length)) as i:
        upscaledAmounts[i] = mulDown((
            amounts[i], scalingFactors[i]))

    return upscaledAmounts


# /**
#  * @dev Same as `_downscaleDown`, but for an entire array. This function does not return anything, but instead
#  * *mutates* the `amounts` array.
#  */
def _downscaleDownArray(amounts, scalingFactors, divDown):
    length = sp.len(amounts)
    # InputHelpers.ensureInputLengthMatch(length, scalingFactors.length)
    downscaledAmounts = sp.compute(sp.map(
        {}, tkey=sp.TNat, tvalue=sp.TNat))
    with sp.for_('i', sp.range(0, length)) as i:
        downscaledAmounts[i] = divDown((
            amounts[i], scalingFactors[i]))

    return downscaledAmounts

# /**
#  * @dev Same as `_downscaleUp`, but for an entire array. This function does not return anything, but instead
#  * *mutates* the `amounts` array.
#  */


def _downscaleUpArray(amounts, scalingFactors, divUp):
    length = sp.len(amounts)
    # InputHelpers.ensureInputLengthMatch(length, scalingFactors.length)
    downscaledAmounts = sp.compute(sp.map(
        {}, tkey=sp.TNat, tvalue=sp.TNat))
    with sp.for_('i', sp.range(0, length)) as i:
        downscaledAmounts[i] = divUp((
            (amounts[i], scalingFactors[i])))

    return downscaledAmounts


# def _computeScalingFactor(token):
#     # // Tokens that don't implement the `decimals` method are not supported.
#     tokenDecimals = ERC20(address(token)).decimals()

#     # // Tokens with more than 18 decimals are not supported.
#     decimalsDifference = Math.sub(18, tokenDecimals)
#     return FixedPoint.ONE * 10**decimalsDifference
