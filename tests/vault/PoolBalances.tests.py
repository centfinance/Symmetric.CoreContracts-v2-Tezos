import smartpy as sp

from contracts.vault.PoolBalances import PoolBalances

from contracts.pool_utils.BasePool import IBasePool

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


class MockPool(sp.Contract):
    def __init__(self):
        sp.Contract.__init__(self)

    @sp.onchain_view()
    def beforeJoinPool(self, params):
        sp.set_type(params, IBasePool.t_before_join_pool_params)
        sp.result((sp.nat(0), sp.map(l={
            0: sp.nat(1000000000000000000),
            1: sp.nat(1000000000000000000),
        }, tkey=sp.TNat, tvalue=sp.TNat)))

    @sp.entry_point
    def onJoinPool(self, params):
        sp.set_type(params, IBasePool.t_on_join_pool_params)
        pass

    @sp.onchain_view()
    def beforeExitPool(self, params):
        sp.set_type(params, IBasePool.t_before_exit_pool_params)
        sp.result((sp.nat(0), sp.map(l={
            0: sp.nat(1000000000000000000),
            1: sp.nat(1000000000000000000),
        }, tkey=sp.TNat, tvalue=sp.TNat)))

    @sp.entry_point
    def onExitPool(self, params):
        sp.set_type(params, IBasePool.t_on_exit_pool_params)
        pass


class MockVault(sp.Contract, PoolBalances):
    def __init__(self):
        sp.Contract.__init__(self)
        PoolBalances.__init__(self)

    def registerPoolTokens(self, params):
        self._registerMinimalSwapInfoPoolTokens(params)


@sp.add_test(name="PoolBalancesTest_1", profile=True)
def test():

    def _toPoolId(pool, specialization, nonce):
        pack = sp.record(
            nonce=nonce,
            pool=pool,
            specialization=specialization
        )
        return sp.pack(pack)

    sc = sp.test_scenario()

    pool = MockPool()
    sc += pool

    c = MockVault()
    sc += c

    poolId = _toPoolId(
        pool.address,
        sp.nat(1),
        sp.nat(1),
    )
    amountsIn = {
        0: sp.nat(1000000000000000000),
        1: sp.nat(1000000000000000000),
    }
    userData = sp.record(
        kind='INIT',
        amountsIn=sp.some(amountsIn),
        minSPTAmountOut=sp.none,
        tokenIndex=sp.none,
        sptAmountOut=sp.none,
        allT=sp.none,
    )

    assets = {
        0: sp.record(
            address=sp.address('tz1'),
            id=sp.nat(0),
            FA2=False,
        ),
        1: sp.record(
            address=sp.address('tz1'),
            id=sp.nat(1),
            FA2=True,
        ),
    }

    limits = {
        0: 100000000000000000000,
        1: 100000000000000000000,
    }

    request = sp.record(
        userData=userData,
        assets=assets,
        limits=limits,
        useInternalBalance=False,
    )
    sender = sp.test_account('sender').address
    recipient = sender

    c.registerPool(sp.nat(1)).run(sender=pool.address)

    assetManagers = [
        sp.address('tz100000000000000000000000000000000000000')] * 2

    c.registerTokens(sp.record(
        poolId=poolId,
        tokens=assets,
        assetManagers=assetManagers
    ))

    c.joinPool(
        sp.record(
            poolId=poolId,
            sender=sender,
            recipient=recipient,
            request=request,
        )
    )

    exitUserData = sp.record(
        kind='INIT',
        amountsOut=sp.some(amountsIn),
        maxSPTAmountIn=sp.none,
        tokenIndex=sp.none,
        sptAmountIn=sp.none,
        recoveryModeExit=False,
    )

    exitRequest = sp.record(
        userData=exitUserData,
        assets=assets,
        limits=limits,
        useInternalBalance=False,
    )

    c.exitPool(
        sp.record(
            poolId=poolId,
            sender=sender,
            recipient=recipient,
            request=exitRequest,
        )
    )
