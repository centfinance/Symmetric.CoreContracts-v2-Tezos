import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors



class PoolRegistry:
    def __init__(self):
        self.update_initial_storage(
            isPoolRegistered=sp.big_map(
                l={},
                tkey=sp.TPair(sp.TAddress, sp.TNat),
                tvalue=sp.TUnit,
            ),
            nextPoolNonce=sp.nat(1)
        )

    @sp.entry_point(lazify=False)
    def registerPool(self):
        self.onlyUnpaused()
        poolId = (sp.sender, sp.compute(self.data.nextPoolNonce))

        self.data.isPoolRegistered[poolId] = sp.unit

        self.data.nextPoolNonce += 1

        poolEvent = sp.record(
            poolId=poolId,
            pool=sp.sender,
        )
        sp.emit(poolEvent, tag='PoolRegistered', with_type=True)

    @sp.onchain_view()
    def getNextPoolNonce(self):
        sp.result(self.data.nextPoolNonce)

    def _ensureRegisteredPool(self, poolId):
        sp.verify(self.data.isPoolRegistered.contains(poolId), Errors.INVALID_POOL_ID)