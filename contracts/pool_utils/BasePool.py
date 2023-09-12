import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

import contracts.interfaces.SymmetricEnums as Enums

import contracts.utils.math.FixedPoint as FixedPoint

import contracts.pool_utils.lib.PoolRegistrationLib as PoolRegistrationLib

from contracts.pool_utils.SymmetricPoolToken import SymmetricPoolToken

from contracts.utils.mixins.Administrable import Administrable

from contracts.utils.mixins.Pausable import Pausable

_MIN_TOKENS = 2
_DEFAULT_MINIMUM_SPT = 1000000
_MIN_SWAP_FEE_PERCENTAGE = 1000000000000
_MAX_SWAP_FEE_PERCENTAGE = 100000000000000000
_SWAP_FEE_PERCENTAGE_OFFSET = 1000000000000

_SWAP_FEE_PERCENTAGE_BIT_LENGTH = 100000000000000000


class IBasePool:
    JOIN_USER_DATA = sp.TRecord(
        kind=sp.TNat,
        amountsIn=sp.TOption(sp.TMap(sp.TNat, sp.TNat)),
        minSPTAmountOut=sp.TOption(sp.TNat),
        sptAmountOut=sp.TOption(sp.TNat),
        tokenIndex=sp.TOption(sp.TNat),
        allT=sp.TOption(sp.TNat),
    )

    EXIT_USER_DATA = sp.TRecord(
        kind=sp.TNat,
        amountsOut=sp.TOption(sp.TMap(sp.TNat, sp.TNat)),
        maxSPTAmountIn=sp.TOption(sp.TNat),
        sptAmountIn=sp.TOption(sp.TNat),
        tokenIndex=sp.TOption(sp.TNat),
        recoveryModeExit=sp.TBool,
    )

    t_after_join_pool_params = sp.TRecord(
        poolId=sp.TPair(sp.TAddress, sp.TNat),
        balances=sp.TMap(sp.TNat, sp.TNat),
        recipient=sp.TAddress,
        amountsIn=sp.TMap(sp.TNat, sp.TNat),
        sptAmountOut=sp.TNat,
        invariant=sp.TNat,
    )

    t_after_exit_pool_params = sp.TRecord(
        poolId=sp.TPair(sp.TAddress, sp.TNat),
        balances=sp.TMap(sp.TNat, sp.TNat),
        sender=sp.TAddress,
        amountsOut=sp.TMap(sp.TNat, sp.TNat),
        sptAmountIn=sp.TNat,
        invariant=sp.TNat,
        recoveryModeExit=sp.TBool,
    )

    t_before_join_pool_params = sp.TRecord(
        balances=sp.TMap(sp.TNat, sp.TNat),
        userData=JOIN_USER_DATA,
    )

    t_before_exit_pool_params = sp.TRecord(
        balances=sp.TMap(sp.TNat, sp.TNat),
        userData=EXIT_USER_DATA,
    )

    def initializePool(self, pool):
        initializePool = sp.contract(sp.TUnit, pool, "initializePool").open_some(
            "INITIALIZE_FAIL")
        sp.transfer(sp.unit, sp.tez(0), initializePool)

    def afterJoinPool(pool, params):
        entry_point = sp.contract(
            IBasePool.t_after_join_pool_params,
            pool,
            "afterJoinPool",
        ).open_some("INTERFACE_MISMATCH")
        sp.transfer(params, sp.tez(0), entry_point)

    def afterExitPool(pool, params):
        entry_point = sp.contract(
            IBasePool.t_after_exit_pool_params,
            pool,
            "afterExitPool",
        ).open_some("INTERFACE_MISMATCH")
        sp.transfer(params, sp.tez(0), entry_point)

    def beforeJoinPool(pool, params):
        view_result = sp.compute(
            sp.view(
                "beforeJoinPool",
                pool,
                params,
                sp.TTuple(sp.TNat, sp.TMap(sp.TNat, sp.TNat), sp.TNat),
            ).open_some(Errors.BEFORE_JOIN_POOL_INVALID)
        )
        return view_result

    def beforeExitPool(pool, params):
        view_result = sp.compute(
            sp.view(
                "beforeExitPool",
                pool,
                params,
                sp.TTuple(sp.TNat, sp.TMap(sp.TNat, sp.TNat), sp.TNat),
            ).open_some(Errors.BEFORE_EXIT_POOL_INVALID)
        )
        return view_result


