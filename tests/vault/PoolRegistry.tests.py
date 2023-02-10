import smartpy as sp

from contracts.vault.PoolRegistry import PoolRegistry


class MockVault(sp.Contract, PoolRegistry):
    def __init__(self):
        sp.Contract.__init__(self)
        PoolRegistry.__init__(self)


@sp.add_test(name="PoolRegistryTest_1", profile=True)
def test():
    sc = sp.test_scenario()
    alice = sp.test_account("Alice")

    v = MockVault()
    sc += v

    v.registerPool(sp.nat(2)).run(sender=alice.address)

    nextNonce = v.getNextPoolNonce()
    sc.verify(nextNonce == sp.nat(2))
