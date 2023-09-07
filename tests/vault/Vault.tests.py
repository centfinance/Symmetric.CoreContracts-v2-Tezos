import smartpy as sp

from contracts.vault.Vault import Vault

from contracts.pool_weighted.WeightedPool import WeightedPool

from contracts.pool_weighted.WeightedPoolFactory import WeightedPoolFactory

from contracts.pool_weighted.ExternalWeightedMath import ExternalWeightedMath

from contracts.pool_weighted.ExternalWeightedProtocolFees import ExternalWeightedProtocolFees

import contracts.interfaces.SymmetricEnums as Enums

import tests.helpers.MockSymmetric as helpers 

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
    env = helpers.setup_test_environment()

    sc = env["scenario"]

    v = env["vault"]

    pools = helpers.setup_test_pools(env["pool_factory"])

    tokens = sp.map({
        0: (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.some(sp.nat(0))),
        1: (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.some(sp.nat(1))),
        # 2: (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.some(sp.nat(2))),
        # 3: (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.some(sp.nat(3))),
        # 4: (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.some(sp.nat(4))),
        # 5: (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.some(sp.nat(5))),
        # 6: (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.some(sp.nat(0))),
        # 7: (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.some(sp.nat(6))),
    })

    weights = sp.map({
        0: sp.nat(500000000000000000),
        1: sp.nat(500000000000000000),
        # 2: sp.nat(125000000000000000),
        # 3: sp.nat(125000000000000000),
        # 4: sp.nat(125000000000000000),
        # 5: sp.nat(125000000000000000),
        # 6: sp.nat(125000000000000000),
        # 7: sp.nat(125000000000000000),
    })

    weights2 = sp.map({
        0: sp.nat(600000000000000000),
        1: sp.nat(400000000000000000),
        # 2: sp.nat(125000000000000000),
        # 3: sp.nat(125000000000000000),
        # 4: sp.nat(125000000000000000),
        # 5: sp.nat(125000000000000000),
        # 6: sp.nat(125000000000000000),
        # 7: sp.nat(125000000000000000),
    })

    scalingFactors = sp.map({
        0: sp.nat(1000000000000000000),
        1: sp.nat(1000000000000000000),
        # 2: sp.nat(1000000000000000000),
        # 3: sp.nat(1000000000000000000),
        # 4: sp.nat(1000000000000000000),
        # 5: sp.nat(1000000000000000000),
        # 6: sp.nat(1000000000000000000),
        # 7: sp.nat(1000000000000000000),
    })

    rp = MockRateProvider()

    sc += rp

    rateProviders = sp.some(sp.map({
        0: sp.none,
        1: sp.some(rp.address),
        # 2: sp.none,
        # 3: sp.none,
        # 4: sp.none,
        # 5: sp.none,
        # 6: sp.none,
        # 7: sp.none,
    }))

    p = WeightedPool(
        owner=env["admin"].address,
        vault=env["vault"].address,
        name="Symm Liqudidty Pool Token",
        symbol="SYMMLP",
        weightedMathLib=env["math"].address,
        weightedProtocolFeesLib=env["protocol_fees"].address,
        tokens=tokens,
        normalizedWeights=weights,
        scalingFactors=scalingFactors,
        swapFeePercentage=sp.nat(1500000000000000),
        rateProviders=rateProviders,
        exemptFromYieldFees=False,
        feeCache=(sp.nat(400000000000000000), sp.nat(400000000000000000)),
        protocolFeesCollector=env["fees_collector"].address,
    )

    sc += p

    p.initializePool()

    p2 = WeightedPool(
        owner=env["admin"].address,
        vault=env["vault"].address,
        name="Symm Liqudidty Pool Token",
        symbol="SYMMLP",
        weightedMathLib=env["math"].address,
        weightedProtocolFeesLib=env["protocol_fees"].address,
        tokens=tokens,
        normalizedWeights=weights2,
        scalingFactors=scalingFactors,
        swapFeePercentage=sp.nat(1500000000000000),
        rateProviders=rateProviders,
        exemptFromYieldFees=False,
        feeCache=(sp.nat(400000000000000000), sp.nat(400000000000000000)),
        protocolFeesCollector=env["fees_collector"].address,
    )

    sc += p2

    p2.initializePool()

    sender = sp.test_account('sender').address
    recipient = sender

    amountsIn = {
        0: sp.nat(1000000000000000000000),
        1: sp.nat(1000000000000000000000),
        # 2: sp.nat(1000000000000000000),
        # 3: sp.nat(1000000000000000000),
        # 4: sp.nat(1000000000000000000),
        # 5: sp.nat(1000000000000000000),
        # 6: sp.nat(1000000000000000000),
        # 7: sp.nat(1000000000000000000),
    }

    userData = sp.record(
        kind=Enums.INIT,
        amountsIn=sp.some(amountsIn),
        minSPTAmountOut=sp.none,
        tokenIndex=sp.none,
        sptAmountOut=sp.none,
        allT=sp.none,
    )

    limits = {
        0: 100000000000000000000000,
        1: 100000000000000000000000,
        # 2: 100000000000000000000,
        # 3: 100000000000000000000,
        # 4: 100000000000000000000,
        # 5: 100000000000000000000,
        # 6: 100000000000000000000,
        # 7: 100000000000000000000,
    }

    request = sp.record(
        userData=userData,
        assets=tokens,
        limits=limits,
    )

    v.joinPool(
        sp.record(
            poolId=sp.pair(p.address, sp.nat(2)),
            sender=sender,
            recipient=recipient,
            request=request,
        )
    ).run(source=sender)

    v.joinPool(
        sp.record(
            poolId=sp.pair(p2.address, sp.nat(3)),
            sender=sender,
            recipient=recipient,
            request=request,
        )
    ).run(source=sender)

    joinUserData = sp.record(
        kind=Enums.EXACT_TOKENS_IN_FOR_SPT_OUT,
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
    )

    v.joinPool(
        sp.record(
            poolId=sp.pair(p.address, sp.nat(2)),
            sender=sender,
            recipient=recipient,
            request=joinRequest,
        )
    ).run(source=sender)

    v.joinPool(
        sp.record(
            poolId=sp.pair(p2.address, sp.nat(3)),
            sender=sender,
            recipient=recipient,
            request=joinRequest,
        )
    ).run(source=sender)
    
    exitLimits = {
        0: 1000000,
        1: 1000000,
        # 2: 1000000,
        # 3: 1000000,
        # 4: 1000000,
        # 5: 1000000,
        # 6: 1000000,
        # 7: 1000000,
    }
    exitUserData = sp.record(
        kind=Enums.EXACT_SPT_IN_FOR_TOKENS_OUT,
        amountsOut=sp.none,
        maxSPTAmountIn=sp.none,
        sptAmountIn=sp.some(sp.nat(999999997888455688)),
        tokenIndex=sp.none,
        recoveryModeExit=False,
    )

    exitRequest = sp.record(
        userData=exitUserData,
        assets=tokens,
        limits=exitLimits,
    )

    v.exitPool(
        sp.record(
            poolId=sp.pair(p.address, sp.nat(2)),
            sender=sender,
            recipient=recipient,
            request=exitRequest,
        )
    ).run(source=sender)

    v.exitPool(
        sp.record(
            poolId=sp.pair(p2.address, sp.nat(3)),
            sender=sender,
            recipient=recipient,
            request=exitRequest,
        )
    ).run(source=sender)

    singleSwap = sp.record(
        poolId=sp.pair(p.address, sp.nat(2)),
        kind=Enums.GIVEN_IN,
        assetIn=tokens[0],
        assetOut=tokens[1],
        amount=sp.nat(1987670000000000000),
    )

    singleSwap2 = sp.record(
        poolId=sp.pair(p2.address, sp.nat(3)),
        kind=Enums.GIVEN_IN,
        assetIn=tokens[0],
        assetOut=tokens[1],
        amount=sp.nat(1987670000000000000),
    )

    funds = sp.record(
        sender=sender,
        recipient=recipient,
    )

    swapParams = sp.record(
        singleSwap=singleSwap,
        funds=funds,
        limit=sp.nat(0),
        deadline=sp.timestamp(1)
    )

    swapParams2 = sp.record(
        singleSwap=singleSwap2,
        funds=funds,
        limit=sp.nat(0),
        deadline=sp.timestamp(1)
    )

    v.swap(swapParams).run(source=sender)

    v.swap(swapParams2).run(source=sender)

    # supply = p.getActualSupply()
    # sc.show(supply)

    # v.joinPool(
    #     sp.record(
    #         poolId=sp.pair(p.address, sp.nat(1)),
    #         sender=sender,
    #         recipient=recipient,
    #         request=joinRequest,
    #     )
    # )

    # swaps = {
    #     0: sp.record(
    #         poolId=sp.pair(p.address, sp.nat(1)),
    #         assetInIndex=1,
    #         assetOutIndex=0,
    #         amount=sp.nat(100000000000000000),
    #     ),
    #     1: sp.record(
    #         poolId=sp.pair(p.address, sp.nat(1)),
    #         assetInIndex=2,
    #         assetOutIndex=3,
    #         amount=sp.nat(125700000500000000),
    #     ),
    #     2: sp.record(
    #         poolId=sp.pair(p.address, sp.nat(1)),
    #         assetInIndex=4,
    #         assetOutIndex=5,
    #         amount=sp.nat(118300000500000000),
    #     ),
    #     3: sp.record(
    #         poolId=sp.pair(p.address, sp.nat(1)),
    #         assetInIndex=7,
    #         assetOutIndex=6,
    #         amount=sp.nat(100000000000000000),
    #     ),
    # }

    # swapLimits = {
    #     0: 10000000000000000000000,
    #     1: 10000000000000000000000,
    #     2: 10000000000000000000000,
    #     3: 10000000000000000000000,
    #     4: 10000000000000000000000,
    #     5: 10000000000000000000000,
    #     6: 10000000000000000000000,
    #     7: 10000000000000000000000,
    # }

    # v.batchSwap(sp.record(
    #     kind='GIVEN_IN',
    #     swaps=swaps,
    #     assets=tokens,
    #     funds=funds,
    #     limits=swapLimits,
    #     deadline=sp.timestamp(1),
    # ))
