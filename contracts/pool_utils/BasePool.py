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


class BasePool(
    SymmetricPoolToken,
):

    def __init__(
        self,
        vault,
        name,
        symbol,
        owner,
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
        # self.data.protocolFeesCollector = vault.getProtocolFeesCollector();

    @sp.entry_point
    def onJoinPool(
        self,
        poolId,
        sender,
        recipient,
        balances,
        lastChangeBlock,
        protocolSwapFeePercentage,
        userData
    ):
        """
              @dev Called by the Vault when a user calls `IVault.joinPool` to add liquidity to this Pool.  how many of
              each registered token the user should provide, as well as the amount of protocol fees the Pool owes to the Vault.
              The Vault will then take tokens from `sender` and add them to the Pool's balances, as well as collect
              the reported amount in protocol fees, which the pool should calculate based on `protocolSwapFeePercentage`.

              Protocol fees are reported and charged on join events so that the Pool is free of debt whenever new users join.

              `sender` is the account performing the join (from which tokens will be withdrawn), and `recipient` is the account
              designated to receive any benefits (typically pool shares). `balances` contains the total balances
              for each token the Pool registered in the Vault, in the same order that `IVault.getPoolTokens` would return.

              `lastChangeBlock` is the last block in which any of the Pool's registered tokens last changed its total
              balance.

              `userData` contains any pool-specific instructions needed to perform the calculations, such as the type of
              join (e.g., proportional given an amount of pool shares, single-asset, multi-asset, etc.)

              Contracts implementing this def should check that the caller is indeed the Vault before performing any
              state-changing operations, such as minting pool shares.
        """
        # only vault and vailid pool id can call

        # ensureNotPaused
        # self._beforeSwapJoinExit()
        sp.set_type(balances, sp.TMap(sp.TNat, sp.TNat))
        scalingFactors = self.data.scalingFactors

        with sp.if_(self.data.totalSupply == 0):
            (sptAmountOut, amountsIn) = self._onInitializePool(
                sp.record(
                    poolId=poolId,
                    sender=sender,
                    recipient=recipient,
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
                    poolId=poolId,
                    sender=sender,
                    recipient=recipient,
                    upScaledBalances=upScaledBalances,
                    lastChangeBlock=lastChangeBlock,
                    # // Protocol fees are disabled while in recovery mode
                    # self.inRecoveryMode() ? 0: protocolSwapFeePercentage,
                    protocolSwapFeePercentage=protocolSwapFeePercentage,
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

    @sp.entry_point
    def onExitPool(
        self,
        poolId,
        sender,
        recipient,
        balances,
        lastChangeBlock,
        protocolSwapFeePercentage,
        userData
    ):
        """
          * @dev Called by the Vault when a user calls `IVault.exitPool` to remove liquidity from this Pool.  how many
          * tokens the Vault should deduct from the Pool's balances, as well as the amount of protocol fees the Pool owes
          * to the Vault. The Vault will then take tokens from the Pool's balances and send them to `recipient`,
          * as well as collect the reported amount in protocol fees, which the Pool should calculate based on
          * `protocolSwapFeePercentage`.
          *
          * Protocol fees are charged on exit events to guarantee that users exiting the Pool have paid their share.
          *
          * `sender` is the account performing the exit (typically the pool shareholder), and `recipient` is the account
          * to which the Vault will send the proceeds. `balances` contains the total token balances for each token
          * the Pool registered in the Vault, in the same order that `IVault.getPoolTokens` would return.
          *
          * `lastChangeBlock` is the last block in which *any* of the Pool's registered tokens last changed its total
          * balance.
          *
          * `userData` contains any pool-specific instructions needed to perform the calculations, such as the type of
          * exit (e.g., proportional given an amount of pool shares, single-asset, multi-asset, etc.)
          *
          * Contracts implementing this def should check that the caller is indeed the Vault before performing any
          * state-changing operations, such as burning pool shares.
        """
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
        with sp.else_():
            scalingFactors = self.data.scalingFactors
            (sptAmountIn, amountsOut) = self._onExitPool(
                sp.record(
                    poolId=poolId,
                    sender=sender,
                    recipient=recipient,
                    balances=balances,
                    lastChangeBlock=lastChangeBlock,
                    # inRecoveryMode() ? 0 : protocolSwapFeePercentage, // Protocol fees are disabled while in recovery mode
                    protocolSwapFeePercentage=protocolSwapFeePercentage,
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
        scalingFactors = self.data.scalingFactors

        with sp.if_(self.data.totalSupply == 0):
            (sptAmountOut, amountsIn) = self._onInitializePool(
                sp.record(
                    poolId=params.poolId,
                    sender=params.sender,
                    recipient=params.recipient,
                    scalingFactors=scalingFactors,
                    userData=params.userData,
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
                params.recipient, sp.as_nat(sptAmountOut - _DEFAULT_MINIMUM_SPT))

            # // amountsIn are amounts entering the Pool, so we round up.
            # ScalingHelpers._downscaleUpArray(amountsIn, scalingFactors)

        with sp.else_():
            upScaledBalances = ScalingHelpers._upscaleArray(
                params.balances, scalingFactors)
            (sptAmountOut, amountsIn) = self._onJoinPool(
                sp.record(
                    poolId=params.poolId,
                    sender=params.sender,
                    recipient=params.recipient,
                    upScaledBalances=upScaledBalances,
                    lastChangeBlock=params.lastChangeBlock,
                    # // Protocol fees are disabled while in recovery mode
                    # self.inRecoveryMode() ? 0: protocolSwapFeePercentage,
                    protocolSwapFeePercentage=params.protocolSwapFeePercentage,
                    scalingFactors=scalingFactors,
                    userData=params.userData,
                )
            )
        # amountsIn are amounts entering the Pool, so we round up.
        downscaledAmounts = ScalingHelpers._downscaleUpArray(
            amountsIn, scalingFactors)

        # This Pool ignores the `dueProtocolFees` return value, so we simply return a zeroed-out array.
        sp.result((sptAmountOut, downscaledAmounts))

    @sp.onchain_view()
    def beforeExitPool(
        self,
        params,
    ):
        downscaledAmounts = sp.local('downScaledAmounts', {})
        with sp.if_(params.userData.recoveryModeExit):
            # TODO: Check that it's in recovery mode
            # _ensureInRecoveryMode();
            # Note that we don't upscale balances nor downscale amountsOut - we don't care about scaling factors during
            # a recovery mode exit.
            (sptAmountIn, amountsOut) = self._doRecoveryModeExit(
                sp.record(
                    balances=params.balances,
                    totalSupply=self.data.totalSupply,
                    userData=params.userData
                )
            )
        with sp.else_():
            scalingFactors = self.data.scalingFactors
            (sptAmountIn, amountsOut) = self._onExitPool(
                sp.record(
                    poolId=params.poolId,
                    sender=params.sender,
                    recipient=params.recipient,
                    balances=params.balances,
                    lastChangeBlock=params.lastChangeBlock,
                    # inRecoveryMode() ? 0 : protocolSwapFeePercentage, // Protocol fees are disabled while in recovery mode
                    protocolSwapFeePercentage=params.protocolSwapFeePercentage,
                    scalingFactors=scalingFactors,
                    userData=params.userData
                )
            )
            downscaledAmounts.value = ScalingHelpers._downscaleDownArray(
                amountsOut, scalingFactors)
            sp.result((sptAmountIn, downscaledAmounts))

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
