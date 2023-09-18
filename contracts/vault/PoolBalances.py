import smartpy as sp


from contracts.vault.PoolTokens import PoolTokens

from contracts.vault.AssetTransfersHandler import AssetTransfersHandler

from contracts.pool_utils.BasePool import IBasePool

import contracts.utils.helpers.InputHelpers as InputHelpers

import contracts.interfaces.SymmetricErrors as Errors

import contracts.vault.balances.BalanceAllocation as BalanceAllocation


class Types:
    TOKEN = sp.TPair(sp.TAddress, sp.TOption(sp.TNat))

    t_joinPool_request = sp.TRecord(
        userData=IBasePool.JOIN_USER_DATA,
        assets=sp.TMap(sp.TNat, TOKEN),
        limits=sp.TMap(sp.TNat, sp.TNat),
    )

    t_joinPool_params = sp.TRecord(
        poolId=sp.TPair(sp.TAddress, sp.TNat),
        sender=sp.TAddress,
        recipient=sp.TAddress,
        request=t_joinPool_request
    )

    t_exitPool_request = sp.TRecord(
        userData=IBasePool.EXIT_USER_DATA,
        assets=sp.TMap(sp.TNat, TOKEN),
        limits=sp.TMap(sp.TNat, sp.TNat),
    )

    t_exitPool_params = sp.TRecord(
        poolId=sp.TPair(sp.TAddress, sp.TNat),
        sender=sp.TAddress,
        recipient=sp.TAddress,
        request=t_exitPool_request
    )


