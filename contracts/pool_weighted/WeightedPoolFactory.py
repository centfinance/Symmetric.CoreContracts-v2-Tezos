import smartpy as sp

from contracts.pool_weighted.WeightedPool import WeightedPool, IWeightedPool

from contracts.pool_utils.BasePoolFactory import BasePoolFactory

import contracts.interfaces.SymmetricErrors as Errors

import contracts.utils.math.FixedPoint as FixedPoint

import contracts.utils.helpers.ScalingHelpers as ScalingHelpers

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


TOKEN = sp.TPair(sp.TAddress, sp.TOption(sp.TNat))

FEE_CACHE = sp.TTuple(sp.TNat, sp.TNat, sp.TNat)


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


def normalize_metadata(self, metadata):
    meta = {}
    for key in metadata:
        meta[key] = sp.utils.bytes_of_string(metadata[key])

    return meta


class WeightedPoolFactory(sp.Contract):

    def __init__(
        self,
        admin,
        vault,
        weightedMathLib,
        weightedProtocolFeesLib,
        protocolFeeProvider,
        feeCache,
        metadata
    ):
        self.init(
            admin=admin,
            metadata=sp.big_map(
                normalize_metadata(self, metadata)),
            feeCache=feeCache,
            fixedPoint=sp.big_map({
                "mulDown": FixedPoint.mulDown,
                "mulUp": FixedPoint.mulUp,
                "divDown": FixedPoint.divDown,
                "divUp": FixedPoint.divUp,
                "powDown": FixedPoint.powDown,
                "powUp": FixedPoint.powUp,
                "pow": FixedPoint.pow,
            }, tkey=sp.TString, tvalue=sp.TLambda(sp.TPair(sp.TNat, sp.TNat), sp.TNat)),
            weightedMathLib=weightedMathLib,
            weightedProtocolFeesLib=weightedProtocolFeesLib,
        )

        BasePoolFactory.__init__(
            self,
            vault,
            protocolFeeProvider,
        )

        self._creationCode = WeightedPool()

    @sp.entry_point(lazify=False)
    def create(self, params):
        """
            Deploys a new WeightedPool
        """
        # sp.set_type(params, Types.CREATE_PARAMS)
        STORAGE = sp.record(
            admin=self.data.admin,
            proposed_admin=sp.none,
            normalizedWeights=sp.map(l={}, tkey=sp.TNat, tvalue=sp.TNat),
            scalingFactors=sp.map(l={}, tkey=sp.TNat, tvalue=sp.TNat),
            tokens=sp.map(l={}, tkey=sp.TNat, tvalue=TOKEN),
            balances=sp.big_map(
                tvalue=sp.TRecord(approvals=sp.TMap(
                    sp.TAddress, sp.TNat), balance=sp.TNat),
            ),
            exemptFromYieldFees=False,
            feeCache=self.data.feeCache,
            initialized=sp.bool(False),
            metadata=sp.big_map({
                "": params.metadata
            }),
            poolId=sp.none,
            protocolFeesCollector=self.data.protocolFeeProvider,
            rateProviders=sp.map(l={}, tkey=sp.TNat,
                                 tvalue=sp.TOption(sp.TAddress)),
            recoveryMode=False,
            settings=sp.record(paused=False),
            token_metadata=sp.big_map(
                {0: sp.record(
                    token_id=0, token_info=params.token_metadata)},
                tkey=sp.TNat,
                tvalue=sp.TRecord(token_id=sp.TNat,
                                  token_info=sp.TMap(sp.TString, sp.TBytes)),
            ),
            totalSupply=sp.nat(0),
            vault=self.data.vault,
            getTokenValue=sp.compute(getTokenValue),
            fixedPoint=sp.compute(self.data.fixedPoint),
            entries=sp.big_map({
                'totalTokens': sp.nat(0),
                'athRateProduct': sp.nat(0),
                'postJoinExitInvariant': sp.nat(0),
                'swapFeePercentage': sp.nat(0),
            }),
            scaling_helpers=sp.big_map({
                "scale": ScalingHelpers.scale_amounts,
            }),
            weightedMathLib=self.data.weightedMathLib,
            weightedProtocolFeesLib=self.data.weightedProtocolFeesLib,
        )
        self._create(self, STORAGE)

        # IWeightedPool.initialize(pool, sp.record(
        #     tokens
        # ))


# CONTRACT_STORAGE = sp.record(
#     vault=sp.address('KT1TxqZ8QtKvLu3V3JH7Gx58n7Co8pgtpQU5'),
#     protocolFeeProvider=sp.address('KT1VqarPDicMFn1ejmQqqshUkUXTCTXwmkCN'),
# )
# sp.add_compilation_target('Test', WeightedPoolFactory(params=CONTRACT_STORAGE))
