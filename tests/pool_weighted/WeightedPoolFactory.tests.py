import smartpy as sp

from contracts.pool_weighted.WeightedPoolFactory import WeightedPoolFactory

from contracts.utils.tokens.FA12 import FA12_common

from contracts.pool_weighted.ExternalWeightedMath import ExternalWeightedMath

from contracts.pool_weighted.ExternalWeightedProtocolFees import ExternalWeightedProtocolFees

from contracts.vault.ProtocolFeesCollector import ProtocolFeesCollector


class MockWeightedPoolFactory(WeightedPoolFactory):
    def __init__(
        self,
        admin,
        vault,
        weightedMathLib,
        weightedProtocolFeesLib,
        protocolFeeProvider,
        metadata,
    ):
        WeightedPoolFactory.__init__(
            self,
            admin,
            vault,
            weightedMathLib,
            weightedProtocolFeesLib,
            protocolFeeProvider,
            metadata,
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
    admin = sp.test_account('Admin')
    vault = sp.test_account('Vault')

    pfc = ProtocolFeesCollector(
        vault.address,
        admin.address,
    )

    sc += pfc

    m = ExternalWeightedMath()
    sc += m

    wpf = ExternalWeightedProtocolFees()
    sc += wpf

    # CONTRACT_STORAGE = sp.record(
    #     protocolFeeProvider=sp.address('KT1VqarPDicMFn1ejmQqqshUkUXTCTXwmkCN'),
    #     vault=sp.address('KT1N5Qpp5DaJzEgEXY1TW6Zne6Eehbxp83XF'),
    #     weightedMathLib=m.address,
    # )
    CONTRACT_METADATA = {
        "": "ipfs://QmbEE3NYTuhE2Vk8sQap4kkKyFQ2P1X6GDRCufxDCpBkLa",
    }
    c = MockWeightedPoolFactory(
        admin.address,
        sp.address('KT1N5Qpp5DaJzEgEXY1TW6Zne6Eehbxp83XF'),
        m.address,
        wpf.address,
        pfc.address,
        CONTRACT_METADATA,
    )

    sc += c

    token_metadata = {
        "name": "SYMM/CTEZ 50:50",
        "symbol": "SYMMLP",
        "decimals": "18",
        "thumbnailUri": "ipfs://QmRzY4YdHBFUeuGPhmPRAUWkVN9qhH3pW14et5V6kZqFZM",
    }

    create_params = sp.record(
        # name='Weighted Pool',
        # symbol='SYMMLP',
        metadata=sp.utils.bytes_of_string("<ipfs://....>"),
        token_metadata=normalize_metadata(token_metadata),
    )
    c.create(create_params)
