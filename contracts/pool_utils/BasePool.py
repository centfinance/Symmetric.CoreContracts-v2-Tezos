import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

import contracts.utils.helpers.ScalingHelpers as ScalingHelpers

import contracts.utils.math.FixedPoint as FixedPoint

import contracts.pool_utils.lib.PoolRegistrationLib as PoolRegistrationLib

from contracts.pool_utils.SymmetricPoolToken import SymmetricPoolToken

_MIN_TOKENS = 2
_DEFAULT_MINIMUM_SPT = 1000000
_MIN_SWAP_FEE_PERCENTAGE = 1000000000000
_MAX_SWAP_FEE_PERCENTAGE = 100000000000000000
_SWAP_FEE_PERCENTAGE_OFFSET = 1000000000000

_SWAP_FEE_PERCENTAGE_BIT_LENGTH = 100000000000000000


class IBasePool:
    JOIN_USER_DATA = sp.TRecord(
        kind=sp.TString,
        amountsIn=sp.TOption(sp.TMap(sp.TNat, sp.TNat)),
        minSPTAmountOut=sp.TOption(sp.TNat),
        sptAmountOut=sp.TOption(sp.TNat),
        tokenIndex=sp.TOption(sp.TNat),
        allT=sp.TOption(sp.TNat),
    )

    EXIT_USER_DATA = sp.TRecord(
        kind=sp.TString,
        amountsOut=sp.TOption(sp.TMap(sp.TNat, sp.TNat)),
        maxSPTAmountIn=sp.TOption(sp.TNat),
        sptAmountIn=sp.TOption(sp.TNat),
        tokenIndex=sp.TOption(sp.TNat),
        recoveryModeExit=sp.TBool,
    )

    t_on_join_pool_params = sp.TRecord(
        balances=sp.TMap(sp.TNat, sp.TNat),
        recipient=sp.TAddress,
        userData=JOIN_USER_DATA,
    )

    t_on_exit_pool_params = sp.TRecord(
        balances=sp.TMap(sp.TNat, sp.TNat),
        sender=sp.TAddress,
        userData=EXIT_USER_DATA,
    )

    t_before_join_pool_params = sp.TRecord(
        balances=sp.TMap(sp.TNat, sp.TNat),
        userData=JOIN_USER_DATA,
    )

    t_before_exit_pool_params = sp.TRecord(
        balances=sp.TMap(sp.TNat, sp.TNat),
        userData=EXIT_USER_DATA,
    )


