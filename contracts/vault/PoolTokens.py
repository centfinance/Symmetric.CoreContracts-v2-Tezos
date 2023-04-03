import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

import contracts.utils.Utils as Utils

import contracts.vault.balances.BalanceAllocation as BalanceAllocation

from contracts.vault.PoolRegistry import PoolRegistry

# from contracts.vault.balances.MinimalSwapInfoPoolsBalance import MinimalSwapInfoPoolsBalance

# from contracts.vault.balances.TwoTokenPoolsBalance import TwoTokenPoolsBalance

# from contracts.vault.balances.GeneralPoolsBalance import GeneralPoolsBalance


class Types:
    # TOKEN = sp.TRecord(
    #     address=sp.TAddress,
    #     id=sp.TNat,
    #     FA2=sp.TBool,
    # )
    TOKEN = sp.TPair(sp.TAddress, sp.TOption(sp.TNat))

    BALANCE = sp.TRecord(
        cash=sp.TNat,
        managed=sp.TNat,
        lastChangeBlock=sp.TNat,
    )
    REGISTER_TOKENS_PARAMS = sp.TRecord(
        poolId=sp.TPair(sp.TAddress, sp.TNat),
        tokens=sp.TMap(sp.TNat, TOKEN),
        assetManagers=sp.TOption(sp.TMap(sp.TNat, sp.TAddress))
    )

    TOKENS_TYPE = sp.TMap(sp.TNat, TOKEN)

    BALANCES_TYPE = sp.TMap(TOKEN, BALANCE)


class PoolTokens(
    PoolRegistry,
):
    def __init__(self):
        self.update_initial_storage(
            poolsTokens=sp.big_map(
                l={},
                tkey=sp.TPair(sp.TAddress, sp.TNat),
                tvalue=Types.TOKENS_TYPE
            ),
            poolsBalances=sp.big_map(
                l={},
                tkey=sp.TPair(sp.TAddress, sp.TNat),
                tvalue=Types.BALANCES_TYPE,
            ),
        ),
        PoolRegistry.__init__(self)

    @sp.entry_point(lazify=False)
    def registerTokens(self, params):
        sp.set_type(params, Types.REGISTER_TOKENS_PARAMS)
        self.onlyUnpaused()
        self.onlyPool(params.poolId)
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

        poolEvent = sp.record(
            poolId=params.poolId,
            tokens=params.tokens,
        )
        sp.emit(poolEvent, tag='TokensRegistered', with_type=True)

    @sp.onchain_view()
    def getPoolTokens(self, poolId):
        sp.set_type(poolId, sp.TPair(sp.TAddress, sp.TNat))
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

    def onlyPool(self, poolId):
        sp.verify(self.data.isPoolRegistered.contains(
            poolId), Errors.INVALID_POOL_ID)
        sp.verify(sp.sender == sp.fst(
            poolId), Errors.CALLER_NOT_POOL)
