import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

from contracts.vault.PoolRegistry import PoolRegistry

from contracts.vault.balances.MinimalSwapInfoPoolsBalance import MinimalSwapInfoPoolsBalance

from contracts.vault.balances.TwoTokenPoolsBalance import TwoTokenPoolsBalance

from contracts.vault.balances.GeneralPoolsBalance import GeneralPoolsBalance


class Types:
    TOKEN = sp.TRecord(
        address=sp.TAddress,
        id=sp.TNat,
        FA2=sp.TBool,
    )
    REGISTER_TOKENS_PARAMS = sp.TRecord(
        poolId=sp.TBytes,
        tokens=sp.TMap(sp.TNat, TOKEN),
        assetManagers=sp.TList(sp.TAddress)
    )


class PoolTokens(
    PoolRegistry,
    MinimalSwapInfoPoolsBalance,
    TwoTokenPoolsBalance,
    GeneralPoolsBalance
):
    def __init__(self):
        PoolRegistry.__init__(self)
        MinimalSwapInfoPoolsBalance.__init__(self)
        TwoTokenPoolsBalance.__init__(self)
        GeneralPoolsBalance.__init__(self)

    @sp.entry_point
    def registerTokens(self, params):
        sp.set_type(params, Types.REGISTER_TOKENS_PARAMS)

        # specialization = self._getPoolSpecialization(params.poolId)

        # with sp.if_(specialization == sp.nat(2)):
        #     sp.verify(sp.len(params.tokens) == sp.nat(2),
        #               Errors.TOKENS_LENGTH_MUST_BE_2)
        #     self._registerTwoTokenPoolTokens(sp.record(
        #         poolId=params.poolId,
        #         tokenX=params.tokens[0],
        #         tokenY=params.tokens[1]
        #     ))
        # with sp.if_(specialization == sp.nat(1)):
        self._registerMinimalSwapInfoPoolTokens(
            sp.record(
                poolId=params.poolId,
                tokens=params.tokens
            ))
        # with sp.if_((specialization != sp.nat(2)) & (specialization != sp.nat(1))):
        #     self._registerGeneralPoolTokens(sp.record(
        #         poolId=params.poolId,
        #         tokens=params.tokens
        #     ))

        poolEvent = sp.record(
            poolId=params.poolId,
            tokens=params.tokens,
            # specialization=specialization
            specialization=sp.nat(1)
        )
        sp.emit(poolEvent, tag='TokensRegistered', with_type=True)

    def _getPoolTokens(self, poolId):
        # specialization = self._getPoolSpecialization(poolId)

        # with sp.if_(specialization == sp.nat(2)):
        #     return self._getTwoTokenPoolTokens(poolId)
        # with sp.if_(specialization == sp.nat(1)):
        return self._getMinimalSwapInfoPoolTokens(poolId)
        # with sp.if_((specialization != sp.nat(2)) & (specialization != sp.nat(1))):
        #     # PoolSpecialization.GENERAL
        #     return self._getGeneralPoolTokens(poolId);
