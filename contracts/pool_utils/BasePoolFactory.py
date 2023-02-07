import smartpy as sp


class BasePoolFactory(sp.contract):

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

        self._isPoolFromFactory[pool] = sp.unit

        # emit PoolCreated( event

        return pool