class BasePool(
    Administrable,
    Pausable,
    SymmetricPoolToken,
):

    def __init__(
        self,
        owner,
        vault,
        name,
        symbol,
        protocolFeesCollector=sp.address(
            'KT1N5Qpp5DaJzEgEXY1TW6Zne6Eehbxp83XF')
    ):
        self.update_initial_storage(
            poolId=sp.none,
            protocolFeesCollector=protocolFeesCollector
        )
        Administrable.__init__(self, owner, False)
        Pausable.__init__(self, False, False)
        SymmetricPoolToken.__init__(self, name, symbol, vault)

    @sp.entry_point(lazify=False)
    def initializePool(self):
        sp.verify(self.data.initialized == False)

        poolId = PoolRegistrationLib.registerPool(
            vault=self.data.vault,
            tokens=self.data.tokens,
            assetManagers=sp.none,
        )

        self.data.poolId = sp.some(poolId)
        self.data.initialized = True

    @sp.private_lambda(with_storage='read-only')
    def onlyVault(self, poolId):
        sp.verify(sp.sender == self.data.vault)
        sp.verify(poolId == self.data.poolId)

    @sp.entry_point(parameter_type=IBasePool.t_after_join_pool_params, lazify=False)
    def afterJoinPool(
        self,
        poolId,
        recipient,
        amountsIn,
        sptAmountOut,
        invariant,
        balances,
    ):
        # only vault and vailid pool id can call
        self.onlyVault(poolId)
        # ensureNotPaused
        self.onlyUnpaused()

        with sp.if_(self.data.totalSupply == 0):

            self._afterInitializePool(invariant)
            sp.verify(sptAmountOut >= _DEFAULT_MINIMUM_SPT,
                      Errors.MINIMUM_SPT)
            # Mint to Tezos Null address
            self._mintPoolTokens(sp.address(
                'tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU'), _DEFAULT_MINIMUM_SPT)
            self._mintPoolTokens(
                recipient, sp.as_nat(sptAmountOut - _DEFAULT_MINIMUM_SPT))

        with sp.else_():
            scalingFactors = self.data.scalingFactors

            upScaledBalances = sp.compute(self.data.scaling_helpers[0]((
                balances, scalingFactors, self.data.fixedPoint[Enums.MUL_DOWN])))

            upScaledAmounts = sp.compute(self.data.scaling_helpers[0]((
                amountsIn, scalingFactors, self.data.fixedPoint[Enums.MUL_DOWN])))

            self._afterJoinPool(
                sp.record(
                    invariant=invariant,
                    balances=upScaledBalances,
                    amountsIn=upScaledAmounts,
                    sptAmountOut=sptAmountOut,
                )
            )

            self._mintPoolTokens(recipient, sptAmountOut)

    @sp.entry_point(parameter_type=IBasePool.t_after_exit_pool_params, lazify=False)
    def afterExitPool(
        self,
        poolId,
        sender,
        amountsOut,
        sptAmountIn,
        invariant,
        balances,
        recoveryModeExit=False
    ):
        self.onlyVault(poolId)
        self.onlyUnpaused()
        with sp.if_(recoveryModeExit):
            sp.verify(self.data.recoveryMode == True, Errors.NOT_IN_RECOVERY_MODE)

            self._burnPoolTokens(sender, sptAmountIn)

        with sp.else_():
            scalingFactors = self.data.scalingFactors

            upScaledBalances = sp.compute(self.data.scaling_helpers[0]((
                balances, scalingFactors, self.data.fixedPoint[Enums.MUL_DOWN])))

            upScaledAmounts = sp.compute(self.data.scaling_helpers[0]((
                amountsOut, scalingFactors, self.data.fixedPoint[Enums.MUL_DOWN])))

            self._afterExitPool(
                sp.record(
                    invariant=invariant,
                    balances=upScaledBalances,
                    amountsOut=upScaledAmounts,
                    sptAmountIn=sptAmountIn,
                )
            )

            self._burnPoolTokens(sender, sptAmountIn)


    @sp.onchain_view()
    def beforeJoinPool(
        self,
        params,
    ):
        sp.set_type(params, IBasePool.t_before_join_pool_params)
        self.onlyUnpaused()
        scalingFactors = self.data.scalingFactors
        result = sp.local('result', (0, {}, 0))
        with sp.if_(self.data.totalSupply == 0):
            result.value = self._beforeInitializePool(
                sp.record(
                    scalingFactors=scalingFactors,
                    userData=params.userData,
                )
            )

        with sp.else_():
            upScaledBalances = sp.compute(self.data.scaling_helpers[0]((
                params.balances, scalingFactors, self.data.fixedPoint[Enums.MUL_DOWN])))
            result.value = self._beforeJoinPool(
                sp.record(
                    balances=upScaledBalances,
                    scalingFactors=scalingFactors,
                    userData=params.userData,
                )
            )
        # amountsIn are amounts entering the Pool, so we round up.
        sptAmountOut, amountsIn, invariant = sp.match_tuple(
            result.value, 'sptAmountOut', 'amountsIn', 'invariant')
        downscaledAmounts = sp.compute(self.data.scaling_helpers[0]((
            amountsIn, scalingFactors, self.data.fixedPoint[Enums.DIV_UP])))

        # This Pool ignores the `dueProtocolFees` return value, so we simply return a zeroed-out array.
        sp.result((sptAmountOut, downscaledAmounts, invariant))

    @sp.onchain_view()
    def beforeExitPool(
        self,
        params,
    ):
        sp.set_type(params, IBasePool.t_before_exit_pool_params)
        self.onlyUnpaused()
        result = sp.local('result', (0, {}, 0))
        with sp.if_(params.userData.recoveryModeExit):

            sp.verify(self.data.recoveryMode == True, Errors.NOT_IN_RECOVERY_MODE)

            result.value = self._doRecoveryModeExit(
                sp.record(
                    balances=params.balances,
                    totalSupply=self.data.totalSupply,
                    userData=params.userData
                )
            )
        with sp.else_():
            scalingFactors = self.data.scalingFactors

            upScaledBalances = sp.compute(self.data.scaling_helpers[0]((
                params.balances, scalingFactors, self.data.fixedPoint[Enums.MUL_DOWN])))

            exitValues = self._beforeExitPool(
                sp.record(
                    balances=upScaledBalances,
                    scalingFactors=scalingFactors,
                    userData=params.userData
                )
            )

            sptAmountIn, amountsOut, invariant = sp.match_tuple(
            exitValues, 'sptAmountIn', 'amountsOut', 'invariant')

            downscaledAmounts = sp.compute(self.data.scaling_helpers[0]((
            amountsOut, scalingFactors, self.data.fixedPoint[Enums.DIV_DOWN])))

            result.value = (sptAmountIn, downscaledAmounts, invariant)



        sp.result(result.value)

    @sp.entry_point(lazify=False)
    def enableRecoveryMode(self):
        self.onlyAdministrator()
        sp.verify(self.data.recoveryMode == False, Errors.IN_RECOVERY_MODE)
        self._setRecoveryMode(True)

    @sp.entry_point(lazify=False)
    def disableRecoveryMode(self):
        self.onlyAdministrator()
        sp.verify(self.data.recoveryMode == True, Errors.NOT_IN_RECOVERY_MODE)
        self._setRecoveryMode(False)

