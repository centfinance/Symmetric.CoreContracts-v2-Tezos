import smartpy as sp


class BasePoolFactory:

    def __init__(self, params):
        self.update_initial_storage(
            _vault=params.vault,
            _protocolFeeProvider=params.protocolFeeProvider,
            _isPoolFromFactory=sp.big_map(
                l={},
                tkey=sp.TAddress,
                tvalue=sp.TUnit,
            ),
        )

        def _create(self, params):
            pool = sp.create_contract(
                contract=self._creationCode, storage=params)

            self.data._isPoolFromFactory[pool] = sp.unit

            sp.emit(pool, with_type=True, tag='PoolCreated')

        self._create = _create
