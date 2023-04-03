import smartpy as sp

from contracts.vault.Vault import Vault

from contracts.pool_weighted.WeightedPool import WeightedPool

from contracts.pool_weighted.WeightedPoolFactory import WeightedPoolFactory

from contracts.pool_weighted.ExternalWeightedMath import ExternalWeightedMath

from contracts.pool_weighted.ExternalWeightedProtocolFees import ExternalWeightedProtocolFees


def normalize_metadata(metadata):
    meta = {}
    for key in metadata:
        meta[key] = sp.utils.bytes_of_string(metadata[key])

    return meta


class MockRateProvider(sp.Contract):
    def __init__(self):
        sp.Contract.__init__(self)

    @sp.onchain_view()
    def getRate(self):
        sp.result(sp.nat(1100000000000000000))


@sp.add_test(name="VaultIntegrationTest_1", profile=True)
def test():
    sc = sp.test_scenario()
    admin = sp.test_account('Admin')

    m = ExternalWeightedMath()
    sc += m

    pf = ExternalWeightedProtocolFees()
    sc += pf

    CONTRACT_METADATA = {
        "": "ipfs://QmbEE3NYTuhE2Vk8sQap4kkKyFQ2P1X6GDRCufxDCpBkLa",
    }
    v = Vault(
        admin.address,
        CONTRACT_METADATA,
    )
    sc += v

    p = WeightedPool(
        owner=admin.address,
        vault=v.address,
        name="Symm Liqudidty Pool Token",
        symbol="SYMMLP",
        weightedMathLib=m.address,
        weightedProtocolFeesLib=pf.address,
    )

    sc += p

    rp = MockRateProvider()

    sc += rp

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

    rateProviders = sp.map({
        0: sp.none,
        1: sp.some(rp.address),
        2: sp.none,
        3: sp.none,
        4: sp.none,
        5: sp.none,
        6: sp.none,
        7: sp.none,
    })

    p.initialize(
        sp.record(
            tokens=tokens,
            normalizedWeights=weights,
            tokenDecimals=decimals,
            swapFeePercentage=sp.nat(1500000000000000),
            rateProviders=rateProviders,
        )
    )

    sender = sp.test_account('sender').address
    recipient = sender

    amountsIn = {
        0: sp.nat(1000000000000000000),
        1: sp.nat(1000000000000000000),
        2: sp.nat(1000000000000000000),
        3: sp.nat(1000000000000000000),
        4: sp.nat(1000000000000000000),
        5: sp.nat(1000000000000000000),
        6: sp.nat(1000000000000000000),
        7: sp.nat(1000000000000000000),
    }

    userData = sp.record(
        kind='INIT',
        amountsIn=sp.some(amountsIn),
        minSPTAmountOut=sp.none,
        tokenIndex=sp.none,
        sptAmountOut=sp.none,
        allT=sp.none,
    )

    limits = {
        0: 100000000000000000000,
        1: 100000000000000000000,
        2: 100000000000000000000,
        3: 100000000000000000000,
        4: 100000000000000000000,
        5: 100000000000000000000,
        6: 100000000000000000000,
        7: 100000000000000000000,
    }

    request = sp.record(
        userData=userData,
        assets=tokens,
        limits=limits,
        useInternalBalance=False,
    )

    v.joinPool(
        sp.record(
            poolId=sp.pair(sp.address(
                'KT1Tezooo3zzSmartPyzzSTATiCzzzseJjWC'), sp.nat(1)),
            sender=sender,
            recipient=recipient,
            request=request,
        )
    )

    joinUserData = sp.record(
        kind='EXACT_TOKENS_IN_FOR_SPT_OUT',
        amountsIn=sp.some(amountsIn),
        minSPTAmountOut=sp.some(sp.nat(1)),
        tokenIndex=sp.none,
        sptAmountOut=sp.none,
        allT=sp.none,
    )

    joinRequest = sp.record(
        userData=joinUserData,
        assets=tokens,
        limits=limits,
        useInternalBalance=False,
    )

    v.joinPool(
        sp.record(
            poolId=sp.pair(sp.address(
                'KT1Tezooo3zzSmartPyzzSTATiCzzzseJjWC'), sp.nat(1)),
            sender=sender,
            recipient=recipient,
            request=joinRequest,
        )
    )

    exitUserData = sp.record(
        kind='EXACT_SPT_IN_FOR_TOKENS_OUT',
        amountsOut=sp.none,
        maxSPTAmountIn=sp.none,
        sptAmountIn=sp.some(sp.nat(999999997888455688)),
        tokenIndex=sp.none,
        recoveryModeExit=False,
    )

    exitRequest = sp.record(
        userData=exitUserData,
        assets=tokens,
        limits=limits,
        useInternalBalance=False,
    )

    v.exitPool(
        sp.record(
            poolId=sp.pair(sp.address(
                'KT1Tezooo3zzSmartPyzzSTATiCzzzseJjWC'), sp.nat(1)),
            sender=sender,
            recipient=recipient,
            request=exitRequest,
        )
    )

    singleSwap = sp.record(
        poolId=sp.pair(sp.address(
            'KT1Tezooo3zzSmartPyzzSTATiCzzzseJjWC'), sp.nat(1)),
        kind='GIVEN_IN',
        assetIn=tokens[0],
        assetOut=tokens[1],
        amount=sp.nat(100000000000000000),
    )

    funds = sp.record(
        sender=sender,
        fromInternalBalance=False,
        recipient=recipient,
        toInternalBalance=False,
    )

    swapParams = sp.record(
        singleSwap=singleSwap,
        funds=funds,
        limit=sp.nat(0),
        deadline=sp.timestamp(1)
    )

    v.swap(swapParams)

    supply = p.getActualSupply()
    sc.show(supply)

    v.joinPool(
        sp.record(
            poolId=sp.pair(sp.address(
                'KT1Tezooo3zzSmartPyzzSTATiCzzzseJjWC'), sp.nat(1)),
            sender=sender,
            recipient=recipient,
            request=joinRequest,
        )
    )

    swaps = {
        0: sp.record(
            poolId=sp.pair(sp.address(
                'KT1Tezooo3zzSmartPyzzSTATiCzzzseJjWC'), sp.nat(1)),
            assetInIndex=1,
            assetOutIndex=0,
            amount=sp.nat(100000000000000000),
        ),
        1: sp.record(
            poolId=sp.pair(sp.address(
                'KT1Tezooo3zzSmartPyzzSTATiCzzzseJjWC'), sp.nat(1)),
            assetInIndex=2,
            assetOutIndex=3,
            amount=sp.nat(125700000500000000),
        ),
        2: sp.record(
            poolId=sp.pair(sp.address(
                'KT1Tezooo3zzSmartPyzzSTATiCzzzseJjWC'), sp.nat(1)),
            assetInIndex=4,
            assetOutIndex=5,
            amount=sp.nat(118300000500000000),
        ),
        3: sp.record(
            poolId=sp.pair(sp.address(
                'KT1Tezooo3zzSmartPyzzSTATiCzzzseJjWC'), sp.nat(1)),
            assetInIndex=7,
            assetOutIndex=6,
            amount=sp.nat(100000000000000000),
        ),
    }

    swapLimits = {
        0: 10000000000000000000000,
        1: 10000000000000000000000,
        2: 10000000000000000000000,
        3: 10000000000000000000000,
        4: 10000000000000000000000,
        5: 10000000000000000000000,
        6: 10000000000000000000000,
        7: 10000000000000000000000,
    }

    v.batchSwap(sp.record(
        kind='GIVEN_IN',
        swaps=swaps,
        assets=tokens,
        funds=funds,
        limits=swapLimits,
        deadline=sp.timestamp(1),
    ))
