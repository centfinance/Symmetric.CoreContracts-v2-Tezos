import smartpy as sp

from contracts.vault.Vault import Vault

from contracts.vault.ProtocolFeesCollector import ProtocolFeesCollector

from contracts.pool_weighted.WeightedPool import WeightedPool

from contracts.pool_weighted.WeightedPoolFactoryNoAdmin import WeightedPoolFactoryNoAdmin

from contracts.pool_weighted.ExternalWeightedMath import ExternalWeightedMath

from contracts.pool_weighted.ExternalWeightedProtocolFees import ExternalWeightedProtocolFees

import contracts.interfaces.SymmetricEnums as Enums
    
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
        "uUSD": (sp.address('KT1XnTn74bUtxHfDtBmm2bGZAQfhPbvKWR8p'), sp.some(sp.nat(0))),
        "uBTC": (sp.address('KT1XnTn74bUtxHfDtBmm2bGZAQfhPbvKWR8p'), sp.some(sp.nat(2))),
        "uXTZ": (sp.address('KT1XnTn74bUtxHfDtBmm2bGZAQfhPbvKWR8p'), sp.some(sp.nat(3))),
        "YOU": (sp.address('KT1Xobej4mc6XgEjDoJoHtTKgbD1ELMvcQuL'), sp.some(sp.nat(0))),
        "tzBTC": (sp.address('KT1PWx2mnDueood7fEmfbBDKx1D9BAnnXitn'), sp.none),
        "PLY": (sp.address('KT1GRSvLoikDsXujKgZPsGLX8k8VvR2Tq95b'), sp.none),
        "wUSDC":  (sp.address('KT18fp5rcTW7mbWDmzFwjLDUhs5MeJmagDSZ'), sp.some(sp.nat(17))),
    }

