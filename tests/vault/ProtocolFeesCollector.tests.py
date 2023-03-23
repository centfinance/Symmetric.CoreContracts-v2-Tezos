import smartpy as sp

from contracts.vault.ProtocolFeesCollector import ProtocolFeesCollector

from contracts.pool_utils.SymmetricPoolToken import SymmetricPoolToken


class MockPoolToken(
    SymmetricPoolToken
):
    def __init__(
            self,
            name,
            symbol,
            vault,
    ):
        SymmetricPoolToken.__init__(
            self,
            name,
            symbol,
            vault,
        )


@sp.add_test(name="ProtocolFeesCollectorTest_1", profile=True)
def test():
    sc = sp.test_scenario()

    vault = sp.test_account('Vault')

    pt1 = MockPoolToken('PoolToken1', 'PT1', vault.address)
    pt2 = MockPoolToken('PoolToken2', 'PT2', vault.address)
    pt3 = MockPoolToken('PoolToken3', 'PT3', vault.address)

    sc += pt1
    sc += pt2
    sc += pt3

    pfc = ProtocolFeesCollector(vault=vault.address)

    sc += pfc
