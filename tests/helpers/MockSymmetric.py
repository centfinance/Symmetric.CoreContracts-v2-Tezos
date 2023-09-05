import smartpy as sp

from contracts.vault.Vault import Vault

from contracts.vault.ProtocolFeesCollector import ProtocolFeesCollector

from contracts.pool_weighted.WeightedPool import WeightedPool

from contracts.pool_weighted.WeightedPoolFactoryNoAdmin import WeightedPoolFactoryNoAdmin

from contracts.pool_weighted.ExternalWeightedMath import ExternalWeightedMath

from contracts.pool_weighted.ExternalWeightedProtocolFees import ExternalWeightedProtocolFees

from tests.tokens.fa12 import FA12

from tests.tokens.fa2 import FA2


def setup_test_environment():
    # Initialize test scenario and accounts
    sc = sp.test_scenario()
    admin = sp.test_account('Admin')
    
    # Deploy ExternalWeightedMath
    m = ExternalWeightedMath()
    sc += m

    # Deploy ExternalWeightedProtocolFees
    pf = ExternalWeightedProtocolFees()
    sc += pf

    # Metadata for Vault
    CONTRACT_METADATA = {
        "": "ipfs://QmbEE3NYTuhE2Vk8sQap4kkKyFQ2P1X6GDRCufxDCpBkLa",
    }

    # Deploy Vault
    v = Vault(admin.address, CONTRACT_METADATA)
    sc += v

    # Deploy ProtocolFeesCollector
    pfc = ProtocolFeesCollector(v.address, admin.address)
    sc += pfc

    # Deploy WeightedPoolFactory
    wpf = WeightedPoolFactoryNoAdmin(
        admin.address,
        v.address,
        m.address,
        pf.address,
        pfc.address,
        (sp.nat(400000000000000000), sp.nat(400000000000000000)),
        CONTRACT_METADATA
    )
    sc += wpf
    
    # Return the test environment for use in tests
    return {
        "scenario": sc,
        "admin": admin,
        "math": m,
        "protocol_fees": pf,
        "vault": v,
        "fees_collector": pfc,
        "pool_factory": wpf
    }

# def token_list(sc, admin):
#         # deploy FA2
#     fa2 = FA2(admin.address, metadata={})
    
#     sc += fa2

#     fa12_tokens = {
#         "token_1": FA12(admin.address),
#         "token_2": FA12(admin.address),
#         "token_3": FA12(admin.address),
#         "token_4": FA12(admin.address),
#         "token_5": FA12(admin.address),
#         "token_6": FA12(admin.address),
#     }

#     # Add fa12_tokens to sc
def normalize_metadata(self, metadata):
        meta = {}
        for key in metadata:
            meta[key] = sp.utils.bytes_of_string(metadata[key])

        return meta




