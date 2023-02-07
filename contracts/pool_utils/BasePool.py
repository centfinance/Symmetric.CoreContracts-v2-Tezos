import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

import contracts.utils.helpers.ScalingHelpers as ScalingHelpers


class BasePool:

    def __init__(self, params):
        pass

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
        self._beforeSwapJoinExit()

        scalingFactors = self._scalingFactors()

        with sp.if_(self.data.totalSupply == 0):
            (sptAmountOut, amountsIn) = self._onInitializePool(
                poolId,
                sender,
                recipient,
                scalingFactors,
                userData
            )

            # // On initialization, we lock _getMinimumBpt() by minting it for the zero address. This BPT acts as a
            # // minimum as it will never be burned, which reduces potential issues with rounding, and also prevents the
            # // Pool from ever being fully drained.
            sp.verify(sptAmountOut >= self._getMinimumBpt(),
                      Errors.MINIMUM_BPT)
            # Mint to Tezos Null address
            self._mintPoolTokens(sp.address(
                'tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU'), self._getMinimumBpt())
            self._mintPoolTokens(
                recipient, (sptAmountOut - self._getMinimumBpt()))

            # // amountsIn are amounts entering the Pool, so we round up.
            ScalingHelpers._downscaleUpArray(amountsIn, scalingFactors)

            # return (amountsIn, new uint256[](balances.length))
        with sp.else_():
            ScalingHelpers._upscaleArray(balances, scalingFactors)
            (sptAmountOut, amountsIn) = self._onJoinPool(
                poolId,
                sender,
                recipient,
                balances,
                lastChangeBlock,
                # // Protocol fees are disabled while in recovery mode
                self.inRecoveryMode() ? 0: protocolSwapFeePercentage,
                scalingFactors,
                userData,
            )

            # // Note we no longer use `balances` after calling `_onJoinPool`, which may mutate it.

            self._mintPoolTokens(recipient, sptAmountOut)

            # // amountsIn are amounts entering the Pool, so we round up.
            ScalingHelpers._downscaleUpArray(amountsIn, scalingFactors)

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
        pass

    @ sp.entry_point
    def setSwapFeePercentage(self, swapFeePercentage):
        pass

    @ sp.onchain_view()
    def getPoolId(self):
        """
        * @dev  this Pool's ID, used when interacting with the Vault (to e.g. join the Pool or swap with it).
        *"""
        pass

    @ sp.onchain_view()
    def getSwapFeePercentage(self):
        """
        @dev  the current swap fee percentage as a 18 decimal fixed point number, so e.g. 1e17 corresponds to a
        10% swap fee.
        """
        pass

    @ sp.onchain_view()
    def getScalingFactors(self):
        """
        * @dev  the scaling factors of each of the Pool's tokens. This is an implementation detail that is typically
        * not relevant for outside parties, but which might be useful for some types of Pools.
        """
        pass

###########
# Internal Functions
###########

    def _onInitializePool(
        self,
        poolId,
        sender,
        receipient,
        scalingFactors,
        userData,
    ):
        pass

    def _onJoinPool(
        self,
        poolId,
        sender,
        receipient,
        balances,
        lastchangeBlock,
        protocolSwapFeePercentage,
        scalingFactors,
        userData,
    ):
        pass
