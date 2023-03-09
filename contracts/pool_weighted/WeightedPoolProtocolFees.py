import smartpy as sp


class WeightedPoolProtocolFees:
    def __init__(self, params):
        self.update_initial_storage(
            exemptFromYieldFees=False,
            athRateProduct=sp.nat(0),
            rateProviders=sp.map(l={}, tkey=sp.TNat,
                                 tvalue=sp.TOption(sp.TAddress)),
        )

    def initialize(self, params):
        sp.verify(sp.len(params.numTokens) == sp.len(params.rateProviders))

        self.data.exemptFromYieldFees = self._getYieldFeeExemption(
            params.rateProviders)

        self.data.rateProviders = params.rateProviders

    def _getYieldFeeExemption(self, rateProviders):
        exempt = sp.local('exempt', True)

        with sp.for_('i', sp.range(0, sp.len(rateProviders)))as i:
            with sp.if_(rateProviders[i] != sp.none):
                exempt.value = False

        return exempt.value
