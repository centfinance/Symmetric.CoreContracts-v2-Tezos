import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors


class Types:

    # TOKEN = sp.TRecord(
    #     address=sp.TAddress,
    #     id=sp.TNat,
    #     FA2=sp.TBool,
    # )
    TOKEN = sp.TPair(sp.TAddress, sp.TOption(sp.TNat))

    BALANCE = sp.TRecord(
        tokenA=sp.TNat,
        tokenB=sp.TNat,
        lastChangeBlock=sp.TNat,
    )

    TWO_TOKEN_POOL_BALANCES = sp.TRecord(
        sharedCash=sp.TOption(BALANCE),
        sharedManaged=sp.TOption(BALANCE),
    )

    TWO_TOKEN_POOL_TOKENS = sp.TRecord(
        tokenA=TOKEN,
        tokenB=TOKEN,
        balances=sp.TOption(TWO_TOKEN_POOL_BALANCES)
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

    def _setTwoTokenPoolCashBalances(self, params):
        updated_cash = sp.record(
            tokenA=params.balanceA.cash,
            tokenB=params.balanceB.cash,
            lastChangeBlock=sp.max(
                params.balanceA.lastChangeBlock, params.balanceB.lastChangeBlock),
        )
        with sp.modify_record(self.data._twoTokenPoolTokens[params.poolId].balances, 'poolBalances') as poolBalances:
            poolBalances.sharedCash = updated_cash
