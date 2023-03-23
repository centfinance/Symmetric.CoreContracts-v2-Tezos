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

    @sp.entry_point
    def mintPoolTokens(self, recipient, amount):
        return super()._mintPoolTokens(recipient, amount)


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

    pt1.mintPoolTokens(sp.record(recipient=pfc.address,
                       amount=1000000000000000000000))
    pt2.mintPoolTokens(sp.record(recipient=pfc.address,
                       amount=23400000000000000000000))
    pt3.mintPoolTokens(sp.record(recipient=pfc.address,
                       amount=57400000000000000000000))

    pt1Balance = pt1.getBalance(pfc.address)
    sc.verify(pt1Balance == sp.nat(1000000000000000000000))

    pt2Balance = pt2.getBalance(pfc.address)
    sc.verify(pt2Balance == sp.nat(23400000000000000000000))

    pt3Balance = pt3.getBalance(pfc.address)
    sc.verify(pt3Balance == sp.nat(57400000000000000000000))

    tokens = sp.map({
        0: sp.record(
            address=pt1.address,
            id=sp.nat(0),
            FA2=False
        ),
        1: sp.record(
            address=pt2.address,
            id=sp.nat(0),
            FA2=False
        ),
        2: sp.record(
            address=pt3.address,
            id=sp.nat(0),
            FA2=False
        ),
    })

    amounts = sp.map({
        0: sp.nat(1000000000000000000000),
        1: sp.nat(1000000000000000000000),
        2: sp.nat(1000000000000000000000),
    })

    pfc.withdrawCollectedFees(
        sp.record(
            tokens=tokens,
            amounts=amounts,
            recipient=vault.address,
        )
    )

    pt1Balance = pt1.getBalance(pfc.address)
    sc.verify(pt1Balance == sp.nat(0))

    pt2Balance = pt2.getBalance(pfc.address)
    sc.verify(pt2Balance == sp.nat(22400000000000000000000))

    pt3Balance = pt3.getBalance(pfc.address)
    sc.verify(pt3Balance == sp.nat(56400000000000000000000))

    pfc.setSwapFeePercentage(sp.nat(10000000000000000))

    pfc.setFlashLoanFeePercentage(sp.nat(1000000000000000))
