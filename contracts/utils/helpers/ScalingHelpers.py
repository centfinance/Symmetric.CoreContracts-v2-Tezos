import smartpy as sp

import contracts.utils.math.FixedPoint as FixedPoint
import contracts.utils.helpers.InputHelpers as InputHelpers


def _upscale(amount,  scalingFactor):
    # // Upscale rounding wouldn't necessarily always go in the same direction: in a swap for example the balance of
    # // token in should be rounded up, and that of token out rounded down. This is the only place where we round in
    # // the same direction for all amounts, as the impact of this rounding is expected to be minimal.
    return FixedPoint.mulDown(amount, scalingFactor)


# /**
#  * @dev Reverses the `scalingFactor` applied to `amount`, resulting in a smaller or equal value depending on
#  * whether it needed scaling or not. The result is rounded down.
#  */
def _downscaleDown(amount, scalingFactor):
    return FixedPoint.divDown(amount, scalingFactor)

# /**
#  * @dev Reverses the `scalingFactor` applied to `amount`, resulting in a smaller or equal value depending on
#  * whether it needed scaling or not. The result is rounded up.
#  */


def _downscaleUp(amount, scalingFactor):
    return FixedPoint.divUp(amount, scalingFactor)


# /**
#  * @dev Same as `_upscale`, but for an entire array. This function does not return anything, but instead *mutates*
#  * the `amounts` array.
#  */
def _upscaleArray(amounts, scalingFactors):
    length = amounts.length
    InputHelpers.ensureInputLengthMatch(length, scalingFactors.length)
    upscaledAmounts = sp.local('upscaledAmounts', [])
    with sp.for_('i' in sp.range(0, length)) as i:
        upscaledAmounts.value.push(
            FixedPoint.mulDown(amounts[i], scalingFactors[i]))

    return upscaledAmounts.value.rev()


# /**
#  * @dev Same as `_downscaleDown`, but for an entire array. This function does not return anything, but instead
#  * *mutates* the `amounts` array.
#  */
def _downscaleDownArray(amounts, scalingFactors):
    length = amounts.length
    InputHelpers.ensureInputLengthMatch(length, scalingFactors.length)
    downscaledAmounts = sp.local('downscaledAmounts', [])
    with sp.for_('i' in sp.range(0, length)) as i:
        downscaledAmounts.value.push(
            FixedPoint.divDown(amounts[i], scalingFactors[i]))

    return downscaledAmounts.value.rev()

# /**
#  * @dev Same as `_downscaleUp`, but for an entire array. This function does not return anything, but instead
#  * *mutates* the `amounts` array.
#  */


def _downscaleUpArray(amounts, scalingFactors):
    length = amounts.length
    InputHelpers.ensureInputLengthMatch(length, scalingFactors.length)
    downscaledAmounts = sp.local('downscaledAmounts', [])
    with sp.for_('i' in sp.range(0, length)) as i:
        downscaledAmounts.value.push(
            FixedPoint.divUp(amounts[i], scalingFactors[i]))

    return downscaledAmounts.value.rev()


def _computeScalingFactor(token):
    # // Tokens that don't implement the `decimals` method are not supported.
    tokenDecimals = ERC20(address(token)).decimals()

    # // Tokens with more than 18 decimals are not supported.
    decimalsDifference = Math.sub(18, tokenDecimals)
    return FixedPoint.ONE * 10**decimalsDifference
