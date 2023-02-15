import smartpy as sp

import contracts.utils.Utils as Utils


class Types:

    TOKEN = sp.TRecord(
        address=sp.TAddress,
        id=sp.TNat
    )

    TOKENS_TYPE = sp.TMap(sp.TNat, TOKEN)

    REGISTER_MSI_POOL_TOKENS_PARAMS = sp.TRecord(
        poolId=sp.TBytes,
        tokens=TOKENS_TYPE
    )


class MinimalSwapInfoPoolsBalance:
    def __init__(self):
        self.update_initial_storage(
            _minimalSwapInfoPoolsTokens=sp.big_map(
                l={},
                tkey=sp.TBytes,
                tvalue=Types.TOKENS_TYPE
            ),
        ),

    def _registerMinimalSwapInfoPoolTokens(self, params):
        sp.set_type(params, Types.REGISTER_MSI_POOL_TOKENS_PARAMS)
        # TODO: Refactor
        with sp.if_(self.data._minimalSwapInfoPoolsTokens.contains(params.poolId)):
            registeredTokens = self.data._minimalSwapInfoPoolsTokens[params.poolId].values(
            )
            tokensAmount = sp.len(params.tokens)
            with sp.for_('i', sp.range(0, tokensAmount)) as i:
                prevSize = sp.len(
                    self.data._minimalSwapInfoPoolsTokens[params.poolId])
                t = params.tokens[i]
                sp.verify(Utils.list_contains(registeredTokens, t) == False)
                self.data._minimalSwapInfoPoolsTokens[params.poolId][prevSize] = t
        with sp.else_():
            self.data._minimalSwapInfoPoolsTokens[params.poolId] = params.tokens
