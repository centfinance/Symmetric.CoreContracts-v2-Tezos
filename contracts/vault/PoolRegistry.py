import smartpy as sp


class PoolRegistry:
    def __init__(self):
        self.update_initial_storage(
            _isPoolRegistered=sp.big_map(
                l={},
                tkey=sp.TBytes,
                tvalue=sp.TUnit,
            ),
            nextPoolNonce=sp.nat(1)
        )

    @sp.entry_point
    def registerPool(self, specialization):
        sp.set_type(specialization, sp.TNat)

        poolId = self._toPoolId(
            self, sp.sender, specialization, self.data.nextPoolNonce)

        self.data._isPoolRegistered[poolId] = sp.unit

        self.data.nextPoolNonce += 1

        poolEvent = sp.record(
            poolId=poolId,
            pool=sp.sender,
            specialization=specialization
        )
        sp.emit(poolEvent, tag='PoolRegistered', with_type=True)

    @sp.onchain_view()
    def getNextNonce(self):
        sp.result(self.data.nextPoolNonce)

    def _toPoolId(self, pool, specialization, nonce):
        pack = sp.record(nonce=nonce, pool=pool, specialization=specialization)
        return sp.pack(pack)
