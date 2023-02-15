import smartpy as sp

import contracts.utils.Utils as Utils


class Types:

    TOKEN = sp.TRecord(
        address=sp.TAddress,
        id=sp.TNat
    )
    ENTRY = sp.TRecord(
        token=TOKEN,
        balance=sp.TBytes
    )

    ENUMERABLE_MAP = sp.TRecord(
        length=sp.TNat,
        tokens=sp.Tmap(sp.TNat, ENTRY),
        indexes=sp.TMap(TOKEN, sp.TNat)
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

        # with sp.if_(self.data._generalPoolsTokens.contains(params.poolId)):
        #     registeredTokens = self.data._generalPoolsTokens[params.poolId].values(
        #     )
        #     prevSize = sp.len(
        #         self.data._generalPoolsTokens[params.poolId])
        #     tokensAmount = sp.len(params.tokens)
        #     with sp.for_('i', sp.range(0, tokensAmount)) as i:
        #         t = params.tokens[i]
        #         sp.verify(Utils.list_contains(registeredTokens, t) == False)
        #         self.data._generalPoolsTokens[params.poolId][i + prevSize] = t
        # with sp.else_():
        #     self.data._generalPoolsTokens[params.poolId] = params.tokens
