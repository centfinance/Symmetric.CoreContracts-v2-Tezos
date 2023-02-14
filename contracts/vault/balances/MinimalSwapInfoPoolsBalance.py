import smartpy as sp


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


def list_contains(lst, elem):
    contains = sp.local("contains", False)
    with sp.for_('e', lst) as e:
        with sp.if_(e == elem):
            contains.value = True


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

        with sp.if_(self.data._minimalSwapInfoPoolsTokens.contains(params.poolId)):
            registeredTokens = self.data._minimalSwapInfoPoolsTokens[params.poolId].values(
            )
            prevSize = sp.len(
                self.data._minimalSwapInfoPoolsTokens[params.poolId])
            tokensAmount = sp.len(params.tokens)
            with sp.for_('i', sp.range(0, tokensAmount)) as i:
                t = params.tokens[i]
                sp.verify(list_contains(registeredTokens, t) == False)
                self.data._minimalSwapInfoPoolsTokens[params.poolId][i + prevSize] = t
        with sp.else_():
            self.data._minimalSwapInfoPoolsTokens[params.poolId] = params.tokens
