import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors


class Types:

    TOKEN = sp.TRecord(
        address=sp.TAddress,
        id=sp.TNat,
        FA2=sp.TBool,
    )
    TWO_TOKEN_POOL_BALANCES = sp.TRecord(
        sharedCash=sp.TBytes,
        sharedManaged=sp.TBytes
    )

    TWO_TOKEN_POOL_TOKENS = sp.TRecord(
        tokenA=TOKEN,
        tokenB=TOKEN,
        balances=sp.TOption(sp.TMap(sp.TBytes, TWO_TOKEN_POOL_BALANCES))
    )

    REGISTER_TT_POOL_TOKENS_PARAMS = sp.TRecord(
        poolId=sp.TBytes,
        tokenX=TOKEN,
        tokenY=TOKEN
    )


class TwoTokenPoolsBalance:
    def __init__(self):
        self.update_initial_storage(
            _twoTokenPoolTokens=sp.big_map(
                l={},
                tkey=sp.TBytes,
                tvalue=Types.TWO_TOKEN_POOL_TOKENS
            ),
        ),

    def _registerTwoTokenPoolTokens(self, params):
        sp.set_type(params, Types.REGISTER_TT_POOL_TOKENS_PARAMS)
        # Check not needed because tokens is a set
        # sp.verify(params.tokenX != params.tokenY,
        #           Errors.TOKEN_ALREADY_REGISTERED)

        twoTokenPoolTokens = sp.record(
            tokenA=params.tokenX,
            tokenB=params.tokenY,
            balances=sp.none
        )
        self.data._twoTokenPoolTokens[params.poolId] = twoTokenPoolTokens
