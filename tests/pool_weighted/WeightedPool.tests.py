import smartpy as sp

from contracts.pool_weighted.WeightedPool import WeightedPool


TOKEN = sp.TRecord(
    address=sp.TAddress,
    id=sp.TNat,
    FA2=sp.TBool,
)

FEE_CACHE = sp.TRecord(
    swapFee=sp.TNat,
    yieldFee=sp.TNat,
    aumFee=sp.TNat,
)

STORAGE = sp.TRecord(
    normalizedWeights=sp.TMap(sp.TNat, sp.TNat),
    scalingFactors=sp.TMap(sp.TNat, sp.TNat),
    tokens=sp.TMap(sp.TNat, TOKEN),
    totalTokens=sp.TNat,
    athRateProduct=sp.TNat,
    balances=sp.TBigMap(sp.TAddress, sp.TRecord(
        approvals=sp.TMap(sp.TAddress, sp.TNat),
        balance=sp.TNat)),
    exemptFromYieldFees=sp.TBool,
    feeCache=FEE_CACHE,
    initialized=sp.TBool,
    metadata=sp.TBigMap(sp.TString, sp.TBytes),
    poolId=sp.TOption(sp.TBytes),
    postJoinExitInvariant=sp.TNat,
    protocolFeesCollector=sp.TOption(sp.TAddress),
    rateProviders=sp.TMap(sp.TNat, sp.TOption(sp.TAddress)),
    swapFeePercentage=sp.TNat,
    swapGivenIn=sp.TNat,
    swapGivenOut=sp.TNat,
    token_metadata=sp.TBigMap(sp.TNat, sp.TRecord(
        token_id=sp.TNat,
        token_info=sp.TMap(sp.TString, sp.TBytes))),
    totalSupply=sp.TNat,
    vault=sp.TAddress,
    getTokenValue=sp.TLambda(sp.TTuple(
        TOKEN,
        sp.TMap(sp.TNat, TOKEN),
        sp.TMap(sp.TNat, sp.TNat)), sp.TNat),
)


class MockVault(sp.Contract):

    def __init__(self):
        self.init(
            nonce=sp.nat(0),
            poolId=sp.bytes("0x0dae12"),
            tokens_set=False
        )

    @sp.onchain_view()
    def getNextNonce(self):
        sp.result(self.data.nonce)

    @sp.entry_point
    def registerPool(self, specialization):
        sp.set_type(specialization, sp.TNat)
        self.data.poolId = self._toPoolId(
            sp.sender, specialization, self.data.nonce)
        self.data.nonce += 1

    @sp.entry_point
    def registerTokens(self, params):
        sp.set_type(params, sp.TRecord(
            poolId=sp.TBytes,
            tokens=sp.TMap(sp.TNat, sp.TRecord(
                address=sp.TAddress, id=sp.TNat, FA2=sp.TBool)),
            assetManagers=sp.TOption(sp.TMap(sp.TNat, sp.TAddress))
        ))
        pass

    def _toPoolId(self, pool, specialization, nonce):
        pack = sp.record(nonce=nonce, pool=pool, specialization=specialization)
        return sp.pack(pack)


class MockWeightedPool(WeightedPool):

    def __init__(
        self,
        vault,
        name,
        symbol,
    ):
        WeightedPool.__init__(
            self,
            vault,
            name,
            symbol,
        )
        self.update_initial_storage(
            swapGivenIn=sp.nat(0),
            swapGivenOut=sp.nat(0),
        )
        self.init_type(STORAGE)

    @sp.entry_point
    def test_onSwapGivenIn(self, params):
        sp.set_type(params, sp.TRecord(
            currentBalanceTokenIn=sp.TNat,
            currentBalanceTokenOut=sp.TNat,
            swapRequest=sp.TRecord(
                tokenIn=TOKEN,
                tokenOut=TOKEN,
                amount=sp.TNat,
            )))
        swapGivenIn = self._onSwapGivenIn(params)
        self.data.swapGivenIn = swapGivenIn

    @sp.entry_point
    def test_onSwapGivenOut(self, params):
        sp.set_type(params, sp.TRecord(
            currentBalanceTokenIn=sp.TNat,
            currentBalanceTokenOut=sp.TNat,
            swapRequest=sp.TRecord(
                tokenIn=TOKEN,
                tokenOut=TOKEN,
                amount=sp.TNat,
            )))
        swapGivenOut = self._onSwapGivenOut(params)
        self.data.swapGivenOut = swapGivenOut


