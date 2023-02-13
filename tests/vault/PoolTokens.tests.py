import smartpy as sp

from contracts.vault.PoolTokens import PoolTokens


class MockVault(sp.Contract, PoolTokens):
    def __init__(self):
        sp.Contract.__init__(self)
        PoolTokens.__init__(self)


@sp.add_test(name="PoolTokensTest_1", profile=True)
def test():
    def _toPoolId(pool, specialization, nonce):
        return sp.pack(sp.record(
            nonce=nonce,
            specialization=specialization,
            pool=pool,
        ))
    sc = sp.test_scenario()
    pool = sp.test_account("Pool")
    token1 = sp.test_account('token1')
    token2 = sp.test_account('token2')

    v = MockVault()
    sc += v

    v.registerPool(sp.nat(1)).run(sender=pool.address)
    poolId = _toPoolId(pool.address, sp.nat(1),  sp.nat(1))

    tokens = sp.set([
        sp.record(address=token1.address, id=sp.nat(0)),
        sp.record(address=token2.address, id=sp.nat(43)),
        sp.record(address=token1.address, id=sp.nat(1)),
    ])

    assetManagers = [
        sp.address('tz100000000000000000000000000000000000000')] * 6

    v.registerTokens(sp.record(
        poolId=poolId,
        tokens=tokens,
        assetManagers=assetManagers
    ))
