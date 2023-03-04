import smartpy as sp

from contracts.vault.Swaps import Swaps


class MockPool(sp.Contract):
    def __init__(self):
        sp.Contract.__init__(self)

    @sp.entry_point
    def onSwap(self, params):
        pass


class MockVault(sp.Contract, Swaps):
    def __init__(self):
        sp.Contract.__init__(self)
        Swaps.__init__(self)


@sp.add_test(name="SwapsTest_1", profile=True)
def test():
    sc = sp.test_scenario()

    pool = MockPool()
    sc += pool

    c = MockVault()
    sc += c
