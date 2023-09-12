import smartpy as sp

from contracts.vault.ProtocolFeesCollector import ProtocolFeesCollector

from contracts.pool_utils.SymmetricPoolToken import SymmetricPoolToken

import tests.helpers.MockSymmetric as helpers 
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


@sp.add_test(name="Can withdraw collected fees", profile=True)
def can_withdraw_collected_fees():
    sc = sp.test_scenario()

    vault = sp.test_account('Vault')
    protocolFeeWithdrawer = sp.test_account('protocolFeeWithdrawer')

    pt1 = MockPoolToken('PoolToken1', 'PT1', vault.address)
    pt2 = MockPoolToken('PoolToken2', 'PT2', vault.address)
    pt3 = MockPoolToken('PoolToken3', 'PT3', vault.address)

    sc += pt1
    sc += pt2
    sc += pt3

    pfc = ProtocolFeesCollector(
        vault.address,
        protocolFeeWithdrawer.address
    )

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
        0: sp.pair(
            pt1.address, sp.none,
        ),
        1: sp.pair(
            pt2.address, sp.none,
        ),
        2: sp.pair(
            pt3.address, sp.none,
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
    ).run(
        sender=protocolFeeWithdrawer.address
    )

    pt1Balance = pt1.getBalance(pfc.address)
    sc.verify(pt1Balance == sp.nat(0))

    pt2Balance = pt2.getBalance(pfc.address)
    sc.verify(pt2Balance == sp.nat(22400000000000000000000))

    pt3Balance = pt3.getBalance(pfc.address)
    sc.verify(pt3Balance == sp.nat(56400000000000000000000))



@sp.add_test(name="Can update swap fee", profile=True)
def can_update_swap_fee():
    env = helpers.setup_test_environment()
    sc = env["scenario"]
    pools = helpers.setup_test_pools(env["pool_factory"])
    helpers.add_test_liquidity(pools, env["vault"], env["admin"].address)

    env["fees_collector"].setSwapFeePercentage(sp.nat(500000000000000000)).run(sender=env["admin"].address)
        
    env["fees_collector"].setYieldFeePercentage(sp.nat(500000000000000000)).run(sender=env["admin"].address)

    weighted_pool = sc.dynamic_contract(0, env["pool_factory"]._creationCode)

    weighted_pool.call("updateProtocolFeePercentageCache", sp.unit).run(sender=env["admin"])

    sc.verify(weighted_pool.data.feeCache == (sp.nat(500000000000000000), sp.nat(500000000000000000)))