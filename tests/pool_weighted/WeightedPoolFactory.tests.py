import smartpy as sp

from contracts.pool_weighted.WeightedPoolFactory import WeightedPoolFactory

from contracts.utils.tokens.FA12 import FA12_common


class MockWeightedPoolFactory(WeightedPoolFactory):
    def __init__(self, params):
        WeightedPoolFactory.__init__(self, params)

    @sp.onchain_view()
    def get_storage(self):
        sp.result(self.data)


def normalize_metadata(metadata):
    meta = {}
    for key in metadata:
        meta[key] = sp.utils.bytes_of_string(metadata[key])

    return meta


@sp.add_test(name="WeightedPoolFactoryTest_1", profile=True)
def test():
    sc = sp.test_scenario()

    CONTRACT_STORAGE = sp.record(
        protocolFeeProvider=sp.address('KT1VqarPDicMFn1ejmQqqshUkUXTCTXwmkCN'),
        vault=sp.address('KT1N5Qpp5DaJzEgEXY1TW6Zne6Eehbxp83XF'),
    )
    c = MockWeightedPoolFactory(CONTRACT_STORAGE)

    sc += c

    token_metadata = {
        "name": "Symmetric Pool Token",
        "symbol": "SYMMLP",
        "decimals": "18",
        "thumbnailUri": "ipfs://......",
    }

    create_params = sp.record(
        # name='Weighted Pool',
        # symbol='SYMMLP',
        metadata=sp.utils.bytes_of_string("<ipfs://....>"),
        token_metadata=normalize_metadata(token_metadata),
        vault=sp.address('KT1TxqZ8QtKvLu3V3JH7Gx58n7Co8pgtpQU5'),
    )
    c.create(create_params)
