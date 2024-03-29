import smartpy as sp

from contracts.pool_weighted.BaseWeightedPool import BaseWeightedPool

import contracts.interfaces.SymmetricEnums as Enums

class MockBaseWeightedPool(BaseWeightedPool):
    MAX_TOKENS = 8

    def __init__(
        self,
        owner,
        vault,
        name,
        symbol,
        protocolFeesCollector,
        normalizedWeights
    ):
        self.init(
            normalizedWeights=normalizedWeights,
            result=sp.pair(sp.nat(0), sp.map(
                {}, tkey=sp.TNat, tvalue=sp.TNat)),
        )
        BaseWeightedPool.__init__(
            self,
            owner,
            vault,
            name,
            symbol,
            protocolFeesCollector,
        )

    @sp.entry_point
    def onInitializePool(self, params):
        result = self._onInitializePool(params)
        self._mintPoolTokens(sp.sender, sp.fst(result))
        self.data.result = result

    @sp.entry_point
    def onJoinPool(self, params):
        result = self._onJoinPool(params)
        self.data.result = result

    @sp.entry_point
    def onExitPool(self, params):
        result = self._onExitPool(params)
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
        0: sp.nat(15384756480000000000),
        1: sp.nat(7000000000000000000),
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
        kind=Enums.INIT,
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

    sc.verify(sp.fst(c.data.result) == 20755076034929283936)

    amounts2 = sp.map({
        0: sp.nat(1539244900000000000),
        1: sp.nat(700350000000000000),
    })
    userData2 = sp.record(
        amountsIn=amounts2,
        kind=Enums.EXACT_TOKENS_IN_FOR_SPT_OUT,
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

    userData3 = sp.record(
        amountsIn=amounts2,
        kind=Enums.TOKEN_IN_FOR_EXACT_SPT_OUT,
        minSPTAmountOut=1,
        tokenIndex=0,
        sptAmountOut=1000000000000000000,
        allT=10,
    )
    params3 = sp.record(
        balances=balances,
        scalingFactors=scalingFactors,
        userData=userData3
    )

    c.onJoinPool(params3)

    userData4 = sp.record(
        amountsIn=amounts2,
        kind=Enums.TOKEN_IN_FOR_EXACT_SPT_OUT,
        minSPTAmountOut=1,
        tokenIndex=0,
        sptAmountOut=1000000000000000000,
        allT=1000000000000000000,
    )
    params4 = sp.record(
        balances=balances,
        scalingFactors=scalingFactors,
        userData=userData4,
    )

    c.onJoinPool(params4)

    exitUserData = sp.record(
        kind=Enums.SPT_IN_FOR_EXACT_TOKENS_OUT,
        maxSPTAmountIn=1000000000000000000,
        amountsOut={0: 1000000000000000000, 1: 1000000000000000000},
        tokenIndex=0,
        sptAmountIn=1000000000000000000,
        allT=1000000000000000000,
    )
    exitParams = sp.record(
        balances=balances,
        scalingFactors=scalingFactors,
        userData=exitUserData,
    )
    c.onExitPool(exitParams)

    exitUserData = sp.record(
        kind=Enums.EXACT_SPT_IN_FOR_TOKENS_OUT,
        maxSPTAmountIn=1000000000000000000,
        amountsOut={0: 1000000000000000000, 1: 1000000000000000000},
        tokenIndex=0,
        sptAmountIn=1000000000000000000,
        allT=1000000000000000000,
    )

    exitParams2 = sp.record(
        balances=balances,
        scalingFactors=scalingFactors,
        userData=exitUserData,
    )
    c.onExitPool(exitParams2)

    exitUserData = sp.record(
        kind=Enums.SPT_IN_FOR_EXACT_TOKENS_OUT,
        maxSPTAmountIn=1000000000000000000,
        amountsOut={0: 1000000000000000000, 1: 1000000000000000000},
        tokenIndex=0,
        sptAmountIn=1000000000000000000,
        allT=1000000000000000000,
    )
    exitParams3 = sp.record(
        balances=balances,
        scalingFactors=scalingFactors,
        userData=exitUserData,
    )
    c.onExitPool(exitParams3)
