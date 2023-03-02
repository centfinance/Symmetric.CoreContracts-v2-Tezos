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
                address=sp.TAddress, id=sp.TNat, FA2=sp.TBool)),
            assetManagers=sp.TOption(sp.TMap(sp.TNat, sp.TAddress))
        ))
        pass

    def _toPoolId(self, pool, specialization, nonce):
        pack = sp.record(nonce=nonce, pool=pool, specialization=specialization)
        return sp.pack(pack)


class MockWeightedPool(WeightedPool):

    def __init__(
        self,
        vault,
        name,
        symbol,
        owner,
    ):
        WeightedPool.__init__(
            self,
            vault,
            name,
            symbol,
            owner,
        )
        self.update_initial_storage(
            swapGivenIn=sp.nat(0),
        )

    @sp.entry_point
    def test_onSwapGivenIn(self, params):
        swapGivenIn = self._onSwapGivenIn(params)
        self.data.swapGivenIn = swapGivenIn


@sp.add_test(name="WeightedPoolTest_1", profile=True)
def test():
    sc = sp.test_scenario()

    v = MockVault()
    sc += v

    tokens = sp.map({
        0: sp.record(address=sp.address('tz1'), id=sp.nat(0), FA2=False),
        1: sp.record(address=sp.address('tz1'), id=sp.nat(1), FA2=False),
    })

    weights = sp.map({
        0: sp.nat(500000000000000000),
        1: sp.nat(500000000000000000),
    })

    decimals = sp.map({
        0: sp.nat(3),
        1: sp.nat(12),
    })

    p = MockWeightedPool(
        vault=v.address,
        name="Symm Liqudidty Pool Token",
        symbol="SYMMLP",
        owner=sp.address("tz1"),
    )

    sc += p

    p.initialize(
        sp.record(
            tokens=tokens,
            normalizedWeights=weights,
            tokenDecimals=decimals,
            swapFeePercentage=sp.nat(15000000000000000)
        )
    )
