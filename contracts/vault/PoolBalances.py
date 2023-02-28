import smartpy as sp


from contracts.vault.PoolTokens import PoolTokens

import contracts.utils.helpers.InputHelpers as InputHelpers

import contracts.interfaces.SymmetricErrors as Errors

import contracts.vault.balances.BalanceAllocation as BalanceAllocation


class Types:
    TOKEN = sp.TRecord(
        address=sp.TAddress,
        id=sp.TNat,
    )

    t_joinUserData = sp.TRecord(
        kind=sp.TString,
        amountsIn=sp.TMap(sp.TNat, sp.TNat),
        minSPTAmountOut=sp.TNat,
        tokenIndex=sp.TNat,
        sptAmountOut=sp.TNat,
        allT=sp.TNat,
    )

    t_exitUserData = sp.TRecord(
        kind=sp.TString,
        amountsOut=sp.TMap(sp.TNat, sp.TNat),
        maxSPTAmountIn=sp.TNat,
        tokenIndex=sp.TNat,
        sptAmountIn=sp.TNat,
        allT=sp.TNat,
    )

    t_onJoinPool_params = sp.TRecord(
        poolId=sp.TBytes,
        sender=sp.TAddress,
        recipient=sp.TAddress,
        balances=sp.TMap(sp.TNat, sp.TNat),
        lastChangeBlock=sp.TNat,
        protocolSwapFeePercentage=sp.TNat,
        userData=t_joinUserData,
    )

    t_onExitPool_params = sp.TRecord(
        poolId=sp.TBytes,
        sender=sp.TAddress,
        recipient=sp.TAddress,
        balances=sp.TMap(sp.TNat, sp.TNat),
        lastChangeBlock=sp.TNat,
        protocolSwapFeePercentage=sp.TNat,
        userData=t_exitUserData,
    )

    t_joinPool_request = sp.TRecord(
        userData=t_joinUserData,
        assets=sp.TMap(sp.TNat, TOKEN),
        limits=sp.TMap(sp.TNat, sp.TNat),
        useInternalBalance=sp.TBool,
    )

    t_joinPool_params = sp.TRecord(
        poolId=sp.TBytes,
        sender=sp.TAddress,
        recipient=sp.TAddress,
        request=t_joinPool_request
    )

    t_exitPool_request = sp.TRecord(
        userData=t_exitUserData,
        assets=sp.TMap(sp.TNat, TOKEN),
        limits=sp.TMap(sp.TNat, sp.TNat),
        useInternalBalance=sp.TBool,
    )

    t_exitPool_params = sp.TRecord(
        poolId=sp.TBytes,
        sender=sp.TAddress,
        recipient=sp.TAddress,
        request=t_exitPool_request
    )

    userData_type = sp.TVariant(
        joinPool=t_joinUserData,
        exitPool=t_exitUserData,
    )

    t_request = sp.TRecord(
        userData=userData_type,
        assets=sp.TMap(sp.TNat, TOKEN),
        limits=sp.TMap(sp.TNat, sp.TNat),
        useInternalBalance=sp.TBool,
    )

    t_joinOrExitPool_params = sp.TRecord(
        poolId=sp.TBytes,
        sender=sp.TAddress,
        recipient=sp.TAddress,
        request=t_request
    )