###########
# Internal Functions
###########

    def _addSwapFeeAmount(self, amount):
        # This returns amount + fee amount, so we round up (favoring a higher fee amount).
        return self.data.fixedPoint[Enums.DIV_UP]((amount, FixedPoint.complement(self.data.entries[Enums.SWAP_FEE_PERCENTAGE])))

    def _subtractSwapFeeAmount(self, amount):
        # This returns amount - fee amount, so we round up (favoring a higher fee amount).
        feeAmount = self.data.fixedPoint[Enums.MUL_UP](
            (amount, self.data.entries[Enums.SWAP_FEE_PERCENTAGE]))
        return sp.as_nat(amount - feeAmount)

    def _setSwapFeePercentage(self, swapFeePercentage):
        sp.verify(swapFeePercentage >= _MIN_SWAP_FEE_PERCENTAGE,
                  Errors.MIN_SWAP_FEE_PERCENTAGE)
        sp.verify(swapFeePercentage <= _MAX_SWAP_FEE_PERCENTAGE,
                  Errors.MAX_SWAP_FEE_PERCENTAGE)

        self.data.entries[Enums.SWAP_FEE_PERCENTAGE] = swapFeePercentage

        sp.emit(swapFeePercentage, 'SwapFeePercentageChanged')


    def _payProtocolFees(self, sptAmount):
        with sp.if_(sptAmount > 0):
            self._mintPoolTokens(
                self.data.protocolFeesCollector, sptAmount)
    
    # @sp.private_lambda(with_storage='read-write')
    def _setRecoveryMode(self, enabled):
        self.data.recoveryMode = enabled

        with sp.if_(enabled == False):
            self._onDisableRecoveryMode()

        sp.emit(enabled, 'RecoveryModeStateChanged', with_type=True)
