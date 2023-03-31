import smartpy as sp


class PoolRegistry:
    def __init__(self):
        self.update_initial_storage(
            isPoolRegistered=sp.big_map(
                l={},
                tkey=sp.TBytes,
                tvalue=sp.TUnit,
            ),
            nextPoolNonce=sp.nat(1)
        )

    @sp.entry_point(lazify=False)
    def registerPool(self):
        self.onlyUnpaused()
        poolId = (sp.compute(self.data.nextPoolNonce), sp.sender)

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
