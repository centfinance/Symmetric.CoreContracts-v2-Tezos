import smartpy as sp

from contracts.pool_weighted.WeightedPoolFactory import WeightedPoolFactory

from contracts.utils.tokens.FA12 import FA12_common

from contracts.pool_weighted.ExternalWeightedMath import ExternalWeightedMath


class MockWeightedPoolFactory(WeightedPoolFactory):
    def __init__(
            self,
            vault,
            weightedMathLib,
            protocolFeeProvider,
    ):
        WeightedPoolFactory.__init__(
            self,
            vault,
            weightedMathLib,
            protocolFeeProvider,
        )

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

    m = ExternalWeightedMath()
    sc += m

    # CONTRACT_STORAGE = sp.record(
    #     protocolFeeProvider=sp.address('KT1VqarPDicMFn1ejmQqqshUkUXTCTXwmkCN'),
    #     vault=sp.address('KT1N5Qpp5DaJzEgEXY1TW6Zne6Eehbxp83XF'),
    #     weightedMathLib=m.address,
    # )

    c = MockWeightedPoolFactory(
        sp.address('KT1N5Qpp5DaJzEgEXY1TW6Zne6Eehbxp83XF'),
        m.address,
        sp.address('KT1VqarPDicMFn1ejmQqqshUkUXTCTXwmkCN'),
    )

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
    )
    c.create(create_params)
