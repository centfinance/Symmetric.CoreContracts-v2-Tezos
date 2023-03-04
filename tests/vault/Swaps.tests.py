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


@sp.add_test(name="SwapsTest_1", profile=True)
def test():
    sc = sp.test_scenario()

    alice = sp.test_account('Alice')

    pool = MockPool()
    sc += pool

    c = MockVault()
    sc += c

    swapParams = sp.record(
        pool=pool.address,
        tokenInBalance=sp.record(
            cash=sp.nat(1000000000000000000),
            managed=sp.nat(0),
            lastChangeBlock=sp.nat(135789)
        ),
        tokenOutBalance=sp.record(
            cash=sp.nat(1000000000000000000),
            managed=sp.nat(0),
            lastChangeBlock=sp.nat(135788)
        ),
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
