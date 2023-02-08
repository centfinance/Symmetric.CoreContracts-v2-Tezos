import smartpy as sp

from contracts.pool_weighted.WeightedPool import WeightedPool

from contracts.pool_utils.BasePoolFactory import BasePoolFactory


# class Types:

#     CREATE_PARAMS = sp.TRecord(
#         name=sp.TString,
#         symbol=sp.TString,
#         tokens=sp.TList(t=sp.TAddress),
#         tokenIds=sp.TList(t=sp.TNat),
#         normalizedWeights=sp.TList(t=sp.TNat),
#         # Implement later
#         # rateProviders=sp.TList(t=sp.TNat)
#         swapFeePercentage=sp.TNat,
#         owner=sp.TAddress
#     )


class WeightedPoolFactory(sp.Contract):

    def __init__(self, params):
        self.init_type(
            sp.TRecord(
                _vault=sp.TAddress,
                _protocolFeeProvider=sp.TAddress,
                _isPoolFromFactory=sp.TBigMap(sp.TAddress, sp.TUnit)
            )
        )
        self._creationCode = WeightedPool(params)

        BasePoolFactory.__init__(
            self,
            params,
        )

    @sp.entry_point
    def create(self, params):
        """
            Deploys a new WeightedPool
        """
        # TODO: Add WeightedPool params type
        # sp.set_type(params, Types.CREATE_PARAMS)
        self._create(self, params)


# CONTRACT_STORAGE = sp.record(
#     vault=sp.address('KT1TxqZ8QtKvLu3V3JH7Gx58n7Co8pgtpQU5'),
#     protocolFeeProvider=sp.address('KT1VqarPDicMFn1ejmQqqshUkUXTCTXwmkCN'),
# )
# sp.add_compilation_target('Test', WeightedPoolFactory(params=CONTRACT_STORAGE))
