import smartpy as sp

import contracts.pool_weighted.WeightedPool as WeightedPool

import contracts.pool_utils.BasePoolFactory as BasePoolFactory


class Types:

    CREATE_PARAMS = sp.TRecord(
        name=sp.TString,
        symbol=sp.TString,
        tokens=sp.TList(t=sp.TAddress),
        tokenIds=sp.TList(t=sp.TNat),
        normalizedWeights=sp.TList(t=sp.TNat),
        # Implement later
        # rateProviders=sp.TList(t=sp.TNat)
        swapFeePercentage=sp.TNat,
        owner=sp.TAddress
    )


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
        """
            Deploys a new WeightedPool
        """
        sp.set_type(params, Types.CREATE_PARAMS)
        weighted_pool_params = sp.record(
            params,
            vault=self.data.vault,
            protocolFeeProvider=self.data.protocolFeeProvider,
        )
        self._create(self, weighted_pool_params)
