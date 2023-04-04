import smartpy as sp

from contracts.pool_weighted.WeightedPool import WeightedPool

from contracts.pool_utils.BasePool import IBasePool

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
MIN_TOKENS = 2
MAX_TOKENS = 8
MIN_SWAP_FEE_PERCENTAGE = 1000000000000
MAX_SWAP_FEE_PERCENTAGE = 100000000000000000
MIN_WEIGHT = 10000000000000000  # 0.01e18

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
        numTokens = sp.len(params.tokens)
        sp.verify(numTokens >= MIN_TOKENS, Errors.MIN_TOKENS)
        sp.verify(numTokens <= MAX_TOKENS, Errors.MAX_TOKENS)
        sp.verify((numTokens == sp.len(params.normalizedWeights))
                  & (numTokens == sp.len(params.tokenDecimals)))

        # // Ensure each normalized weight is above the minimum
        normalizedSum = sp.local('normalizedSum', 0)
        with sp.for_('i', sp.range(0, numTokens)) as i:
            normalizedWeight = params.normalizedWeights[i]

            sp.verify(normalizedWeight >=
                      MIN_WEIGHT, Errors.MIN_WEIGHT)
            normalizedSum.value = normalizedSum.value + normalizedWeight

        # // Ensure that the normalized weights sum to ONE
        sp.verify(normalizedSum.value == FixedPoint.ONE,
                  Errors.NORMALIZED_WEIGHT_INVARIANT)

        # self.data.normalizedWeights = params.normalizedWeights
        scalingFactors = sp.compute(sp.map({}, tkey=sp.TNat, tvalue=sp.TNat))
        with sp.for_('i', sp.range(0, numTokens)) as i:
            scalingFactors[i] = self._computeScalingFactor(
                params.tokenDecimals[i])

        exemptFromYieldFees = sp.local('exemptFromYieldFees', True)
        with sp.if_(params.rateProviders.is_some()):
            rateProviders = params.rateProviders.open_some()
            sp.verify(numTokens == sp.len(rateProviders))

            exemptFromYieldFees.value = self._getYieldFeeExemption(
                rateProviders)

        sp.verify(params.swapFeePercentage >= MIN_SWAP_FEE_PERCENTAGE,
                  Errors.MIN_SWAP_FEE_PERCENTAGE)
        sp.verify(params.swapFeePercentage <= MAX_SWAP_FEE_PERCENTAGE,
                  Errors.MAX_SWAP_FEE_PERCENTAGE)

        STORAGE = sp.record(
            admin=self.data.admin,
            proposed_admin=sp.none,
            normalizedWeights=params.normalizedWeights,
            scalingFactors=scalingFactors,
            tokens=params.tokens,
            balances=sp.big_map(
                tvalue=sp.TRecord(approvals=sp.TMap(
                    sp.TAddress, sp.TNat), balance=sp.TNat),
            ),
            exemptFromYieldFees=exemptFromYieldFees.value,
            feeCache=self.data.feeCache,
            initialized=sp.bool(False),
            metadata=sp.big_map({
                "": params.metadata
            }),
            poolId=sp.none,
            protocolFeesCollector=self.data.protocolFeeProvider,
            rateProviders=params.rateProviders,
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
                'totalTokens': numTokens,
                'athRateProduct': sp.nat(0),
                'postJoinExitInvariant': sp.nat(0),
                'swapFeePercentage': params.swapFeePercentage,
            }),
            scaling_helpers=sp.big_map({
                "scale": ScalingHelpers.scale_amounts,
            }),
            weightedMathLib=self.data.weightedMathLib,
            weightedProtocolFeesLib=self.data.weightedProtocolFeesLib,
        )
        pool = self._create(self, STORAGE)

        IBasePool.initialize(pool)

    def _computeScalingFactor(self, decimals):
        sp.set_type(decimals, sp.TNat)
        decimalsDifference = sp.as_nat(18 - decimals)
        return FixedPoint.ONE * (self.data.fixedPoint['pow']((sp.nat(10), decimalsDifference)))

    def _getYieldFeeExemption(self, rateProviders):
        exempt = sp.local('exempt', True)

        with sp.for_('i', sp.range(0, sp.len(rateProviders)))as i:
            with sp.if_(rateProviders[i] != sp.none):
                exempt.value = False

        return exempt.value
