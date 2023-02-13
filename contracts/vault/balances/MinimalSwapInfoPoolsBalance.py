import smartpy as sp


class Types:
    TOKENS_TYPE = sp.TList(sp.TRecord(
        address=sp.TAddress,
        id=sp.TNat
    ))

    REGISTER_MSI_POOL_TOKENS_PARAMS = sp.record(
        poolId=sp.TBytes,
        tokens=TOKENS_TYPE
    )


def list_contains(lst, elem):
    contains = sp.local("contains", False)
    with sp.for_('e' in lst) as e:
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
        poolTokens = sp.local('poolTokens', sp.set([]), sp.TSet(sp.TRecord(
            address=sp.TAddress,
            id=sp.TNat
        )))
        with sp.for_('t' in params.tokens) as t:
            sp.verify(~poolTokens.value.contains(t))
            poolTokens.push(t)

        tokensSet = poolTokens.elements()
        with sp.if_(self.data._minimalSwapInfoPoolsTokens.contains(params.poolId)):
            with sp.for_('t' in tokensSet) as t:
                sp.verify(list_contains(
                    self.data._minimalSwapInfoPoolsTokens[params.poolId], t))
                self.data._minimalSwapInfoPoolsTokens[params.poolId].push(t)
        with sp.else_():
            self.data._minimalSwapInfoPoolsTokens[params.poolId] = tokensSet
