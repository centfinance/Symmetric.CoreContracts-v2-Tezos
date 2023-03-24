import smartpy as sp

from contracts.vault.Vault import Vault

from contracts.pool_weighted.WeightedPool import WeightedPool

from contracts.pool_weighted.WeightedPoolFactory import WeightedPoolFactory

from contracts.pool_weighted.ExternalWeightedMath import ExternalWeightedMath


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

    m = ExternalWeightedMath()
    sc += m

    CONTRACT_METADATA = {
        "": "ipfs://QmbEE3NYTuhE2Vk8sQap4kkKyFQ2P1X6GDRCufxDCpBkLa",
    }
    v = Vault(
        CONTRACT_METADATA,
    )
    sc += v

    p = WeightedPool(
        vault=v.address,
        name="Symm Liqudidty Pool Token",
        symbol="SYMMLP",
        weightedMathLib=m.address,
    )

    sc += p

    rp = MockRateProvider()

    sc += rp

    tokens = sp.map({
        0: sp.record(address=sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), id=sp.nat(0), FA2=False),
        1: sp.record(address=sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), id=sp.nat(1), FA2=False),
    })

    weights = sp.map({
        0: sp.nat(500000000000000000),
        1: sp.nat(500000000000000000),
    })

    decimals = sp.map({
        0: sp.nat(18),
        1: sp.nat(18),
    })

    rateProviders = sp.map({
        0: sp.none,
        1: sp.some(rp.address),
    })

    feeCache=sp.record(
        swapFee=sp.nat(40000000000000000),
        yieldFee=sp.nat(40000000000000000),
        aumFee=sp.nat(0),
    )

    p.initialize(
        sp.record(
            tokens=tokens,
            normalizedWeights=weights,
            tokenDecimals=decimals,
            swapFeePercentage=sp.nat(1500000000000000),
            rateProviders=rateProviders,
            feeCache=feeCache,
        )
    )

    sender = sp.test_account('sender').address
    recipient = sender

    amountsIn = {
        0: sp.nat(1000000000000000000),
        1: sp.nat(1000000000000000000),
    }
    1000000999999
    1000000000000000000
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
    }

    request = sp.record(
        userData=userData,
        assets=tokens,
        limits=limits,
        useInternalBalance=False,
    )

    v.joinPool(
        sp.record(
            poolId=sp.bytes(
                '0x050707000107070a0000001601d1371b91c60c441cf7678f644fb63e2a78b0e951000002'),
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
            poolId=sp.bytes(
                '0x050707000107070a0000001601d1371b91c60c441cf7678f644fb63e2a78b0e951000002'),
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
            poolId=sp.bytes(
                '0x050707000107070a0000001601d1371b91c60c441cf7678f644fb63e2a78b0e951000002'),
            sender=sender,
            recipient=recipient,
            request=exitRequest,
        )
    )

    singleSwap = sp.record(
        poolId=sp.bytes(
            '0x050707000107070a0000001601d1371b91c60c441cf7678f644fb63e2a78b0e951000002'),
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
            poolId=sp.bytes(
                '0x050707000107070a0000001601d1371b91c60c441cf7678f644fb63e2a78b0e951000002'),
            sender=sender,
            recipient=recipient,
            request=joinRequest,
        )
    )