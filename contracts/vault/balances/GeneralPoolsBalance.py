import smartpy as sp

import contracts.utils.Utils as Utils

import contracts.interfaces.SymmetricErrors as Errors


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

    ENUMERABLE_MAP = sp.TRecord(
        balances=sp.TMap(sp.TNat, sp.TOption(BALANCE)),
        tokens=sp.TMap(TOKEN, sp.TNat)
    )

    TOKENS_TYPE = sp.TMap(sp.TNat, TOKEN)

    REGISTER_G_POOL_TOKENS_PARAMS = sp.TRecord(
        poolId=sp.TBytes,
        tokens=TOKENS_TYPE
    )


class GeneralPoolsBalance:
    def __init__(self):
        self.update_initial_storage(
            _generalPoolsBalances=sp.big_map(
                l={},
                tkey=sp.TBytes,
                tvalue=Types.ENUMERABLE_MAP
            ),
        ),

    #    Requirements:
    #
    #  - `tokens` must not be registered in the Pool
    #
    def _registerGeneralPoolTokens(self, params):
        sp.set_type(params, Types.REGISTER_G_POOL_TOKENS_PARAMS)
      # TODO: Refactor to use only one loop
        with sp.if_(self.data._generalPoolsBalances.contains(params.poolId)):
            registered = self.data._generalPoolsBalances[params.poolId]
            with sp.for_('t', params.tokens.values()) as t:
                sp.verify(registered.tokens.contains(t) == False,
                          Errors.TOKEN_ALREADY_REGISTERED)
                index = sp.len(registered.tokens)
                registered.tokens[t] = index
                # Initiailise Balance
                registered.balances[index] = sp.none
        with sp.else_():
            record = sp.compute(sp.record(
                balances=sp.map(l={}, tkey=sp.TNat,
                                tvalue=sp.TOption(sp.TBytes)),
                tokens=sp.map(l={}, tkey=Types.TOKEN, tvalue=sp.TNat)
            ))
            tokensAmount = sp.range(0, sp.len(params.tokens))
            with sp.for_('i', tokensAmount) as i:
                t = params.tokens[i]
                record.tokens[t] = i
                record.balances[i] = sp.none
            self.data._generalPoolsBalances[params.poolId] = record

    def _setGeneralPoolBalances(self, params):
        poolBalances = self.data._generalPoolsBalances[params.poolId]

        with sp.for_('i', sp.range(0, sp.len(params.balances))) as i:
            poolBalances.balances[i] = params.balances[i]
