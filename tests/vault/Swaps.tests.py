import smartpy as sp

from contracts.vault.Swaps import Swaps

from contracts.pool_utils.BaseMinimalSwapInfoPool import Types as BMSIPTypes

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
    def onSwap(self, params):
        sp.set_type(params, BMSIPTypes.t_onSwap_params)
        sp.result(sp.nat(1000000000000000000))

    @sp.onchain_view()
    def beforeJoinPool(self, params):
        sp.set_type(params, t_onJoinPool_params)
        sp.result((sp.nat(0), sp.map(l={
            0: sp.nat(1000000000000000000),
            1: sp.nat(1000000000000000000),
        }, tkey=sp.TNat, tvalue=sp.TNat)))

    @sp.entry_point
    def onJoinPool(self, params):
        sp.set_type(params, t_onJoinPool_params)
        pass

    @sp.onchain_view()
    def beforeExitPool(self, params):
        sp.set_type(params, t_onExitPool_params)
        sp.result((sp.nat(0), sp.map(l={
            0: sp.nat(1000000000000000000),
            1: sp.nat(1000000000000000000),
        }, tkey=sp.TNat, tvalue=sp.TNat)))

    @sp.entry_point
    def onExitPool(self, params):
        sp.set_type(params, t_onExitPool_params)
        pass


class MockVault(sp.Contract, Swaps):
    def __init__(self):
        sp.Contract.__init__(self)
        Swaps.__init__(self)


def _toPoolId(pool, specialization, nonce):
    pack = sp.record(
        nonce=nonce,
        pool=pool,
        specialization=specialization
    )
    return sp.pack(pack)


@sp.add_test(name="SwapsTest_1", profile=True)
def test():
    sc = sp.test_scenario()

    alice = sp.test_account('Alice')

    pool = MockPool()
    sc += pool

    c = MockVault()
    sc += c

    c.registerPool(sp.nat(1)).run(sender=pool.address)

    assets = {
        0: sp.record(
            address=sp.address('tz1'),
            id=sp.nat(0),
            FA2=False,),
        1: sp.record(
            address=sp.address('tz1'),
            id=sp.nat(1),
            FA2=False,)
    }

    limits = {
        0: 100000000000000000000,
        1: 100000000000000000000,
    }
    amountsIn = {
        0: 1000000000000000000,
        1: 1000000000000000000,
    }
    userData = sp.record(
        kind='INIT',
        amountsIn=amountsIn,
        minSPTAmountOut=sp.none,
        tokenIndex=sp.none,
        sptAmountOut=sp.none,
        allT=sp.none,
    )

    request = sp.record(
        userData=userData,
        assets=assets,
        limits=limits,
        useInternalBalance=False,
    )
    sender = sp.test_account('sender').address
    recipient = sender

    assetManagers = [
        sp.address('tz100000000000000000000000000000000000000')] * 2

    poolId = _toPoolId(
        pool.address,
        sp.nat(1),
        sp.nat(1),
    )
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

    swapParams = sp.record(
        poolId=poolId,
        request=sp.record(
            kind='GIVEN_IN',
            tokenIn=assets[0],
            tokenOut=assets[1],
            amount=sp.nat(12384759483945037),
        )
    )

    c.swap(swapParams)

    swapParams2 = sp.record(
        poolId=poolId,
        request=sp.record(
            kind='GIVEN_OUT',
            tokenIn=assets[1],
            tokenOut=assets[0],
            amount=sp.nat(12384759483945037),
        )
    )

    c.swap(swapParams2)
