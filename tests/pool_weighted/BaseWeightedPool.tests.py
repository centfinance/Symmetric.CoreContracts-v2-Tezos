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
        self.data.result = result


@sp.add_test(name="BaseWeightedPoolTest_1", profile=True)
def test():
    sc = sp.test_scenario()

    weights = sp.map({
        0: sp.nat(330000000000000000),
        1: sp.nat(330000000000000000),
        2: sp.nat(340000000000000000),
    })

    amounts = sp.map({
        0: sp.nat(1000000000000000000),
        1: sp.nat(1000000000000000000),
        2: sp.nat(1000000000000000000)
    })

    scalingFactors = sp.map({
        0: sp.nat(1000000000000000000),
        1: sp.nat(1000000000000000000),
        2: sp.nat(1000000000000000000)
    })

    c = MockBaseWeightedPool(
        vault=sp.address("tz1"),
        name="Symm Liqudidty Pool Token",
        symbol="SYMMLP",
        owner=sp.address("tz1"),
        normalizedWeights=weights,
    )

    sc += c

    # userData = sp.record(
    #     amountsIn=amounts,
    #     kind='INIT',
    # )

    # params = sp.record(
    #     userData=userData,
    #     scalingFactors=scalingFactors,
    # )
    # c.onInitializePool(
    #     params
    # )
