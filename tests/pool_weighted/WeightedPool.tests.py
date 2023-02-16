import smartpy as sp

from contracts.pool_weighted.WeightedPool import WeightedPool


class MockVault(sp.Contract):

    def __init__(self):
        self.init(
            nonce=sp.nat(0),
            poolId=sp.bytes("0x0dae12"),
            tokens_set=False
        )

    @sp.onchain_view()
    def getNextNonce(self):
        sp.result(self.data.nonce)

    @sp.entry_point
    def registerPool(self, specialization):
        sp.set_type(specialization, sp.TNat)
        self.data.poolId = self._toPoolId(
            sp.sender, specialization, self.data.nonce)
        self.data.nonce += 1

    @sp.entry_point
    def registerTokens(self, params):
        sp.set_type(params, sp.TRecord(
            poolId=sp.TBytes,
            tokens=sp.TMap(sp.TNat, sp.TRecord(
                address=sp.TAddress, id=sp.TNat)),
            assetManagers=sp.TList(sp.TAddress)
        ))
        pass

    def _toPoolId(self, pool, specialization, nonce):
        pack = sp.record(nonce=nonce, pool=pool, specialization=specialization)
        return sp.pack(pack)


class MockWeightedPool(WeightedPool):

    def __init__(
        self,
        vault,
        tokens,
        normalizedWeights,
        name,
        symbol,
        owner,
    ):
        WeightedPool.__init__(
            self,
            vault,
            tokens,
            normalizedWeights,
            name,
            symbol,
            owner,
        )


@sp.add_test(name="WeightedPoolTest_1", profile=True)
def test():
    sc = sp.test_scenario()

    v = MockVault()
    sc += v

    tokens = sp.map({
        0: sp.record(address=sp.address('tz1'), id=sp.nat(0)),
        1: sp.record(address=sp.address('tz1'), id=sp.nat(1)),
        3: sp.record(address=sp.address('tz1'), id=sp.nat(2)),
    })

    weights = sp.map(({
        0: sp.nat(30),
        1: sp.nat(30),
        2: sp.nat(30),
    }))

    p = MockWeightedPool(
        vault=v.address,
        tokens=tokens,
        normalizedWeights=weights,
        name="Symm Liqudidty Pool Token",
        symbol="SYMMLP",
        owner=sp.address("tz1"),
    )

    sc += p