DECIMALS = {
        "SYMM": 18,
        "CTZ": 18,
        "USDT": 6,
        "uUSD": 6,
        "uBTC": 8,
        "uXTZ": 18,
        "YOU": 18,
        "tzBTC": 8,
        "PLY": 18,
        "wUSDC": 6,
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

# Mock prices for tokens
PRICES = {
        "SYMM": 1,
        "CTZ": 1.2,
        "USDT": 1,
        "uUSD": 1,
        "uBTC": 50000,
        "uXTZ": 3,
        "YOU": 2,
        "tzBTC": 50000,
        "PLY": 0.5,
        "wUSDC": 1,
    }

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
def normalize_metadata(metadata):
        meta = {}
        for key in metadata:
            meta[key] = sp.utils.bytes_of_string(metadata[key])

        return meta




def setup_test_pools(factory):
    
    def create_pool(tokens_list, swapFeePercentage, weights_list):
        assert len(tokens_list) == len(weights_list), "Tokens and weights list lengths must match"
        
        tokens_map = {}
        normalizedWeights_map = {}
        tokenDecimals_map = {}
        rateProviders_map = {}
        
        for idx, token_key in enumerate(tokens_list):
            tokens_map[idx] = TOKENS[token_key]
            normalizedWeights_map[idx] = sp.nat(int(weights_list[idx] * (10 ** 18)))
            tokenDecimals_map[idx] = sp.nat(DECIMALS[token_key])
            rateProviders_map[idx] = RATE_PROVIDERS[token_key]
            
        factory.create(
            tokens=sp.map(tokens_map),
            normalizedWeights=sp.map(normalizedWeights_map),
            tokenDecimals=sp.map(tokenDecimals_map),
            rateProviders=sp.some(sp.map(rateProviders_map)),
            swapFeePercentage=sp.nat(int(swapFeePercentage * (10 ** 18))),
            metadata=sp.utils.bytes_of_string("<ipfs://....>"),
            token_metadata=normalize_metadata(TOKEN_METADATA)
        )
        address = factory.data.lastPool

        factory.initialize()

        return address
    
    # Pools with varied weights
    pool_1 = create_pool(["SYMM", "CTZ"], 0.01, [0.6, 0.4])
    # pool_2 = create_pool(["SYMM", "USDT", "uBTC"], 0.02, [0.3, 0.5, 0.2])
    # pool_3 = create_pool(["SYMM", "USDT", "uBTC", "uXTZ"], 0.025, [0.25, 0.25, 0.3, 0.2])
    # pool_4 = create_pool(["SYMM", "USDT", "uBTC", "uXTZ", "YOU"], 0.03, [0.2, 0.2, 0.2, 0.2, 0.2])
    # pool_5 = create_pool(["SYMM", "USDT", "uBTC", "uXTZ", "YOU", "tzBTC"], 0.035, [0.2, 0.15, 0.15, 0.15, 0.15, 0.2])
    # pool_6 = create_pool(["SYMM", "USDT", "uBTC", "uXTZ", "YOU", "tzBTC", "PLY"], 0.04, [0.15, 0.15, 0.15, 0.1, 0.1, 0.1, 0.25])
    # pool_7 = create_pool(["SYMM", "USDT", "uBTC", "uXTZ", "YOU", "tzBTC", "PLY", "wUSDC"], 0.045, [0.15, 0.1, 0.1, 0.1, 0.1, 0.1, 0.15, 0.2])

    return {
        "pool_1": {
          "pool_id": sp.pair(pool_1, sp.nat(1)),
          "tokens": {
            0: TOKENS['SYMM'],
            1: TOKENS['CTZ'],
          },
          "decimals": {
            0: DECIMALS['SYMM'],
            1: DECIMALS['CTZ'],
            },
          "weights": [0.6, 0.4],
          },
        # "pool_2": {
        #   "pool_id": sp.pair(pool_2, sp.nat(2)),
        #   "tokens": {
        #     0: TOKENS['SYMM'],
        #     1: TOKENS['USDT'],
        #     2: TOKENS['uBTC'],
        #   },
        #   "decimals": {
        #     0: DECIMALS['SYMM'],
        #     1: DECIMALS['CTZ'],
        #     2: DECIMALS['uBTC'],
        #     },
        #   "weights": [0.3, 0.5, 0.2],
        #   },
        # "pool_3": {
        #   "pool_id": sp.pair(pool_3, sp.nat(3)),
        #   "tokens": {
        #     0: TOKENS['SYMM'],
        #     1: TOKENS['USDT'],
        #     2: TOKENS['uBTC'],
        #     3: TOKENS['uXTZ'],
        #   },
        #   "decimals": {
        #     0: DECIMALS['SYMM'],
        #     1: DECIMALS['USDT'],
        #     2: DECIMALS['uBTC'],
        #     3: DECIMALS['uXTZ'],
        #   },
        #   "weights": [0.25, 0.25, 0.3, 0.2],
        #   },
        # "pool_4": {
        #   "pool_id": sp.pair(pool_4, sp.nat(4)),
        #   "tokens": {
        #     0: TOKENS['SYMM'],
        #     1: TOKENS['USDT'],
        #     2: TOKENS['uBTC'],
        #     3: TOKENS['uXTZ'],
        #     4: TOKENS['YOU'],
        #   },
        #   "decimals": {
        #     0: DECIMALS['SYMM'],
        #     1: DECIMALS['USDT'],
        #     2: DECIMALS['uBTC'],
        #     3: DECIMALS['uXTZ'],
        #     4: DECIMALS['YOU'],
        #   },
        #   "weights": [0.2, 0.2, 0.2, 0.2, 0.2],
        #   },
        # "pool_5": {
        #   "pool_id": sp.pair(pool_5, sp.nat(5)),
        #   "tokens": {
        #     0: TOKENS['SYMM'],
        #     1: TOKENS['USDT'],
        #     2: TOKENS['uBTC'],
        #     3: TOKENS['uXTZ'],
        #     4: TOKENS['YOU'],
        #     5: TOKENS['tzBTC'],
        #   },
        #   "decimals": {
        #     0: DECIMALS['SYMM'],
        #     1: DECIMALS['USDT'],
        #     2: DECIMALS['uBTC'],
        #     3: DECIMALS['uXTZ'],
        #     4: DECIMALS['YOU'],
        #     5: DECIMALS['tzBTC'],
        #   },
        #   "weights": [0.2, 0.15, 0.15, 0.15, 0.15, 0.2],
        #   },
        # "pool_6": {
        #   "pool_id": sp.pair(pool_6, sp.nat(6)),
        #   "tokens": {
        #     0: TOKENS['SYMM'],
        #     1: TOKENS['USDT'],
        #     2: TOKENS['uBTC'],
        #     3: TOKENS['uXTZ'],
        #     4: TOKENS['YOU'],
        #     5: TOKENS['tzBTC'],
        #     6: TOKENS['PLY'],
        #   },
        #   "decimals": {
        #     0: DECIMALS['SYMM'],
        #     1: DECIMALS['USDT'],
        #     2: DECIMALS['uBTC'],
        #     3: DECIMALS['uXTZ'],
        #     4: DECIMALS['YOU'],
        #     5: DECIMALS['tzBTC'],
        #     6: DECIMALS['PLY'],
        #   },
        #   "weights": [0.15, 0.15, 0.15, 0.1, 0.1, 0.1, 0.25],
        #   },
        # "pool_7": {
        #   "pool_id": sp.pair(pool_7, sp.nat(7)),
        #   "tokens": {
        #     0: TOKENS['SYMM'],
        #     1: TOKENS['USDT'],
        #     2: TOKENS['uBTC'],
        #     3: TOKENS['uXTZ'],
        #     4: TOKENS['YOU'],
        #     5: TOKENS['tzBTC'],
        #     6: TOKENS['PLY'],
        #     7: TOKENS['wUSDC'],
        #   },
        #   "decimals": {
        #     0: DECIMALS['SYMM'],
        #     1: DECIMALS['USDT'],
        #     2: DECIMALS['uBTC'],
        #     3: DECIMALS['uXTZ'],
        #     4: DECIMALS['YOU'],
        #     5: DECIMALS['tzBTC'],
        #     6: DECIMALS['PLY'],
        #     7: DECIMALS['wUSDC'],
        #   },
        #   "weights": [0.15, 0.1, 0.1, 0.1, 0.1, 0.1, 0.15, 0.2],
        #   },
    }

def add_test_liquidity(pools, vault):
    sender = sp.test_account('sender').address
    recipient = sender

    BASE_AMOUNT = 10  # Representing 1 in the 18 decimal format

    # Loop through each pool and add liquidity
    for pool_name, pool_data in pools.items():

        amountsIn = {}
        limits = {}

        for token_idx, token_value in pool_data["tokens"].items():

            # for key, value in  TOKENS.items():
                # if value == token_value:
                    
            token_key = "SYMM"

                    
            weight = pool_data["weights"][token_idx]
            decimal = pool_data["decimals"][token_idx]
            mock_price = PRICES[token_key]
            amount = int(BASE_AMOUNT * weight * mock_price)

            # Adjust for token decimals
            #amountsIn[token_idx] = sp.nat(1000000000000000000000)
            amountsIn[token_idx] = sp.nat(int(amount * (10 ** decimal)))
            limits[token_idx] = sp.nat(int(amount * (10 ** (decimal + 2)))) 
            #limits[token_idx] = sp.nat(100000000000000000000000)  # +2 for 100x limit


        
        userData = sp.record(
            kind=Enums.INIT,
            amountsIn=sp.some(amountsIn),
            minSPTAmountOut=sp.none,
            tokenIndex=sp.none,
            sptAmountOut=sp.none,
            allT=sp.none,
        )

        request = sp.record(
            userData=userData,
            assets=pool_data["tokens"],
            limits=limits,
        )

        vault.joinPool(
            sp.record(
                poolId=pool_data["pool_id"],
                sender=sender,
                recipient=recipient,
                request=request,
            )
        ).run(source=sender)


# def add_test_liquidity(pools, vault):
#     sender = sp.test_account('sender').address
#     recipient = sender

#     amountsIn = {
#         0: sp.nat(1000000000000000000000),
#         1: sp.nat(1000000000000000000000),
#     }

#     userData = sp.record(
#         kind=Enums.INIT,
#         amountsIn=sp.some(amountsIn),
#         minSPTAmountOut=sp.none,
#         tokenIndex=sp.none,
#         sptAmountOut=sp.none,
#         allT=sp.none,
#     )

#     limits = {
#         0: 100000000000000000000000,
#         1: 100000000000000000000000,
#     }

#     request = sp.record(
#         userData=userData,
#         assets=pools["pool_1"]["tokens"],
#         limits=limits,
#     )

#     vault.joinPool(
#         sp.record(
#             poolId=pools["pool_1"]["pool_id"],
#             sender=sender,
#             recipient=recipient,
#             request=request,
#         )
#     )