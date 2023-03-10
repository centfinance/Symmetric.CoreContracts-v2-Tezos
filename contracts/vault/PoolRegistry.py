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
            sp.sender, specialization, self.data.nextPoolNonce)

        self.data._isPoolRegistered[poolId] = sp.unit

        self.data.nextPoolNonce += 1

        poolEvent = sp.record(
            poolId=poolId,
            pool=sp.sender,
            specialization=specialization
        )
        sp.emit(poolEvent, tag='PoolRegistered', with_type=True)

    @sp.onchain_view(pure=True)
    def getNextPoolNonce(self):
        sp.result(self.data.nextPoolNonce)

    def _toPoolId(self, pool, specialization, nonce):
        pack = sp.record(
            nonce=nonce,
            pool=pool,
            specialization=specialization
        )
        return sp.pack(pack)

    def _getPoolSpecialization(self, poolId):
        sp.set_type(poolId, sp.TBytes)

        record = sp.unpack(poolId, sp.TRecord(
            nonce=sp.TNat,
            pool=sp.TAddress,
            specialization=sp.TNat
        )).open_some(message="Invalid poolId")
        return record.specialization

    def _getPoolAddress(self, poolId):
        sp.set_type(poolId, sp.TBytes)

        record = sp.unpack(poolId, sp.TRecord(
            nonce=sp.TNat,
            pool=sp.TAddress,
            specialization=sp.TNat
        )).open_some(message="Invalid poolId")
        return record.pool