class PoolBalances(
    PoolTokens,
):
    """
    Stores the Asset Managers (by Pool and token), and implements the top level Asset Manager and Pool interfaces,
    such as registering and deregistering tokens, joining and exiting Pools, and informational functions like `getPool`
    and `getPoolTokens`.
    """
    def __init__(self):
        PoolTokens.__init__(self)

    @sp.entry_point(parameter_type=Types.t_joinPool_params)
    def joinPool(
        self,
        poolId,
        sender,
        recipient,
        request
    ):
        """
        Allows a user to join the pool.

        Parameters:
            poolId (TPair(TAddress, TNat)): Identifier for the pool.
            sender (TAddress): Address of the user sending the request.
            recipient (TAddress): Address to receive the resulting tokens.
            request (t_joinPool_request): Contains user data, assets, and limits for the join operation.

        Notes:
            - Only non-paused pools are accessible.
            - The sender should match the source of the request.
            - The pool specified by poolId should be registered.
            - Calls to this function might update the pool balances and emit a 'PoolBalanceChanged' event.

        """
        self.onlyUnpaused()
        sp.verify(sender == sp.source, Errors.SENDER_NOT_ALLOWED)
        self._ensureRegisteredPool(poolId)
        
        balances = self._validateTokensAndGetBalances(
            sp.record(
                poolId=poolId,
                expectedTokens=request.assets,
                limits=request.limits,
            ))

        totalBalances = BalanceAllocation.totals(balances)
        pool = sp.fst(poolId)

        # Call BasePool view to get amounts
        t = sp.compute(sp.view('beforeJoinPool', pool,
                               sp.record(balances=totalBalances, userData=request.userData), t=sp.TTuple(sp.TNat, sp.TMap(sp.TNat, sp.TNat), sp.TNat)).open_some(Errors.BEFORE_JOIN_POOL_INVALID))
        sptAmountOut, amountsIn, invariant = sp.match_tuple(
            t, 'sptAmountOut', 'amountsIn', 'invariant')
        params = sp.record(
            poolId=poolId,
            recipient=recipient,
            amountsIn=amountsIn,
            sptAmountOut=sptAmountOut,
            invariant=invariant,
            balances=totalBalances,
        )
        # Call BasePool entry point to perform join
        onJoinPool = sp.contract(IBasePool.t_after_join_pool_params, pool, "afterJoinPool").open_some(
            "INTERFACE_MISMATCH")

        sp.transfer(params, sp.tez(0), onJoinPool)

        sp.verify(sp.len(balances) == sp.len(amountsIn))
        #  The Vault ignores the `recipient` in joins and the `sender` in exits: it is up to the Pool to keep track of
        #  their participation.
        finalBalances = self._processJoinPoolTransfers(
            sender, request, balances, amountsIn)

        self._setPoolBalances(
            sp.record(
                poolId=poolId,
                tokens=request.assets,
                balances=finalBalances,
            ))

        PoolBalanceChanged = sp.record(
            poolId=poolId,
            sender=sender,
            tokens=request.assets,
            amountsInOrOut=self._castToInt(
                sp.record(amounts=amountsIn, positive=True)),
        )
        sp.emit(PoolBalanceChanged, tag='PoolBalanceChanged', with_type=True)

    @sp.entry_point(parameter_type=Types.t_exitPool_params)
    def exitPool(
        self,
        poolId,
        sender,
        recipient,
        request
    ):
        """
        Allows a user to exit the pool.

        Parameters:
            poolId (TPair(TAddress, TNat)): Identifier for the pool.
            sender (TAddress): Address of the user sending the request.
            recipient (TAddress): Address to receive the resulting tokens.
            request (t_exitPool_request): Contains user data, assets, and limits for the exit operation.

        Notes:
            - Only non-paused pools are accessible.
            - The sender should match the source of the request.
            - The pool specified by poolId should be registered.
            - Calls to this function might update the pool balances and emit a 'PoolBalanceChanged' event.

        """
        self.onlyUnpaused()
        sp.verify(sender == sp.source, Errors.SENDER_NOT_ALLOWED )
        self._ensureRegisteredPool(poolId)
        balances = self._validateTokensAndGetBalances(
            sp.record(
                poolId=poolId,
                expectedTokens=request.assets,
                limits=request.limits,
            ))

        totalBalances = BalanceAllocation.totals(balances)

        pool = sp.fst(poolId)

        # Call BasePool view to get amounts
        t = sp.compute(sp.view('beforeExitPool', pool,
                               sp.record(balances=totalBalances, userData=request.userData), t=sp.TTuple(sp.TNat, sp.TMap(sp.TNat, sp.TNat), sp.TNat)).open_some(Errors.BEFORE_EXIT_POOL_INVALID))
        sptAmountIn, amountsOut, invariant = sp.match_tuple(
            t, 'sptAmountIn', 'amountsOut', 'invariant')

        params = sp.record(
            poolId=poolId,
            sender=sender,
            amountsOut=amountsOut,
            sptAmountIn=sptAmountIn,
            invariant=invariant,
            balances=totalBalances,
            recoveryModeExit=request.userData.recoveryModeExit,
        )
        # Call BasePool entry point to perform join
        onExitPool = sp.contract(IBasePool.t_after_exit_pool_params, pool, "afterExitPool").open_some(
            "INTERFACE_MISMATCH")
        sp.transfer(params, sp.tez(0), onExitPool)

        sp.verify(sp.len(balances) == sp.len(amountsOut))
        #  The Vault ignores the `recipient` in joins and the `sender` in exits: it is up to the Pool to keep track of
        #  their participation.
        finalBalances = self._processExitPoolTransfers(
            sender, request, balances, amountsOut)

        self._setPoolBalances(
            sp.record(
                poolId=poolId,
                tokens=request.assets,
                balances=finalBalances,
            ))

        PoolBalanceChanged = sp.record(
            poolId=poolId,
            sender=sender,
            tokens=request.assets,
            amountsInOrOut=self._castToInt(
                sp.record(amounts=amountsOut, positive=False)),
        )
        sp.emit(PoolBalanceChanged, tag='PoolBalanceChanged', with_type=True)

    def _processJoinPoolTransfers(
        self,
        sender,
        change,
        balances,
        amountsIn,
    ):
        """
        Transfers `amountsIn` from `sender`, ensuring they are within their accepted limits

        Returns:
            The Pool's final balances, which are derived from the current balances added to `amountsIn`
        """

        joinBalances = sp.compute(
            sp.map(l={}, tkey=sp.TNat, tvalue=sp.TPair(sp.TNat, sp.TNat)))
        with sp.for_('x', sp.range(0, sp.len(change.assets))) as x:
            amountIn = amountsIn[x]
            sp.verify(amountIn <= change.limits[x], Errors.JOIN_ABOVE_MAX)

            asset = change.assets[x]
            AssetTransfersHandler._receiveAsset(asset, amountIn, sender)

            joinBalances[x] = (
                (sp.fst(balances[x]) + amountIn), sp.snd(balances[x]))

        return joinBalances

    def _processExitPoolTransfers(
        self,
        recipient,
        change,
        balances,
        amountsOut,
    ):
        """
        Transfers `amountsOut` from `recipient`, ensuring they are within their accepted limits

        Returns:
            Returns the Pool's final balances, which are the current `balances` minus `amountsOut`
        """        
        exitBalances = sp.compute(
            sp.map(l={}, tkey=sp.TNat, tvalue=sp.TPair(sp.TNat, sp.TNat)))
        with sp.for_('x', sp.range(0, sp.len(change.assets))) as x:
            amountOut = amountsOut[x]
            sp.verify(amountOut >= change.limits[x], Errors.EXIT_BELOW_MIN)

            asset = change.assets[x]
            AssetTransfersHandler._sendAsset(asset, amountOut, recipient)

            exitBalances[x] = (
                (sp.as_nat(sp.fst(balances[x]) - amountOut)), sp.snd(balances[x]))

        return exitBalances

    @sp.private_lambda(with_storage='read-only', wrap_call=True)
    def _validateTokensAndGetBalances(self, params):
        """
        Returns the total balance for the given `poolId`'s `expectedTokens`.

        Parameters:
            poolId: The ID of the pool.
            expectedTokens: List of expected tokens.

        Notes:
            - `expectedTokens` must exactly match the token array returned by `getPoolTokens` in terms of length, elements, and order.
            - The Pool must have at least one registered token.

        Returns:
            A map containing the balances of the pool tokens.
        """
        sp.verify(sp.len(params.expectedTokens) == sp.len(params.limits))

        (actualTokens, balances) = self._getPoolTokens(params.poolId)
        sp.verify(sp.len(actualTokens) == sp.len(params.expectedTokens))
        sp.verify(sp.len(actualTokens) > 0, Errors.POOL_NO_TOKENS)

        with sp.for_('i', sp.range(0, sp.len(actualTokens))) as i:
            sp.verify(actualTokens[i] ==
                      params.expectedTokens[i], Errors.TOKENS_MISMATCH)

        sp.result(balances)

    @sp.private_lambda()
    def _castToInt(self, params):
        """
        Casts a map of nat values to int, setting the sign of the result based on the `positive` flag.

        Parameters:
            values (sp.Tmap[sp.TNat, sp.TNat]): List of values to be cast.
            positive (sp.TBool): Flag to determine the sign of the result.
        """
        signedValues = sp.compute(sp.map({}))
        with sp.for_('i', sp.range(0, sp.len(params.amounts))) as i:
            with sp.if_(params.positive):
                signedValues[i] = sp.to_int(params.amounts[i])
            with sp.else_():
                signedValues[i] = - sp.to_int(params.amounts[i])

        sp.result(signedValues)
