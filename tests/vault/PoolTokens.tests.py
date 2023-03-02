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
    pool2 = sp.test_account("Pool2")
    pool3 = sp.test_account("Pool3")
    token1 = sp.test_account('token1')
    token2 = sp.test_account('token2')
    token3 = sp.test_account('token3')
    token4 = sp.test_account('token4')

    v = MockVault()
    sc += v

    # Test MinimalSwapInfo
    v.registerPool(sp.nat(1)).run(sender=pool.address)
    poolId = _toPoolId(pool.address, sp.nat(1),  sp.nat(1))

    tokens = sp.map({
        0: sp.record(address=token1.address, id=sp.nat(0), FA2=False),
        1: sp.record(address=token2.address, id=sp.nat(43), FA2=False),
        2: sp.record(address=token1.address, id=sp.nat(1), FA2=False),
    })

    assetManagers = [
        sp.address('tz100000000000000000000000000000000000000')] * 3

    v.registerTokens(sp.record(
        poolId=poolId,
        tokens=tokens,
        assetManagers=assetManagers
    ))

    newTokens = sp.map({
        0: sp.record(address=token3.address, id=sp.nat(0), FA2=False),
        1: sp.record(address=token4.address, id=sp.nat(0), FA2=False),
    })

    v.registerTokens(sp.record(
        poolId=poolId,
        tokens=newTokens,
        assetManagers=assetManagers
    ))

   # Test TwoTokensPool
    v.registerPool(sp.nat(2)).run(sender=pool2.address)
    tokens2 = sp.map({
        0: sp.record(address=token1.address, id=sp.nat(0), FA2=False),
        1: sp.record(address=token2.address, id=sp.nat(43), FA2=False),
    })
    poolId2 = _toPoolId(pool2.address, sp.nat(2),  sp.nat(2))

    v.registerTokens(sp.record(
        poolId=poolId2,
        tokens=tokens2,
        assetManagers=assetManagers
    ))

    # Test GeneralPool
    v.registerPool(sp.nat(0)).run(sender=pool3.address)

    poolId3 = _toPoolId(pool3.address, sp.nat(0),  sp.nat(3))

    v.registerTokens(sp.record(
        poolId=poolId3,
        tokens=tokens,
        assetManagers=assetManagers
    ))

    v.registerTokens(sp.record(
        poolId=poolId3,
        tokens=newTokens,
        assetManagers=assetManagers
    ))
