import smartpy as sp


from contracts.vault.PoolTokens import PoolTokens

import contracts.utils.helpers.InputHelpers as InputHelpers

import contracts.interfaces.SymmetricErrors as Errors

import contracts.vault.balances.BalanceAllocation as BalanceAllocation


class PoolBalances(
    PoolTokens,
):
    def __init__(self):
        PoolTokens.__init__(self)

    @sp.entry_point
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

    @sp.entry_point
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
    @sp.private_lambda(with_storage="read-write", with_operations=True)
    def _joinOrExit(
        self,
        params,
    ):
        # This def uses a large number of stack variables (poolId, sender and recipient, balances, amounts, fees,
        # etc.), which leads to 'stack too deep' issues. It relies on private defs with seemingly arbitrary
        # interfaces to work around this limitation.
        sp.verify(sp.len(params.change.assets) == sp.len(params.change.limits))

        # We first check that the caller passed the Pool's registered tokens in the correct order, and retrieve the
        # current balance for each.
        tokens = params.change.assets
        balances = self._validateTokensAndGetBalances(params.poolId, tokens)

        # The bulk of the work is done here: the corresponding Pool hook is called, its final balances are computed,
        # assets are transferred, and fees are paid.
        (
            finalBalances,
            amountsInOrOut,
            paidProtocolSwapFeeAmounts
        ) = self._callPoolBalanceChange(params.kind, params.poolId, params.sender, params.recipient, params.change, balances)

        # All that remains is storing the new Pool balances.
        specialization = self._getSpecialization(params.poolId)
        with sp.if_(specialization == sp.nat(2)):
            self._setTwoTokenPoolCashBalances(
                params.poolId, tokens[0], finalBalances[0], tokens[1], finalBalances[1])

        with sp.if_(specialization == sp.nat(1)):
            self._setMinimalSwapInfoPoolBalances(
                params.poolId, tokens, finalBalances)

        with sp.if_((specialization != sp.nat(2)) & (specialization != sp.nat(1))):
            # PoolSpecialization.GENERAL
            self._setGeneralPoolBalances(params.poolId, finalBalances)

        # Amounts in are positive, out are negative
        positive = params.kind == 1

        PoolBalanceChanged = sp.record(
            poolId=params.poolId,
            sender=params.sender,
            tokens=tokens,
            amountsInOrOut=amountsInOrOut,
            paidProtocolSwapFeeAmounts=paidProtocolSwapFeeAmounts,
        )
        sp.emit(PoolBalanceChanged, tag='PoolBalanceChanged', with_type=True)

    # /**
    #  * @dev Calls the corresponding Pool hook to get the amounts in/out plus protocol fee amounts, and performs the
    #  * associated token transfers and fee payments, returning the Pool's final balances.
    #  */
    def _callPoolBalanceChange(
        self,
        kind,
        poolId,
        sender,
        recipient,
        change,
        balances
    ):

        (totalBalances,  lastChangeBlock) = BalanceAllocation.totalsAndLastChangeBlock(
            balances)

        pool = self._getPoolAddress(poolId)

        amountsInOrOut = sp.local('amountInOrOut', 0)
        params = sp.record(
            poolId=poolId,
            sender=sender,
            recipient=recipient,
            balances=totalBalances,
            lastChangeBlock=lastChangeBlock,
            protocolSwapFeePercentage=self.data.swapFeePercentage,
            userData=change.userData,
        )
        with sp.if_(kind == 1):

            # Calll BasePool view to get amounts
            (sptAmountIn, amountsOut) = sp.view('beforeJoinPool', pool,
                                                params, t=sp.TPair(sp.TNat, sp.TMap(sp.TNat, sp.TNat)))
            # Call BasePool entry point to perform join
            onJoinPool = sp.contract(sp.TNat, pool, "onJoinPool").open_some(
                "INTERFACE_MISMATCH")
            sp.transfer(params, sp.tez(0), onJoinPool)
            amountsInOrOut.value = amountsIn
        with sp.else_():
            (sptAmountOut, amountsIn) = sp.view('beforeJoinPool', pool,
                                                params, t=sp.TPair(sp.TNat, sp.TMap(sp.TNat, sp.TNat)))

            pool.onExitPool()
            amountsInOrOut.value = amountsOut

        InputHelpers.ensureInputLengthMatch(
            sp.len(balances), sp.len(amountsInOrOut))
        # // The Vault ignores the `recipient` in joins and the `sender` in exits: it is up to the Pool to keep track of
        # // their participation.
        finalBalances = sp.compute({})
        with sp.if_(kind == 1):
            finalBalances = self._processJoinPoolTransfers(
                sender, change, balances, amountsInOrOut)
        with sp.else_():
            finalBalances = self._processExitPoolTransfers(
                recipient, change, balances, amountsInOrOut)

        return (finalBalances, amountsInOrOut)

    def _processJoinPoolTransfers(
        self,
        sender,
        change,
        balances,
        amountsIn,
    ):
        # // We need to track how much of the received ETH was used and wrapped into WETH to return any excess.
        wrappedEth = 0

        finalBalances = sp.compute(sp.map({}, sp.TNat, sp.TBytes))
        with sp.for_('i', sp.range(0, sp.len(change.assets))) as i:
            amountIn = amountsIn[i]
            sp.verify(amountIn <= change.limits[i], Errors.JOIN_ABOVE_MAX)

            # // Receive assets from the sender - possibly from Internal Balance.
            asset = change.assets[i]
            self._receiveAsset(asset, amountIn, sender,
                               change.useInternalBalance)

            with sp.if_(self._isETH(asset)):
                wrappedEth = wrappedEth.add(amountIn)

            finalBalances[i] = balances[i].increaseCash(amountIn)

        # // Handle any used and remaining ETH.
        self._handleRemainingEth(wrappedEth)

        return finalBalances

    def _processExitPoolTransfers(
        self,
        recipient,
        change,
        balances,
        amountsOut,
    ):
        finalBalances = sp.compute(sp.map({}, sp.TNat, sp.TBytes))
        with sp.for_('i', sp.range(0, sp.len(change.assets))) as i:
            amountOut = amountsOut[i]
            sp.verify(amountOut <= change.limits[i], Errors.EXIT_BELOW_MIN)

            asset = change.assets[i]
            self._sendAsset(asset, amountOut, recipient,
                            change.useInternalBalance)

            finalBalances[i] = balances[i].decreaseCash(
                amountOut)

        return finalBalances

    def _validateTokensAndGetBalances(self, poolId, expectedTokens):
        (actualTokens, balances) = self._getPoolTokens(poolId)
        InputHelpers.ensureInputLengthMatch(
            sp.len(actualTokens), sp.len(expectedTokens))
        sp.verify(actualTokens.length > 0, Errors.POOL_NO_TOKENS)

        with sp.for_('i', sp.range(0, sp.len(actualTokens))) as i:
            sp.verify(actualTokens[i] ==
                      expectedTokens[i], Errors.TOKENS_MISMATCH)

        return balances
