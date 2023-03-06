import smartpy as sp

from contracts.vault.Swaps import Swaps

from contracts.pool_utils.BaseMinimalSwapInfoPool import Types as BMSIPTypes


class MockPool(sp.Contract):
    def __init__(self):
        sp.Contract.__init__(self)

    @sp.onchain_view()
    def onSwap(self, params):
        sp.set_type(params, BMSIPTypes.t_onSwap_params)
        sp.result(sp.nat(1000000000000000000))


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

    swapParams = sp.record(
        poolId=poolId,
        # tokenInBalance=sp.record(
        #     cash=sp.nat(1000000000000000000),
        #     managed=sp.nat(0),
        #     lastChangeBlock=sp.nat(135789)
        # ),
        # tokenOutBalance=sp.record(
        #     cash=sp.nat(1000000000000000000),
        #     managed=sp.nat(0),
        #     lastChangeBlock=sp.nat(135788)
        # ),
        request=sp.record(
            kind='GIVEN_IN',
            tokenIn=sp.record(
                address=sp.address('tz1'),
                id=sp.nat(0),
                FA2=False,
            ),
            tokenOut=sp.record(
                address=sp.address('tz1'),
                id=sp.nat(1),
                FA2=False,
            ),
            amount=sp.nat(12384759483945037),
        )
    )

    c.swap(swapParams)

    # swapParams2 = sp.record(
    #     poolId=poolId,
    #     # tokenInBalance=sp.record(
    #     #     cash=sp.nat(1000000000000000000),
    #     #     managed=sp.nat(0),
    #     #     lastChangeBlock=sp.nat(135789)
    #     # ),
    #     # tokenOutBalance=sp.record(
    #     #     cash=sp.nat(1000000000000000000),
    #     #     managed=sp.nat(0),
    #     #     lastChangeBlock=sp.nat(135788)
    #     # ),
    #     request=sp.record(
    #         kind='GIVEN_OUT',
    #         tokenIn=sp.record(
    #             address=sp.address('tz1'),
    #             id=sp.nat(0),
    #             FA2=False,
    #         ),
    #         tokenOut=sp.record(
    #             address=sp.address('tz1'),
    #             id=sp.nat(1),
    #             FA2=False,
    #         ),
    #         amount=sp.nat(12384759483945037),
    #     )
    # )

    # c.swap(swapParams2)
