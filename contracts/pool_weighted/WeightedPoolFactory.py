import smartpy as sp

import contracts.pool_weighted.WeightedPool as WeightedPool

import contracts.pool_utils.BasePoolFactory as BasePoolFactory


class WeightedPoolFactory(sp.contract):

    def __init__(self, params):
        self.init_type(
            params=sp.TRecord(
                vault=sp.TAddress,
                protocolFeeProvider=sp.TAddress,
            )
        )

        BasePoolFactory.__init__(
            self,
            params,
        )

        self._creationCode = WeightedPool()

    @sp.entry_point
    def create(self, params):
