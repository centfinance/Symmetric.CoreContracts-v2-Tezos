import smartpy as sp

# import contracts.interfaces.SymmetricErrors as Errors

from contracts.vault.PoolRegistry import PoolRegistry

from contracts.vault.balances.MinimalSwapInfoPoolsBalance import MinimalSwapInfoPoolsBalance


class Types:
    REGISTER_TOKENS_PARAMS = sp.TRecord(
        poolId=sp.TBytes,
        tokens=sp.TSet(sp.TRecord(address=sp.TAddress, id=sp.TNat)),
        assetManagers=sp.TList(sp.TAddress)
    )


class PoolTokens(
    PoolRegistry,
    MinimalSwapInfoPoolsBalance
):
    def __init__(self):
        PoolRegistry.__init__(self)
        MinimalSwapInfoPoolsBalance.__init__(self)

    @sp.entry_point
    def registerTokens(self, params):
        sp.set_type(params, Types.REGISTER_TOKENS_PARAMS)

        specialization = self._getSpecialization(params.poolId)

        # with sp.if_(specialization == sp.nat(2)):
        #     sp.verify(sp.len(params.tokens) == sp.nat(
        #         2, Errors.TOKENS_LENGTH_MUST_BE_2))
        #     self._registerTwoTokenPoolTokens(
        #         params.poolId, params.tokens[0], params.tokens[1])
        with sp.if_(specialization == sp.nat(1)):
            self._registerMinimalSwapInfoPoolTokens(
                sp.record(
                    poolId=params.poolId,
                    tokens=params.tokens
                ))
        # with sp.else_():
        #     self._registerGeneralPool(params.poolId, params.tokens)

        poolEvent = sp.record(
            poolId=params.poolId,
            tokens=params.tokens,
            specialization=specialization
        )
        sp.emit(poolEvent, tag='TokensRegistered', with_type=True)
