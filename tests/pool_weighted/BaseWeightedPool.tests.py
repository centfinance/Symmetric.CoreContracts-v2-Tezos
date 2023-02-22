import smartpy as sp

from contracts.pool_weighted.BaseWeightedPool import BaseWeightedPool


class MockBaseWeightedPool(BaseWeightedPool):
    MAX_TOKENS = 8

    def __init__(
        self,
        vault,
        name,
        symbol,
        owner,
        normalizedWeights
    ):
        self.init(
            normalizedWeights=normalizedWeights,
            result=sp.pair(sp.nat(0), sp.map(
                {}, tkey=sp.TNat, tvalue=sp.TNat)),
        )
        BaseWeightedPool.__init__(
            self,
            vault,
            name,
            symbol,
            owner,
        )

    @sp.entry_point
    def onInitializePool(self, params):
        result = self._onInitializePool(params)
        self._mintPoolTokens(sp.sender, sp.nat(2000000000000000000))
        self.data.result = result

    @sp.entry_point
    def onJoinPool(self, params):
        result = self._onJoinPool(params)
        self.data.result = result


@sp.add_test(name="BaseWeightedPoolTest_1", profile=True)
def test():
    sc = sp.test_scenario()
    vault = sp.test_account('Vault')

    weights = sp.map({
        0: sp.nat(500000000000000000),
        1: sp.nat(500000000000000000),
    })

    amounts = sp.map({
        0: sp.nat(1538475648000000000),
        1: sp.nat(700000000000000000),
    })

    balances = sp.map({
        0: sp.nat(20538475648000000000),
        1: sp.nat(7800000000000000000),
    })

    scalingFactors = sp.map({
        0: sp.nat(1000000000000000000),
        1: sp.nat(1000000000000000000),
    })

    c = MockBaseWeightedPool(
        vault=sp.address("tz1"),
        name="Symm Liquidity Pool Token",
        symbol="SYMMLP",
        owner=sp.address("tz1"),
        normalizedWeights=weights,
    )

    sc += c

    userData = sp.record(
        amountsIn=amounts,
        kind='INIT',
    )

    params = sp.record(
        userData=userData,
        scalingFactors=scalingFactors,
    )
    c.onInitializePool(
        params
    ).run(
        sender=vault.address
    )

    sc.verify(sp.fst(c.data.result) == 2)

    amounts2 = sp.map({
        0: sp.nat(1539244900000000000),
        1: sp.nat(700350000000000000),
    })
    userData2 = sp.record(
        amountsIn=amounts2,
        kind='EXACT_TOKENS_IN_FOR_SPT_OUT',
        minSPTAmountOut=1,
        tokenIndex=0,
        sptAmountOut=1,
        allT=10,
    )
    params2 = sp.record(
        balances=balances,
        scalingFactors=scalingFactors,
        userData=userData2
    )

    c.onJoinPool(params2)
