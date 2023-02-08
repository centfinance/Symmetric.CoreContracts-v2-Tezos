import smartpy as sp

from contracts.pool_weighted.WeightedPoolFactory import WeightedPoolFactory


class MockWeightedPoolFactory(WeightedPoolFactory):
    def __init__(self, params):
        WeightedPoolFactory.__init__(self, params)

    @sp.onchain_view()
    def get_storage(self):
        sp.result(self.data)


@sp.add_test(name="WeightedPoolFactoryTest_1", profile=True)
def test():
    sc = sp.test_scenario()

    CONTRACT_STORAGE = sp.record(
        vault=sp.address('KT1TxqZ8QtKvLu3V3JH7Gx58n7Co8pgtpQU5'),
        protocolFeeProvider=sp.address('KT1VqarPDicMFn1ejmQqqshUkUXTCTXwmkCN'),
    )
    c = MockWeightedPoolFactory(CONTRACT_STORAGE)

    sc += c
    create_params = sp.record(
        protocolFeeProvider=sp.address('KT1VqarPDicMFn1ejmQqqshUkUXTCTXwmkCN'),
        vault=sp.address('KT1TxqZ8QtKvLu3V3JH7Gx58n7Co8pgtpQU5'),
    )
    c.create(create_params)
