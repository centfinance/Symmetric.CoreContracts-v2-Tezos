import smartpy as sp

import contracts.utils.Utils as Utils

import contracts.interfaces.SymmetricErrors as Errors


class Types:

    TOKEN = sp.TRecord(
        address=sp.TAddress,
        id=sp.TNat
    )

    ENUMERABLE_MAP = sp.TRecord(
        balances=sp.Tmap(sp.TNat, sp.TOption(sp.TBytes)),
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

        with sp.if_(self.data._generalPoolsTokens.contains(params.poolId)):
            registered = self.data._generalPoolsTokens[params.poolId]
            with sp.for_('t', params.tokens.values()) as t:
                sp.verify(registered.contains(t) == False,
                          Errors.TOKEN_ALREADY_REGISTERED)
                index = sp.len(registered.indexes)
                registered.tokens[t] = index
                # Initiailise Balance
                registered.balances[index] = sp.none
        with sp.else_():
            registered = sp.record(
                balances=sp.Tmap(tkey=sp.TNat, tvalue=sp.TOption(sp.TBytes)),
                tokens=sp.TMap(tkey=Types.TOKEN, tvalue=sp.TNat)
            )
            tokensAmount = sp.len(params.tokens)
            with sp.for_('i', sp.range(0, tokensAmount)) as i:
                t = params.tokens[i]
                registered.tokens[t] = i
                registered.balances[i] = sp.none
