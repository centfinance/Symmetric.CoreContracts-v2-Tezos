import smartpy as sp

import contracts.pool_utils.lib.PoolRegistrationLib as PoolRegistrationLib


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
            assetManagers=sp.TList(sp.TAddress)
        ))
        pass

    def _toPoolId(self, pool, specialization, nonce):
        pack = sp.record(nonce=nonce, pool=pool, specialization=specialization)
        return sp.pack(pack)


class MockPool(sp.Contract):

    def __init__(self, params):
        self.init(
            vault=params.vault,
            specialization=params.specialization,
            tokens=params.tokens,
            poolId=sp.bytes("0x0dae11")
        )
        self.init_type(
            sp.TRecord(
                vault=sp.TAddress,
                specialization=sp.TNat,
                tokens=sp.TMap(sp.TNat, sp.TRecord(
                    address=sp.TAddress, id=sp.TNat, FA2=sp.TBool)),
                poolId=sp.TBytes
            )
        )

    @sp.entry_point
    def initialize(self):
        assetManagers = [
            sp.address('tz100000000000000000000000000000000000000')] * 1
        poolId = PoolRegistrationLib.registerPool(
            vault=self.data.vault, specialization=self.data.specialization, tokens=self.data.tokens, assetManagers=assetManagers)
        self.data.poolId = poolId


@sp.add_test(name="PoolRegistrationLibTest_1", profile=True)
def test():
    sc = sp.test_scenario()

    v = MockVault()
    sc += v

    tokens = sp.map({
        0: sp.record(address=sp.address('tz1'), id=sp.nat(0), FA2=False),
    })
    p = MockPool(sp.record(
        vault=v.address,
        specialization=sp.nat(2),
        tokens=tokens
    ))
    sc += p
    p.initialize()
    sc.verify(v.data.nonce == sp.nat(1))
    sc.verify(p.data.poolId == v.data.poolId)
