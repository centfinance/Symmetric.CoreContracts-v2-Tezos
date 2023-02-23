import smartpy as sp

from contracts.pool_utils.BasePool import BasePool


class MockBasePool(BasePool):
    MAX_TOKENS = 8

    def __init__(
        self,
        tokens,
        scalingFactors,
        normalizedWeights,
        vault,
        name,
        symbol,
        owner,
    ):
        self.init(
            tokens=tokens,
            scalingFactors=scalingFactors,
            normalizedWeights=normalizedWeights,
            totalTokens=sp.nat(2),
            initialized=sp.bool(True),
        )
        BasePool.__init__(
            self,
            vault,
            name,
            symbol,
            owner,
        )

    def _onInitializePool(self, params):
        return (
            1000000000000000000,
            {
                0: sp.nat(1000000000000000000),
                1: sp.nat(1000000000000000000),
            }
        )

    def _onJoinPool(self, params):
        return (
            1000000000000000000,
            {
                0: sp.nat(1000000000000000000),
                1: sp.nat(1000000000000000000),
            }
        )

    def _doRecoveryModeExit(
            self,
            params
    ):
        pass


@sp.add_test(name="BasePoolTest_1", profile=True)
def test():
    sc = sp.test_scenario()
    vault = sp.test_account('Vault')
    token1 = sp.test_account('token1')
    token2 = sp.test_account('token2')

    tokens = {
        0: sp.record(
            address=token1.address,
            id=0,
        ),
        1: sp.record(
            address=token2.address,
            id=0,
        )
    }
    weights = sp.map({
        0: sp.nat(500000000000000000),
        1: sp.nat(500000000000000000),
    })

    scalingFactors = sp.map({
        0: sp.nat(1000000000000000000),
        1: sp.nat(1000000000000000000),
    })

    c = MockBasePool(
        tokens=tokens,
        scalingFactors=scalingFactors,
        normalizedWeights=weights,
        vault=vault.address,
        name="Symm Liquidity Pool Token",
        symbol="SYMMLP",
        owner=sp.address("tz1"),
    )

    sc += c
