import smartpy as sp

from contracts.pool_weighted.WeightedPoolFactory import WeightedPoolFactory

from contracts.utils.tokens.FA12 import FA12_common

from contracts.pool_weighted.ExternalWeightedMath import ExternalWeightedMath

from contracts.pool_weighted.ExternalWeightedProtocolFees import ExternalWeightedProtocolFees

from contracts.vault.ProtocolFeesCollector import ProtocolFeesCollector

TOKEN = sp.TPair(sp.TAddress, sp.TOption(sp.TNat))

TOKENS = sp.TMap(sp.TNat, TOKEN)


class MockVault(sp.Contract):

    def __init__(self):
        self.init(
            nonce=sp.nat(0),
            poolId=(sp.address('tz1'), sp.nat(0)),
            tokens_set=False
        )

    @sp.onchain_view()
    def getNextPoolNonce(self):
        sp.result(self.data.nonce)

    @sp.entry_point
    def registerPool(self):
        self.data.poolId = (sp.sender, self.data.nonce)
        self.data.nonce += 1

    @sp.entry_point
    def registerTokens(self, params):
        sp.set_type(params, sp.TRecord(
            poolId=sp.TPair(sp.TAddress, sp.TNat),
            tokens=TOKENS,
            assetManagers=sp.TOption(sp.TMap(sp.TNat, sp.TAddress)),
        ))
        self.data.tokens_set = True


class MockWeightedPoolFactory(WeightedPoolFactory):
    def __init__(
        self,
        admin,
        vault,
        weightedMathLib,
        weightedProtocolFeesLib,
        protocolFeeProvider,
        feeCache,
        metadata,
    ):
        WeightedPoolFactory.__init__(
            self,
            admin,
            vault,
            weightedMathLib,
            weightedProtocolFeesLib,
            protocolFeeProvider,
            feeCache,
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

    vault = MockVault()
    sc += vault

    pfc = ProtocolFeesCollector(
        vault.address,
        admin.address,
    )

    sc += pfc

    m = ExternalWeightedMath()
    sc += m

    wpf = ExternalWeightedProtocolFees()
    sc += wpf

    CONTRACT_METADATA = {
        "": "ipfs://QmbEE3NYTuhE2Vk8sQap4kkKyFQ2P1X6GDRCufxDCpBkLa",
    }
    c = MockWeightedPoolFactory(
        admin.address,
        vault.address,
        m.address,
        wpf.address,
        pfc.address,
        (sp.nat(400000000000000000), sp.nat(400000000000000000)),
        CONTRACT_METADATA,
    )

    sc += c

    token_metadata = {
        "name": "SYMM/CTEZ 50:50",
        "symbol": "SYMMLP",
        "decimals": "18",
        "thumbnailUri": "ipfs://QmRzY4YdHBFUeuGPhmPRAUWkVN9qhH3pW14et5V6kZqFZM",
    }

    tokens = sp.map({
        0: (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.none),
        1: (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.some(sp.nat(1))),
        2: (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.some(sp.nat(2))),
        3: (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.some(sp.nat(3))),
        4: (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.some(sp.nat(4))),
        5: (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.some(sp.nat(5))),
        6: (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.some(sp.nat(0))),
        7: (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.some(sp.nat(6))),
    })

    weights = sp.map({
        0: sp.nat(125000000000000000),
        1: sp.nat(125000000000000000),
        2: sp.nat(125000000000000000),
        3: sp.nat(125000000000000000),
        4: sp.nat(125000000000000000),
        5: sp.nat(125000000000000000),
        6: sp.nat(125000000000000000),
        7: sp.nat(125000000000000000),
    })

    decimals = sp.map({
        0: sp.nat(18),
        1: sp.nat(18),
        2: sp.nat(18),
        3: sp.nat(18),
        4: sp.nat(18),
        5: sp.nat(18),
        6: sp.nat(18),
        7: sp.nat(18),
    })

    create_params = sp.record(
        tokens=tokens,
        tokenDecimals=decimals,
        normalizedWeights=weights,
        rateProviders=sp.none,
        swapFeePercentage=sp.nat(10000000000000000),
        metadata=sp.utils.bytes_of_string("<ipfs://....>"),
        token_metadata=normalize_metadata(token_metadata),
    )
    c.create(create_params).run(sender=admin.address)
