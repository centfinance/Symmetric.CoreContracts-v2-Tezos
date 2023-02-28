import smartpy as sp

from contracts.vault.PoolBalances import PoolBalances


class MockVault(sp.Contract, PoolBalances):
    def __init__(self):
        sp.Contract.__init__(self)
        PoolBalances.__init__(self)


@sp.add_test(name="PoolBalancesTest_1", profile=True)
def test():
    sc = sp.test_scenario()

    c = MockVault()

    sc += c