def setup_test_pools(sc, factory):
    
    CONTRACT_METADATA= {
        "": "<ipfs://....>",
    }

    TOKEN_METADATA = {
            "name": "SYMM LP",
            "symbol": "SLP",
            "decimals": "18",
            "thumbnailUri": "ipfs://......",
    }

    TOKENS = {
        "SYMM": (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.none),
        "CTZ": (sp.address('KT1SjXiUX63QvdNMcM2m492f7kuf8JxXRLp4'), sp.none),
        "USDT": (sp.address('KT1XnTn74bUtxHfDtBmm2bGZAQfhPbvKWR8o'), sp.some(sp.nat(0))),
        "uUSD": (sp.address('KT1XnTn74bUtxHfDtBmm2bGZAQfhPbvKWR8o'), sp.some(sp.nat(0))),
        "uBTC": (sp.address('KT1XnTn74bUtxHfDtBmm2bGZAQfhPbvKWR8o'), sp.some(sp.nat(2))),
        "uXTZ": (sp.address('KT1XnTn74bUtxHfDtBmm2bGZAQfhPbvKWR8o'), sp.some(sp.nat(3))),
        "YOU": (sp.address('KT1Xobej4mc6XgEjDoJoHtTKgbD1ELMvcQuL'), sp.some(sp.nat(0))),
        "tzBTC": (sp.address('KT1PWx2mnDueood7fEmfbBDKx1D9BAnnXitn'), sp.none),
        "PLY": (sp.address('KT1GRSvLoikDsXujKgZPsGLX8k8VvR2Tq95b'), sp.none),
        "wUSDC":  (sp.address('KT18fp5rcTW7mbWDmzFwjLDUhs5MeJmagDSZ'), sp.some(sp.nat(17))),
    }

    DECIMALS = {
        "SYMM": sp.nat(18),
        "CTZ": sp.nat(18),
        "USDT": sp.nat(6),
        "uUSD": sp.nat(6),
        "uBTC": sp.nat(8),
        "uXTZ": sp.nat(18),
        "YOU": sp.nat(18),
        "tzBTC": sp.nat(8),
        "PLY": sp.nat(18),
        "wUSDC": sp.nat(6),
    }

    RATE_PROVIDERS = {
        "SYMM": sp.none,
        "CTZ": sp.none,
        "USDT": sp.none,
        "uUSD": sp.none,
        "uBTC": sp.none,
        "uXTZ": sp.none,
        "YOU": sp.none,
        "tzBTC": sp.none,
        "PLY": sp.none,
        "wUSDC": sp.none,
    }

    def create_pool(tokens_list, swapFeePercentage, weights_list):
        assert len(tokens_list) == len(weights_list), "Tokens and weights list lengths must match"
        
        tokens_map = {}
        normalizedWeights_map = {}
        tokenDecimals_map = {}
        rateProviders_map = {}
        token_metadata_map = {}
        
        for idx, token_key in enumerate(tokens_list):
            tokens_map[idx] = TOKENS[token_key]
            normalizedWeights_map[idx] = sp.nat(weights_list[idx] * (10 ** 18))
            tokenDecimals_map[idx] = DECIMALS[token_key]
            rateProviders_map[idx] = RATE_PROVIDERS[token_key]
            token_metadata_map[idx] = sp.record(token_id=idx, token_info=normalize_metadata(TOKEN_METADATA))
            
        factory.create(
            tokens=sp.map(tokens_map),
            normalizedWeights=sp.map(normalizedWeights_map),
            tokenDecimals=sp.map(tokenDecimals_map),
            rateProviders=sp.map(rateProviders_map),
            swapFeePercentage=sp.nat(swapFeePercentage * (10 ** 18)),
            metadata=sp.big_map(normalize_metadata(CONTRACT_METADATA)),
            token_metadata=sp.big_map(token_metadata_map)
        )
        factory.init()
    
    # Pools with varied weights
    create_pool(["SYMM", "CTZ"], 0.01, [0.4, 0.6])
    create_pool(["SYMM", "USDT", "uBTC"], 0.02, [0.3, 0.5, 0.2])
    create_pool(["SYMM", "USDT", "uBTC", "uXTZ"], 0.025, [0.25, 0.25, 0.3, 0.2])
    create_pool(["SYMM", "USDT", "uBTC", "uXTZ", "YOU"], 0.03, [0.2, 0.2, 0.2, 0.2, 0.2])
    create_pool(["SYMM", "USDT", "uBTC", "uXTZ", "YOU", "tzBTC"], 0.035, [0.2, 0.15, 0.15, 0.15, 0.15, 0.2])
    create_pool(["SYMM", "USDT", "uBTC", "uXTZ", "YOU", "tzBTC", "PLY"], 0.04, [0.15, 0.15, 0.15, 0.1, 0.1, 0.1, 0.25])
    create_pool(["SYMM", "USDT", "uBTC", "uXTZ", "YOU", "tzBTC", "PLY", "wUSDC"], 0.045, [0.15, 0.1, 0.1, 0.1, 0.1, 0.1, 0.15, 0.2])