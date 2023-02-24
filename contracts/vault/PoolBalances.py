import smartpy as sp

from contracts.vault.PoolTokens import PoolTokens


class PoolBalances(
    PoolTokens,
):
    def __init__(self):
        PoolTokens.__init__(self)

    def joinPool(
        self,
        poolId,
        sender,
        recipient,
        request
    ):
        self._joinOrExit(
            1,
            poolId,
            sender,
            recipient,
            request
        )

    def exitPool(
        self,
        poolId,
        sender,
        recipient,
        request
    ):
        self._joinOrExit(
            0,
            poolId,
            sender,
            recipient,
            request
        )

    # /**
    #  * @dev Implements both `joinPool` and `exitPool`, based on `kind`.
    #  */
    def _joinOrExit(
        self,
        kind,
        poolId,
        sender,
        recipient,
        change
    ):
        # This def uses a large number of stack variables (poolId, sender and recipient, balances, amounts, fees,
        # etc.), which leads to 'stack too deep' issues. It relies on private defs with seemingly arbitrary
        # interfaces to work around this limitation.
        sp.verify(sp.len(change.assets) == sp.len(change.limits))

        # We first check that the caller passed the Pool's registered tokens in the correct order, and retrieve the
        # current balance for each.
        tokens = change.assets
        balances = self._validateTokensAndGetBalances(poolId, tokens)

        # The bulk of the work is done here: the corresponding Pool hook is called, its final balances are computed,
        # assets are transferred, and fees are paid.
        (
            finalBalances,
            amountsInOrOut,
            paidProtocolSwapFeeAmounts
        ) = self._callPoolBalanceChange(kind, poolId, sender, recipient, change, balances)

        # All that remains is storing the new Pool balances.
        specialization = self._getPoolSpecialization(poolId)
        with sp.if_(specialization == sp.nat(2)):
            self._setTwoTokenPoolCashBalances(
                poolId, tokens[0], finalBalances[0], tokens[1], finalBalances[1])

        with sp.if_(specialization == sp.nat(1)):
            self._setMinimalSwapInfoPoolBalances(poolId, tokens, finalBalances)

        with sp.if_((specialization != sp.nat(2)) & (specialization != sp.nat(1))):
            # PoolSpecialization.GENERAL
            self._setGeneralPoolBalances(poolId, finalBalances)

        # Amounts in are positive, out are negative
        positive = kind == 1

        PoolBalanceChanged = sp.record(
            poolId=poolId,
            sender=sender,
            tokens=tokens,
            amountsInOrOut=amountsInOrOut,
            paidProtocolSwapFeeAmounts=paidProtocolSwapFeeAmounts,
        )
        sp.emit(PoolBalanceChanged, tag='PoolBalanceChanged', with_type=True)
