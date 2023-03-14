import smartpy as sp

from contracts.pool_weighted.WeightedPool import WeightedPool

from contracts.pool_utils.BasePoolFactory import BasePoolFactory

import contracts.interfaces.SymmetricErrors as Errors

# class Types:

#     CREATE_PARAMS = sp.TRecord(
#         name=sp.TString,
#         symbol=sp.TString,
#         tokens=sp.TList(t=sp.TAddress),
#         tokenIds=sp.TList(t=sp.TNat),
#         normalizedWeights=sp.TList(t=sp.TNat),
#         # Implement later
#         # rateProviders=sp.TList(t=sp.TNat)
#         swapFeePercentage=sp.TNat,
#         owner=sp.TAddress
#     )

TOKEN = sp.TRecord(
    address=sp.TAddress,
    id=sp.TNat,
    FA2=sp.TBool,
)

FEE_CACHE = sp.TRecord(
    swapFee=sp.TNat,
    yieldFee=sp.TNat,
    aumFee=sp.TNat,
)


def getTokenValue(t):
    sp.set_type(t, sp.TTuple(
        TOKEN,
        sp.TMap(sp.TNat, TOKEN),
        sp.TMap(sp.TNat, sp.TNat)))

    token, tokens, entries,  = sp.match_tuple(
        t, 'token', 'tokens', 'entries')

    entry = sp.local('entry', sp.nat(0))
    with sp.for_('i', sp.range(0, sp.len(entries))) as i:
        with sp.if_(tokens[i] == token):
            entry.value = entries[i]

    with sp.if_(entry.value == 0):
        sp.failwith(Errors.INVALID_TOKEN)

    sp.result(entry.value)


class WeightedPoolFactory(sp.Contract):

    def __init__(self, params):
        self.init_type(
            sp.TRecord(
                _vault=sp.TAddress,
                _protocolFeeProvider=sp.TAddress,
                _isPoolFromFactory=sp.TBigMap(sp.TAddress, sp.TUnit)
            )
        )

        BasePoolFactory.__init__(
            self,
            params,
        )
        self._creationCode = WeightedPool(
            params.vault,
            'Weighted Pool Implementation',
            'WPI'
        )

    @sp.entry_point(lazify=True)
    def create(self, params):
        """
            Deploys a new WeightedPool
        """
        # TODO: Add WeightedPool params type
        # sp.set_type(params, Types.CREATE_PARAMS)
        STORAGE = sp.record(
            normalizedWeights=sp.map(l={}, tkey=sp.TNat, tvalue=sp.TNat),
            scalingFactors=sp.map(l={}, tkey=sp.TNat, tvalue=sp.TNat),
            tokens=sp.map(l={}, tkey=sp.TNat, tvalue=TOKEN),
            totalTokens=sp.nat(0),
            athRateProduct=sp.nat(0),
            balances=sp.big_map(
                tvalue=sp.TRecord(approvals=sp.TMap(
                    sp.TAddress, sp.TNat), balance=sp.TNat),
            ),
            exemptFromYieldFees=False,
            feeCache=sp.record(
                swapFee=sp.nat(0),
                yieldFee=sp.nat(0),
                aumFee=sp.nat(0),
            ),
            initialized=sp.bool(False),
            metadata=sp.big_map({
                "": params.metadata
            }),
            poolId=sp.none,
            postJoinExitInvariant=sp.nat(0),
            protocolFeesCollector=sp.none,
            rateProviders=sp.map(l={}, tkey=sp.TNat,
                                 tvalue=sp.TOption(sp.TAddress)),
            swapFeePercentage=sp.nat(0),
            token_metadata=sp.big_map(
                {0: sp.record(
                    token_id=0, token_info=params.token_metadata)},
                tkey=sp.TNat,
                tvalue=sp.TRecord(token_id=sp.TNat,
                                  token_info=sp.TMap(sp.TString, sp.TBytes)),
            ),
            totalSupply=sp.nat(0),
            vault=self.data._vault,
            getTokenValue=getTokenValue,
        )
        self._create(self, STORAGE)


# CONTRACT_STORAGE = sp.record(
#     vault=sp.address('KT1TxqZ8QtKvLu3V3JH7Gx58n7Co8pgtpQU5'),
#     protocolFeeProvider=sp.address('KT1VqarPDicMFn1ejmQqqshUkUXTCTXwmkCN'),
# )
# sp.add_compilation_target('Test', WeightedPoolFactory(params=CONTRACT_STORAGE))
