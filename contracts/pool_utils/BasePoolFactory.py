from contracts.pool_utils.BasePool import IBasePool
import smartpy as sp


class BasePoolFactory:

    def __init__(
        self,
        vault,
        protocolFeeProvider,
    ):
        self.update_initial_storage(
            vault=vault,
            protocolFeeProvider=protocolFeeProvider,
            isPoolFromFactory=sp.big_map(
                l={},
                tkey=sp.TAddress,
                tvalue=sp.TUnit,
            ),
        )

        def _create(self, params):
            pool = sp.create_contract(
                contract=self._creationCode, storage=params)
            IBasePool.initialize(self, pool)
            self.data.isPoolFromFactory[pool] = sp.unit

            sp.emit(pool, with_type=True, tag='PoolCreated')

        self._create = _create