@ sp.add_test(name="WeightedPoolTest_1", profile=True)
def test():
    sc = sp.test_scenario()

    v = MockVault()
    sc += v

    tokens = sp.map({
        0: sp.record(address=sp.address('tz1'), id=sp.nat(0), FA2=False),
        1: sp.record(address=sp.address('tz1'), id=sp.nat(1), FA2=False),
    })

    weights = sp.map({
        0: sp.nat(500000000000000000),
        1: sp.nat(500000000000000000),
    })

    decimals = sp.map({
        0: sp.nat(3),
        1: sp.nat(12),
    })

    rateProviders = sp.map({
        0: sp.none,
        1: sp.none,
    })

    p = MockWeightedPool(
        vault=v.address,
        name="Symm Liqudidty Pool Token",
        symbol="SYMMLP",
    )

    sc += p

    p.initialize(
        sp.record(
            tokens=tokens,
            normalizedWeights=weights,
            tokenDecimals=decimals,
            swapFeePercentage=sp.nat(15000000000000000),
            rateProviders=rateProviders,
        )
    )

    p.test_onSwapGivenIn(
        sp.record(
            currentBalanceTokenIn=sp.nat(1000000000000000000),
            currentBalanceTokenOut=sp.nat(1000000000000000000),
            swapRequest=sp.record(
                tokenIn=tokens[0],
                tokenOut=tokens[1],
                amount=sp.nat(212340000000000000),
            )
        )
    )

    p.test_onSwapGivenOut(
        sp.record(
            currentBalanceTokenIn=sp.nat(1000000000000000000),
            currentBalanceTokenOut=sp.nat(1000000000000000000),
            swapRequest=sp.record(
                tokenIn=tokens[0],
                tokenOut=tokens[1],
                amount=sp.nat(212340000000000000),
            )
        )
    )


@sp.add_test(name="BaseMinimalSwapInfoPoolTest_1", profile=True)
def test():
    sc = sp.test_scenario()

    v = MockVault()
    sc += v

    tokens = sp.map({
        0: sp.record(address=sp.address('tz1'), id=sp.nat(0), FA2=False),
        1: sp.record(address=sp.address('tz1'), id=sp.nat(1), FA2=False),
    })

    weights = sp.map({
        0: sp.nat(500000000000000000),
        1: sp.nat(500000000000000000),
    })

    decimals = sp.map({
        0: sp.nat(3),
        1: sp.nat(12),
    })

    rateProviders = sp.map({
        0: sp.none,
        1: sp.none,
    })

    p = MockWeightedPool(
        vault=v.address,
        name="Symm Liqudidty Pool Token",
        symbol="SYMMLP",
    )

    sc += p

    p.initialize(
        sp.record(
            tokens=tokens,
            normalizedWeights=weights,
            tokenDecimals=decimals,
            swapFeePercentage=sp.nat(15000000000000000),
            rateProviders=rateProviders,
        )
    )

    swapParams = sp.record(
        request=sp.record(
            kind='GIVEN_IN',
            tokenIn=tokens[0],
            tokenOut=tokens[1],
            amount=sp.nat(100000000000000000)
        ),
        balanceTokenIn=sp.nat(1000000000000000000),
        balanceTokenOut=sp.nat(1000000000000000000),
    )

    amount = p.onSwap(swapParams)
    sc.verify(amount == 89667728720983158)

    swapParams2 = sp.record(
        request=sp.record(
            kind='GIVEN_OUT',
            tokenIn=tokens[0],
            tokenOut=tokens[1],
            amount=sp.nat(100000000000000000)
        ),
        balanceTokenIn=sp.nat(1000000000000000000),
        balanceTokenOut=sp.nat(1000000000000000000),
    )

    amount = p.onSwap(swapParams2)
    sc.verify(amount == 112803158488437678)
