import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

import contracts.utils.Utils as Utils

import contracts.vault.balances.BalanceAllocation as BalanceAllocation

from contracts.vault.PoolRegistry import PoolRegistry

# from contracts.vault.balances.MinimalSwapInfoPoolsBalance import MinimalSwapInfoPoolsBalance

# from contracts.vault.balances.TwoTokenPoolsBalance import TwoTokenPoolsBalance

# from contracts.vault.balances.GeneralPoolsBalance import GeneralPoolsBalance


class Types:
    TOKEN = sp.TRecord(
        address=sp.TAddress,
        id=sp.TNat,
        FA2=sp.TBool,
    )

    BALANCE = sp.TRecord(
        cash=sp.TNat,
        managed=sp.TNat,
        lastChangeBlock=sp.TNat,
    )
    REGISTER_TOKENS_PARAMS = sp.TRecord(
        poolId=sp.TBytes,
        tokens=sp.TMap(sp.TNat, TOKEN),
        assetManagers=sp.TOption(sp.TMap(sp.TNat, sp.TAddress))
    )

    TOKENS_TYPE = sp.TMap(sp.TNat, TOKEN)

    BALANCES_TYPE = sp.TMap(TOKEN, BALANCE)


class PoolTokens(
    PoolRegistry,
    # MinimalSwapInfoPoolsBalance,
    # TwoTokenPoolsBalance,
    # GeneralPoolsBalance
):
    def __init__(self):
        self.update_initial_storage(
            poolsTokens=sp.big_map(
                l={},
                tkey=sp.TBytes,
                tvalue=Types.TOKENS_TYPE
            ),
            poolsBalances=sp.big_map(
                l={},
                tkey=sp.TBytes,
                tvalue=Types.BALANCES_TYPE,
            ),
        ),
        PoolRegistry.__init__(self)
        # MinimalSwapInfoPoolsBalance.__init__(self)
        # TwoTokenPoolsBalance.__init__(self)
        # GeneralPoolsBalance.__init__(self)

    @sp.entry_point(lazify=False)
    def registerTokens(self, params):
        sp.set_type(params, Types.REGISTER_TOKENS_PARAMS)
        self.onlyUnpaused()
        # TODO: Refactor
        with sp.if_(self.data.poolsTokens.contains(params.poolId)):
            registeredTokens = self.data.poolsTokens[params.poolId].values(
            )
            tokensAmount = sp.len(params.tokens)
            with sp.for_('i', sp.range(0, tokensAmount)) as i:
                prevSize = sp.len(
                    self.data.poolsTokens[params.poolId])
                t = params.tokens[i]
                sp.verify(Utils.list_contains(registeredTokens, t) == False)
                self.data.poolsTokens[params.poolId][prevSize] = t
        with sp.else_():
            self.data.poolsTokens[params.poolId] = params.tokens
            self.data.poolsBalances[params.poolId] = sp.map(
                l={}, tkey=Types.TOKEN, tvalue=Types.BALANCE)

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
        # self._registerMinimalSwapInfoPoolTokens(
        #     sp.record(
        #         poolId=params.poolId,
        #         tokens=params.tokens
        #     ))
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

    @sp.onchain_view()
    def getPoolTokens(self, poolId):
        sp.set_type(poolId, sp.TBytes)
        (tokens, rawBalances) = self._getPoolTokens(poolId)
        (balances, lastChangeBlock) = BalanceAllocation.totalsAndLastChangeBlock(
            rawBalances)
        sp.result((
            tokens,
            balances,
            lastChangeBlock,
        ))

    def _getPoolTokens(self, poolId):
        poolTokens = self.data.poolsTokens[poolId]
        tokens = sp.compute(sp.map(l={}, tkey=sp.TNat, tvalue=Types.TOKEN))
        balances = sp.compute(
            sp.map(l={}, tkey=sp.TNat, tvalue=Types.BALANCE))

        with sp.for_('i', sp.range(0, sp.len(poolTokens))) as i:
            token = poolTokens[i]
            tokens[i] = token
            balances[i] = self.data.poolsBalances.get(poolId, {}).get(token, sp.record(
                cash=sp.nat(0),
                managed=sp.nat(0),
                lastChangeBlock=sp.level,
            ))

        return (tokens, balances)
        # specialization = self._getPoolSpecialization(poolId)

        # with sp.if_(specialization == sp.nat(2)):
        #     return self._getTwoTokenPoolTokens(poolId)
        # with sp.if_(specialization == sp.nat(1)):
        # return self._getMinimalSwapInfoPoolTokens(poolId)
        # with sp.if_((specialization != sp.nat(2)) & (specialization != sp.nat(1))):
        #     # PoolSpecialization.GENERAL
        #     return self._getGeneralPoolTokens(poolId);

    def _setPoolBalances(
        self,
        params
    ):
        with sp.for_('i', sp.range(0, sp.len(params.tokens))) as i:
            self.data.poolsBalances[params.poolId][params.tokens[i]
                                                   ] = params.balances[i]

    def _getPoolBalance(self, params):
        return self.data.poolsBalances.get(
            params.poolId, message=Errors.INVALID_POOL_ID).get(params.token, message=Errors.TOKEN_NOT_REGISTERED)