class BasePool(
    SymmetricPoolToken,
):

    def __init__(
        self,
        vault,
        name,
        symbol,
    ):
        self.update_initial_storage(
            poolId=sp.none,
            swapFeePercentage=sp.nat(0),
            protocolFeesCollector=sp.none
        )
        SymmetricPoolToken.__init__(self, name, symbol, vault)

    @sp.entry_point
    def initialize(
        self,
        params,
    ):
        sp.verify(self.data.initialized == False)

        tokensAmount = sp.len(params.tokens)
        sp.verify(tokensAmount >= _MIN_TOKENS, Errors.MIN_TOKENS)
        sp.verify(tokensAmount <= self.MAX_TOKENS, Errors.MAX_TOKENS)

        self._setSwapFeePercentage(params.swapFeePercentage)

        poolId = PoolRegistrationLib.registerPool(
            vault=params.vault,
            specialization=params.specialization,
            tokens=params.tokens,
            assetManagers=params.assetManagers
        )

        self.data.poolId = sp.some(poolId)

        # TODO: Add protocolFeesCollector call to vault
        # self.data.protocolFeesCollector = vault.getProtocolFeesCollector()
        self.data.protocolFeesCollector = sp.some(
            sp.address('KT1N5Qpp5DaJzEgEXY1TW6Zne6Eehbxp83XF'))

    @sp.entry_point(parameter_type=IBasePool.t_on_join_pool_params)
    def onJoinPool(
        self,
        recipient,
        balances,
        userData
    ):
        # only vault and vailid pool id can call

        # ensureNotPaused
        # self._beforeSwapJoinExit()
        scalingFactors = self.data.scalingFactors

        with sp.if_(self.data.totalSupply == 0):
            (sptAmountOut, amountsIn) = self._onInitializePool(
                sp.record(
                    scalingFactors=scalingFactors,
                    userData=userData,
                )
            )

            # // On initialization, we lock _getMinimumBpt() by minting it for the zero address. This BPT acts as a
            # // minimum as it will never be burned, which reduces potential issues with rounding, and also prevents the
            # // Pool from ever being fully drained.
            sp.verify(sptAmountOut >= _DEFAULT_MINIMUM_SPT,
                      Errors.MINIMUM_SPT)
            # Mint to Tezos Null address
            self._mintPoolTokens(sp.address(
                'tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU'), _DEFAULT_MINIMUM_SPT)
            self._mintPoolTokens(
                recipient, sp.as_nat(sptAmountOut - _DEFAULT_MINIMUM_SPT))

            # // amountsIn are amounts entering the Pool, so we round up.
            # ScalingHelpers._downscaleUpArray(amountsIn, scalingFactors)

        with sp.else_():
            upScaledBalances = ScalingHelpers._upscaleArray(
                balances, scalingFactors)
            (sptAmountOut, amountsIn) = self._onJoinPool(
                sp.record(
                    balances=upScaledBalances,
                    scalingFactors=scalingFactors,
                    userData=userData,
                )
            )

            # // Note we no longer use `balances` after calling `_onJoinPool`, which may mutate it.

            self._mintPoolTokens(recipient, sptAmountOut)

        # // amountsIn are amounts entering the Pool, so we round up.
        # downscaledAmounts = ScalingHelpers._downscaleUpArray(
        #     amountsIn, scalingFactors)

        # // This Pool ignores the `dueProtocolFees` return value, so we simply return a zeroed-out array.
        # return (amountsIn, new uint256[](balances.length));

    @sp.entry_point(parameter_type=IBasePool.t_on_exit_pool_params)
    def onExitPool(
        self,
        sender,
        balances,
        userData
    ):
        with sp.if_(userData.recoveryModeExit):
            # TODO: Check that it's in recovery mode
            # _ensureInRecoveryMode();
            # Note that we don't upscale balances nor downscale amountsOut - we don't care about scaling factors during
            # a recovery mode exit.
            (sptAmountIn, amountsOut) = self._doRecoveryModeExit(
                sp.record(
                    balances=balances,
                    totalSupply=self.data.totalSupply,
                    userData=userData
                )
            )
            self._burnPoolTokens(sender, sptAmountIn)

        with sp.else_():
            scalingFactors = self.data.scalingFactors
            (sptAmountIn, amountsOut) = self._onExitPool(
                sp.record(
                    balances=balances,
                    scalingFactors=scalingFactors,
                    userData=userData
                )
            )
            self._burnPoolTokens(sender, sptAmountIn)

    # @ sp.entry_point
    # def setSwapFeePercentage(self, swapFeePercentage):
    #     pass

    @sp.onchain_view()
    def beforeJoinPool(
        self,
        params,
    ):
        sp.set_type(params, IBasePool.t_before_join_pool_params)
        scalingFactors = self.data.scalingFactors
        result = sp.local('result', (0, {}))
        with sp.if_(self.data.totalSupply == 0):
            result.value = self._onInitializePool(
                sp.record(
                    scalingFactors=scalingFactors,
                    userData=params.userData,
                )
            )

        with sp.else_():
            upScaledBalances = ScalingHelpers._upscaleArray(
                params.balances, scalingFactors)
            result.value = self._onJoinPool(
                sp.record(
                    balances=upScaledBalances,
                    scalingFactors=scalingFactors,
                    userData=params.userData,
                )
            )
        # amountsIn are amounts entering the Pool, so we round up.
        downscaledAmounts = ScalingHelpers._downscaleUpArray(
            sp.snd(result.value), scalingFactors)

        # This Pool ignores the `dueProtocolFees` return value, so we simply return a zeroed-out array.
        sp.result((sp.fst(result.value), downscaledAmounts))

    @sp.onchain_view()
    def beforeExitPool(
        self,
        params,
    ):
        sp.set_type(params, IBasePool.t_before_exit_pool_params)
        result = sp.local('result', (0, {}))
        with sp.if_(params.userData.recoveryModeExit):
            # TODO: Check that it's in recovery mode
            # _ensureInRecoveryMode();

            result.value = self._doRecoveryModeExit(
                sp.record(
                    balances=params.balances,
                    totalSupply=self.data.totalSupply,
                    userData=params.userData
                )
            )
        with sp.else_():
            scalingFactors = self.data.scalingFactors
            result.value = self._onExitPool(
                sp.record(
                    balances=params.balances,
                    scalingFactors=scalingFactors,
                    userData=params.userData
                )
            )

        downscaledAmounts = ScalingHelpers._downscaleDownArray(
            sp.snd(result.value), scalingFactors)
        sp.result((sp.fst(result.value), downscaledAmounts))

    # @ sp.onchain_view()
    # def getPoolId(self):
    #     """
    #     * @dev  this Pool's ID, used when interacting with the Vault (to e.g. join the Pool or swap with it).
    #     *"""
    #     pass

    # @ sp.onchain_view()
    # def getSwapFeePercentage(self):
    #     """
    #     @dev  the current swap fee percentage as a 18 decimal fixed point number, so e.g. 1e17 corresponds to a
    #     10% swap fee.
    #     """
    #     pass

    # @ sp.onchain_view()
    # def getScalingFactors(self):
    #     """
    #     * @dev  the scaling factors of each of the Pool's tokens. This is an implementation detail that is typically
    #     * not relevant for outside parties, but which might be useful for some types of Pools.
    #     """
    #     pass