class PoolBalances(
    PoolTokens,
):
    def __init__(self):
        PoolTokens.__init__(self)

    @sp.entry_point(parameter_type=Types.t_joinOrExitPool_params)
    def joinPool(
        self,
        poolId,
        sender,
        recipient,
        request
    ):
        self._joinOrExit(
            sp.record(
                kind=0,
                poolId=poolId,
                sender=sender,
                recipient=recipient,
                change=request,
            ))

    @sp.entry_point(parameter_type=Types.t_joinOrExitPool_params)
    def exitPool(
        self,
        poolId,
        sender,
        recipient,
        request
    ):
        self._joinOrExit(
            sp.record(
                kind=0,
                poolId=poolId,
                sender=sender,
                recipient=recipient,
                change=request,
            ))

    # /**
    #  * @dev Implements both `joinPool` and `exitPool`, based on `kind`.
    #  */
    @sp.private_lambda(with_storage="read-write", with_operations=True)
    def _joinOrExit(
        self,
        params,
    ):
        sp.set_type(params.change.assets, sp.TMap(sp.TNat, Types.TOKEN))
        sp.set_type(params.change.limits, sp.TMap(sp.TNat, sp.TNat))
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
        ) = self._callPoolBalanceChange(params.kind, params.poolId, params.sender, params.recipient, params.change, balances)

        # All that remains is storing the new Pool balances.
        specialization = self._getSpecialization(params.poolId)
        # with sp.if_(specialization == sp.nat(2)):
        #     self._setTwoTokenPoolCashBalances(
        #         params.poolId, tokens[0], finalBalances[0], tokens[1], finalBalances[1])

        with sp.if_(specialization == sp.nat(1)):
            self._setMinimalSwapInfoPoolBalances(
                sp.record(
                    poolId=params.poolId,
                    tokens=tokens,
                    balances=finalBalances,
                ))

        # with sp.if_((specialization != sp.nat(2)) & (specialization != sp.nat(1))):
        #     # PoolSpecialization.GENERAL
        #     self._setGeneralPoolBalances(params.poolId, finalBalances)

        # Amounts in are positive, out are negative
        # positive = params.kind == 1

        # PoolBalanceChanged = sp.record(
        #     poolId=params.poolId,
        #     sender=params.sender,
        #     tokens=tokens,
        #     amountsInOrOut=amountsInOrOut,
        #     paidProtocolSwapFeeAmounts=paidProtocolSwapFeeAmounts,
        # )
        # sp.emit(PoolBalanceChanged, tag='PoolBalanceChanged', with_type=True)

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
        amountsInOrOut = sp.compute(sp.map(l={}, tkey=sp.TNat, tvalue=sp.TNat))

        with sp.if_(kind == 1):
            params = sp.record(
                poolId=poolId,
                sender=sender,
                recipient=recipient,
                balances=totalBalances,
                lastChangeBlock=lastChangeBlock,
                protocolSwapFeePercentage=0,
                # protocolSwapFeePercentage=self.data.swapFeePercentage,
                userData=change.userData.open_variant('joinPool'),
            )
            # Calll BasePool view to get amounts
            pair = sp.view('beforeJoinPool', pool,
                           params, t=sp.TPair(sp.TNat, sp.TMap(sp.TNat, sp.TNat))).open_some("Invalid view")
            # Call BasePool entry point to perform join
            onJoinPool = sp.contract(Types.t_onJoinPool_params, pool, "onJoinPool").open_some(
                "INTERFACE_MISMATCH")
            sp.transfer(params, sp.tez(0), onJoinPool)
            amountsInOrOut = sp.snd(pair)
        with sp.else_():
            params = sp.record(
                poolId=poolId,
                sender=sender,
                recipient=recipient,
                balances=totalBalances,
                lastChangeBlock=lastChangeBlock,
                protocolSwapFeePercentage=0,
                # protocolSwapFeePercentage=self.data.swapFeePercentage,
                userData=change.userData.open_variant('exitPool'),
            )
            pair = sp.view('beforeExitPool', pool,
                           params, t=sp.TPair(sp.TNat, sp.TMap(sp.TNat, sp.TNat))).open_some("Invalid view")

            onExitPool = sp.contract(Types.t_onExitPool_params, pool, "onExitPool").open_some(
                "INTERFACE_MISMATCH")
            sp.transfer(params, sp.tez(0), onExitPool)
            amountsInOrOut = sp.snd(pair)

        sp.verify(sp.len(balances) == sp.len(amountsInOrOut))
        #  The Vault ignores the `recipient` in joins and the `sender` in exits: it is up to the Pool to keep track of
        #  their participation.
        finalBalances = sp.local('finalBalances', {})
        with sp.if_(kind == 1):
            finalBalances.value = self._processJoinPoolTransfers(
                sender, change, balances, amountsInOrOut)
        # with sp.else_():
        #     finalBalances = self._processExitPoolTransfers(
        #         recipient, change, balances, amountsInOrOut)

        return (finalBalances.value, amountsInOrOut)

    def _processJoinPoolTransfers(
        self,
        sender,
        change,
        balances,
        amountsIn,
    ):
        # // We need to track how much of the received ETH was used and wrapped into WETH to return any excess.
        wrappedXtz = sp.compute(0)

        newBalances = sp.compute(sp.map(l={}, tkey=sp.TNat, tvalue=sp.TRecord(
            cash=sp.TNat,
            managed=sp.TNat,
            lastChangeBlock=sp.TNat,
        )))
        with sp.for_('i', sp.range(0, sp.len(change.assets))) as i:
            amountIn = amountsIn[i]
            sp.verify(amountIn <= change.limits[i], Errors.JOIN_ABOVE_MAX)

            # // Receive assets from the sender - possibly from Internal Balance.
            # asset = change.assets[i]
            # self._receiveAsset(asset, amountIn, sender,
            #                    change.useInternalBalance)

            # with sp.if_(self._isXTZ(asset)):
            #     wrappedXtz = wrappedXtz.add(amountIn)
            updated_balance = sp.record(
                cash=(balances[i].cash + amountIn),
                managed=balances[i].managed,
                lastChangeBlock=balances[i].lastChangeBlock,
            )

            newBalances[i] = updated_balance

        # // Handle any used and remaining ETH.
        # self._handleRemainingXtz(wrappedXtz)

        return newBalances

    # def _processExitPoolTransfers(
    #     self,
    #     recipient,
    #     change,
    #     balances,
    #     amountsOut,
    # ):
    #     finalBalances = sp.compute(sp.map({}, sp.TNat, sp.TNat))
    #     with sp.for_('i', sp.range(0, sp.len(change.assets))) as i:
    #         amountOut = amountsOut[i]
    #         sp.verify(amountOut <= change.limits[i], Errors.EXIT_BELOW_MIN)

    #         asset = change.assets[i]
    #         self._sendAsset(asset, amountOut, recipient,
    #                         change.useInternalBalance)

    #         finalBalances[i] = balances[i].decreaseCash(
    #             amountOut)

    #     return finalBalances

    def _validateTokensAndGetBalances(self, poolId, expectedTokens):
        (actualTokens, balances) = self._getPoolTokens(poolId)
        sp.verify(sp.len(actualTokens) == sp.len(expectedTokens))
        sp.verify(sp.len(actualTokens) > 0, Errors.POOL_NO_TOKENS)

        with sp.for_('i', sp.range(0, sp.len(actualTokens))) as i:
            sp.verify(actualTokens[i] ==
                      expectedTokens[i], Errors.TOKENS_MISMATCH)

        return balances
