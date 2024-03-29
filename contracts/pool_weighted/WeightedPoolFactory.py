import json
import smartpy as sp

from contracts.pool_weighted.WeightedPool import WeightedPool

from contracts.utils.mixins.Administrable import Administrable

from contracts.pool_utils.BasePool import IBasePool

from contracts.pool_utils.BasePoolFactory import BasePoolFactory

import contracts.interfaces.SymmetricErrors as Errors

import contracts.utils.math.FixedPoint as FixedPoint

import contracts.utils.helpers.ScalingHelpers as ScalingHelpers

import contracts.interfaces.SymmetricEnums as Enums

f = open(".taq/config.local.testing.json")

data = json.load(f)
# class Types:

MIN_TOKENS = 2
MAX_TOKENS = 8
MIN_SWAP_FEE_PERCENTAGE = 1000000000000
MAX_SWAP_FEE_PERCENTAGE = 100000000000000000
MIN_WEIGHT = 10000000000000000  # 0.01e18

TOKEN = sp.TPair(sp.TAddress, sp.TOption(sp.TNat))

FEE_CACHE = sp.TTuple(sp.TNat, sp.TNat, sp.TNat)

CONTRACT_METADATA = {
    "": "https://raw.githubusercontent.com/centfinance/Symmetric.CoreContracts-v2-Tezos/main/metadata/testnet/WeightedPoolFactory.json",
}


class IWeightedPoolFactory:
    CreateParams = sp.TRecord(
        tokens=sp.TMap(sp.TNat, sp.TPair(sp.TAddress, sp.TOption(sp.TNat))),
        normalizedWeights=sp.TMap(sp.TNat, sp.TNat),
        tokenDecimals=sp.TMap(sp.TNat, sp.TNat),
        rateProviders=sp.TOption(sp.TMap(sp.TNat, sp.TOption(sp.TAddress))),
        swapFeePercentage=sp.TNat,
        metadata=sp.TBytes,
        token_metadata=sp.TMap(sp.TString, sp.TBytes),
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


def normalize_metadata(self, metadata):
    meta = {}
    for key in metadata:
        meta[key] = sp.utils.bytes_of_string(metadata[key])

    return meta


class WeightedPoolFactory(
    sp.Contract,
    Administrable,
):

    def __init__(
        self,
        admin=sp.address('tz1UGWQQ5YFkZqWgE3gqmPyuwy2R5VGpMM9B'),
        vault=sp.address(data["contracts"]["Vault"]["address"]),
        weightedMathLib=sp.address(data["contracts"]["ExternalWeightedMath"]["address"]),
        weightedProtocolFeesLib=sp.address(data["contracts"]["ExternalWeightedProtocolFees"]["address"]),
        protocolFeeProvider=sp.address(data["contracts"]["ProtocolFeesCollector"]["address"]),
        feeCache=(sp.nat(400000000000000000), sp.nat(400000000000000000)),
        metadata=CONTRACT_METADATA,
    ):
        self.init(
            metadata=sp.big_map(
                normalize_metadata(self, metadata)),
            feeCache=feeCache,
            weightedMathLib=weightedMathLib,
            weightedProtocolFeesLib=weightedProtocolFeesLib,
        )
        Administrable.__init__(
            self,
            admin,
            False,
        )
        BasePoolFactory.__init__(
            self,
            vault,
            protocolFeeProvider,
        )

        self._creationCode = WeightedPool()

    @sp.entry_point(lazify=False, parameter_type=IWeightedPoolFactory.CreateParams)
    def create(self, params):
        """
            Deploys a new WeightedPool
        """
        self.onlyAdministrator()
        numTokens = sp.len(params.tokens)
        sp.verify(numTokens >= MIN_TOKENS, Errors.MIN_TOKENS)
        sp.verify(numTokens <= MAX_TOKENS, Errors.MAX_TOKENS)
        sp.verify((numTokens == sp.len(params.normalizedWeights))
                  & (numTokens == sp.len(params.tokenDecimals)))

        # Ensure each normalized weight is above the minimum
        normalizedSum = sp.local('normalizedSum', 0)
        with sp.for_('i', sp.range(0, numTokens)) as i:
            normalizedWeight = params.normalizedWeights[i]

            sp.verify(normalizedWeight >=
                      MIN_WEIGHT, Errors.MIN_WEIGHT)
            normalizedSum.value = normalizedSum.value + normalizedWeight

        sp.verify(normalizedSum.value == FixedPoint.ONE,
                  Errors.NORMALIZED_WEIGHT_INVARIANT)
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
            fixedPoint=sp.big_map({
                Enums.MUL_DOWN: FixedPoint.mulDown,
                Enums.MUL_UP: FixedPoint.mulUp,
                Enums.DIV_DOWN: FixedPoint.divDown,
                Enums.DIV_UP: FixedPoint.divUp,
            }, tkey=sp.TNat, tvalue=sp.TLambda(sp.TPair(sp.TNat, sp.TNat), sp.TNat)),
            entries=sp.big_map({
                Enums.ATH_RATE_PRODUCT: sp.nat(0),
                Enums.POST_JOIN_EXIT_INVARIANT: sp.nat(0),
                Enums.SWAP_FEE_PERCENTAGE: params.swapFeePercentage,
            }),
            scaling_helpers=sp.big_map({
                0: ScalingHelpers.scale_amounts,
            }),
            weightedMathLib=self.data.weightedMathLib,
            weightedProtocolFeesLib=self.data.weightedProtocolFeesLib,
        )
        self._create(self, STORAGE)

        # IBasePool.initialize(self, pool)

    def _computeScalingFactor(self, decimals):
        sp.set_type(decimals, sp.TNat)
        decimalsDifference = sp.as_nat(18 - decimals)
        return FixedPoint.ONE * (self.power((sp.nat(10), decimalsDifference)))

    def _getYieldFeeExemption(self, rateProviders):
        exempt = sp.local('exempt', True)

        with sp.for_('i', sp.range(0, sp.len(rateProviders)))as i:
            with sp.if_(rateProviders[i] != sp.none):
                exempt.value = False

        return exempt.value

    def power(self, p):
        x, y = sp.match_pair(p)
        powResult = sp.local('powResult', 1)
        base = sp.local('base', x)
        exponent = sp.local('exponent', y)

        with sp.while_(exponent.value != 0):
            with sp.if_((exponent.value % 2) != 0):
                powResult.value *= base.value

            exponent.value = exponent.value >> 1  # Equivalent to exponent.value / 2
            base.value *= base.value

        return powResult.value


sp.add_compilation_target('WeightedPoolFactory', WeightedPoolFactory())