###########
# Internal Functions
###########

    def _addSwapFeeAmount(self, amount):
        # This returns amount + fee amount, so we round up (favoring a higher fee amount).
        return FixedPoint.divUp(amount, FixedPoint.complement(self.data.swapFeePercentage))

    def _subtractSwapFeeAmount(self, amount):
        # This returns amount - fee amount, so we round up (favoring a higher fee amount).
        feeAmount = FixedPoint.mulUp(amount, self.data.swapFeePercentage)
        return sp.as_nat(amount - feeAmount)

    def _setSwapFeePercentage(self, swapFeePercentage):
        sp.verify(swapFeePercentage >= _MIN_SWAP_FEE_PERCENTAGE,
                  Errors.MIN_SWAP_FEE_PERCENTAGE)
        sp.verify(swapFeePercentage <= _MAX_SWAP_FEE_PERCENTAGE,
                  Errors.MAX_SWAP_FEE_PERCENTAGE)

        self.data.swapFeePercentage = swapFeePercentage

        sp.emit(swapFeePercentage, 'SwapFeePercentageChanged')

    def _computeScalingFactor(self, decimals):
        sp.set_type(decimals, sp.TNat)
        decimalsDifference = sp.as_nat(18 - decimals)
        return FixedPoint.ONE * (FixedPoint.pow(sp.nat(10), decimalsDifference))

    # def _onInitializePool(
    #     self,
    #     poolId,
    #     sender,
    #     receipient,
    #     scalingFactors,
    #     userData,
    # ):
    #     pass

    # def _onJoinPool(
    #     self,
    #     poolId,
    #     sender,
    #     receipient,
    #     balances,
    #     lastchangeBlock,
    #     protocolSwapFeePercentage,
    #     scalingFactors,
    #     userData,
    # ):
    #     pass
