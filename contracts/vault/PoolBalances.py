import smartpy as sp


from contracts.vault.PoolTokens import PoolTokens

from contracts.vault.AssetTransfersHandler import AssetTransfersHandler

import contracts.utils.helpers.InputHelpers as InputHelpers

import contracts.interfaces.SymmetricErrors as Errors

import contracts.vault.balances.BalanceAllocation as BalanceAllocation


class Types:
    TOKEN = sp.TRecord(
        address=sp.TAddress,
        id=sp.TNat,
        FA2=sp.TBool,
    )

    t_joinUserData = sp.TRecord(
        kind=sp.TString,
        amountsIn=sp.TMap(sp.TNat, sp.TNat),
        minSPTAmountOut=sp.TOption(sp.TNat),
        tokenIndex=sp.TOption(sp.TNat),
        sptAmountOut=sp.TOption(sp.TNat),
        allT=sp.TOption(sp.TNat),
    )

    t_exitUserData = sp.TRecord(
        kind=sp.TString,
        amountsOut=sp.TMap(sp.TNat, sp.TNat),
        maxSPTAmountIn=sp.TOption(sp.TNat),
        tokenIndex=sp.TOption(sp.TNat),
        sptAmountIn=sp.TOption(sp.TNat),
        allT=sp.TOption(sp.TNat),
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


class PoolBalances(
    PoolTokens,
):
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
        balances = self._validateTokensAndGetBalances(
            sp.record(
                poolId=poolId,
                expectedTokens=request.assets,
                limits=request.limits,
            ))

        (totalBalances,  lastChangeBlock) = BalanceAllocation.totalsAndLastChangeBlock(
            balances)

        pool = self._getPoolAddress(poolId)

        params = sp.record(
            poolId=poolId,
            sender=sender,
            recipient=recipient,
            balances=totalBalances,
            lastChangeBlock=lastChangeBlock,
            protocolSwapFeePercentage=sp.nat(0),
            # protocolSwapFeePercentage=self.data.swapFeePercentage,
            userData=request.userData,
        )
        # Call BasePool view to get amounts
        pair = sp.view('beforeJoinPool', pool,
                       params, t=sp.TPair(sp.TNat, sp.TMap(sp.TNat, sp.TNat))).open_some("Invalid view")
        # Call BasePool entry point to perform join
        onJoinPool = sp.contract(Types.t_onJoinPool_params, pool, "onJoinPool").open_some(
            "INTERFACE_MISMATCH")

        sp.transfer(params, sp.tez(0), onJoinPool)

        amountsIn = sp.snd(pair)

        sp.verify(sp.len(balances) == sp.len(amountsIn))
        #  The Vault ignores the `recipient` in joins and the `sender` in exits: it is up to the Pool to keep track of
        #  their participation.
        finalBalances = self._processJoinPoolTransfers(
            sender, request, balances, amountsIn)

        self._setMinimalSwapInfoPoolBalances(
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
        balances = self._validateTokensAndGetBalances(
            sp.record(
                poolId=poolId,
                expectedTokens=request.assets,
                limits=request.limits,
            ))

        (totalBalances,  lastChangeBlock) = BalanceAllocation.totalsAndLastChangeBlock(
            balances)

        pool = self._getPoolAddress(poolId)

        params = sp.record(
            poolId=poolId,
            sender=sender,
            recipient=recipient,
            balances=totalBalances,
            lastChangeBlock=lastChangeBlock,
            protocolSwapFeePercentage=sp.nat(0),
            # protocolSwapFeePercentage=self.data.swapFeePercentage,
            userData=request.userData,
        )
        # Call BasePool view to get amounts
        pair = sp.view('beforeExitPool', pool,
                       params, t=sp.TPair(sp.TNat, sp.TMap(sp.TNat, sp.TNat))).open_some("Invalid view")
        # Call BasePool entry point to perform join
        onExitPool = sp.contract(Types.t_onExitPool_params, pool, "onExitPool").open_some(
            "INTERFACE_MISMATCH")

        sp.transfer(params, sp.tez(0), onExitPool)

        amountsOut = sp.snd(pair)

        sp.verify(sp.len(balances) == sp.len(amountsOut))
        #  The Vault ignores the `recipient` in joins and the `sender` in exits: it is up to the Pool to keep track of
        #  their participation.
        finalBalances = self._processExitPoolTransfers(
            sender, request, balances, amountsOut)

        self._setMinimalSwapInfoPoolBalances(
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
       #  wrappedXtz = sp.compute(0)

        joinBalances = sp.compute(sp.map(l={}, tkey=sp.TNat, tvalue=sp.TRecord(
            cash=sp.TNat,
            managed=sp.TNat,
            lastChangeBlock=sp.TNat,
        )))
        with sp.for_('i', sp.range(0, sp.len(change.assets))) as i:
            amountIn = amountsIn[i]
            sp.verify(amountIn <= change.limits[i], Errors.JOIN_ABOVE_MAX)

            # Receive assets from the sender - possibly from Internal Balance.
            asset = change.assets[i]
            AssetTransfersHandler._receiveAsset(asset, amountIn, sender,
                                                change.useInternalBalance)
            # TODO: Handle Native Tez
            # with sp.if_(self._isXTZ(asset)):
            #     wrappedXtz = wrappedXtz.add(amountIn)

            updated_balance = sp.record(
                cash=(balances[i].cash + amountIn),
                managed=balances[i].managed,
                lastChangeBlock=balances[i].lastChangeBlock,
            )

            joinBalances[i] = updated_balance

        # TODO: Handle Native Tez
        # self._handleRemainingXtz(wrappedXtz)

        return joinBalances

    def _processExitPoolTransfers(
        self,
        recipient,
        change,
        balances,
        amountsOut,
    ):
        exitBalances = sp.compute(sp.map(l={}, tkey=sp.TNat, tvalue=sp.TRecord(
            cash=sp.TNat,
            managed=sp.TNat,
            lastChangeBlock=sp.TNat,
        )))
        with sp.for_('i', sp.range(0, sp.len(change.assets))) as i:
            amountOut = amountsOut[i]
            sp.verify(amountOut <= change.limits[i], Errors.EXIT_BELOW_MIN)

            asset = change.assets[i]
            AssetTransfersHandler._sendAsset(asset, amountOut, recipient,
                                             change.useInternalBalance)

            updated_balance = sp.record(
                cash=sp.as_nat(balances[i].cash - amountOut),
                managed=balances[i].managed,
                lastChangeBlock=balances[i].lastChangeBlock,
            )

            exitBalances[i] = updated_balance

        return exitBalances

    @sp.private_lambda(with_storage='read-only', wrap_call=True)
    def _validateTokensAndGetBalances(self, params):
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
        signedValues = sp.compute(sp.map({}))
        with sp.for_('i', sp.range(0, sp.len(params.amounts))) as i:
            with sp.if_(params.positive):
                signedValues[i] = sp.to_int(params.amounts[i])
            with sp.else_():
                signedValues[i] = - sp.to_int(params.amounts[i])

        sp.result(signedValues)
