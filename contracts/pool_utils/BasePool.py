import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

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
        kind=sp.TString,
        amountsIn=sp.TOption(sp.TMap(sp.TNat, sp.TNat)),
        minSPTAmountOut=sp.TOption(sp.TNat),
        sptAmountOut=sp.TOption(sp.TNat),
        tokenIndex=sp.TOption(sp.TNat),
        allT=sp.TOption(sp.TNat),
    )

    EXIT_USER_DATA = sp.TRecord(
        kind=sp.TString,
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
            ).open_some("Invalid view")
        )
        return view_result

    def beforeExitPool(pool, params):
        view_result = sp.compute(
            sp.view(
                "beforeExitPool",
                pool,
                params,
                sp.TTuple(sp.TNat, sp.TMap(sp.TNat, sp.TNat), sp.TNat),
            ).open_some("Invalid view")
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
        # tokensAmount = sp.len(self.data.tokens)
        # sp.verify(tokensAmount >= _MIN_TOKENS, Errors.MIN_TOKENS)
        # sp.verify(tokensAmount <= self.MAX_TOKENS, Errors.MAX_TOKENS)

        # self._setSwapFeePercentage(params.swapFeePercentage)

        poolId = PoolRegistrationLib.registerPool(
            vault=self.data.vault,
            tokens=self.data.tokens,
            assetManagers=sp.none,
        )

        self.data.poolId = sp.some(poolId)

        # TODO: Add protocolFeesCollector call to vault
        # self.data.protocolFeesCollector = vault.getProtocolFeesCollector()
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

            upScaledBalances = sp.compute(self.data.scaling_helpers['scale']((
                balances, scalingFactors, self.data.fixedPoint['mulDown'])))

            upScaledAmounts = sp.compute(self.data.scaling_helpers['scale']((
                amountsIn, scalingFactors, self.data.fixedPoint['mulDown'])))

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
            # TODO: Check that it's in recovery mode
            # _ensureInRecoveryMode();

            self._burnPoolTokens(sender, sptAmountIn)

        with sp.else_():
            scalingFactors = self.data.scalingFactors

            upScaledBalances = sp.compute(self.data.scaling_helpers['scale']((
                balances, scalingFactors, self.data.fixedPoint['mulDown'])))

            upScaledAmounts = sp.compute(self.data.scaling_helpers['scale']((
                amountsOut, scalingFactors, self.data.fixedPoint['mulDown'])))

            self._afterExitPool(
                sp.record(
                    invariant=invariant,
                    balances=upScaledBalances,
                    amountsOut=upScaledAmounts,
                    sptAmountIn=sptAmountIn,
                )
            )

            self._burnPoolTokens(sender, sptAmountIn)

    # # @ sp.entry_point
    # # def setSwapFeePercentage(self, swapFeePercentage):
    # #     pass

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
            upScaledBalances = sp.compute(self.data.scaling_helpers['scale']((
                params.balances, scalingFactors, self.data.fixedPoint['mulDown'])))
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
        downscaledAmounts = sp.compute(self.data.scaling_helpers['scale']((
            amountsIn, scalingFactors, self.data.fixedPoint['divUp'])))

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
            # TODO: Check that it's in recovery mode
            # _ensureInRecoveryMode();

            result.value = self._doRecoveryModeExit(
                sp.record(
                    balances=params.balances,
                    totalSupply=self.data.totalSupply,
                    userData=params.userData
                )
            )
        with sp.else_():
            scalingFactors = self.data.scalingFactors

            upScaledBalances = sp.compute(self.data.scaling_helpers['scale']((
                params.balances, scalingFactors, self.data.fixedPoint['mulDown'])))

            result.value = self._beforeExitPool(
                sp.record(
                    balances=upScaledBalances,
                    scalingFactors=scalingFactors,
                    userData=params.userData
                )
            )
        sptAmountIn, amountsOut, invariant = sp.match_tuple(
            result.value, 'sptAmountIn', 'amountsOut', 'invariant')

        downscaledAmounts = sp.compute(self.data.scaling_helpers['scale']((
            amountsOut, scalingFactors, self.data.fixedPoint['divDown'])))

        sp.result((sptAmountIn, downscaledAmounts, invariant))

    # @ sp.onchain_view()
    # def getPoolId(self):
    #     """
    #     * @dev  this Pool's ID, used when interacting with the Vault (to e.g. join the Pool or swap with it).
    #     *"""
    #     pass

    # @ sp.onchain_view()
    # def getSwapFeePercentage(self):
    #     """
    #     @dev  the current swap fee percentage as a 18 decimal fixed point number, so e.g. 1e17 corresponds to a
    #     10% swap fee.
    #     """
    #     pass

    # @ sp.onchain_view()
    # def getScalingFactors(self):
    #     """
    #     * @dev  the scaling factors of each of the Pool's tokens. This is an implementation detail that is typically
    #     * not relevant for outside parties, but which might be useful for some types of Pools.
    #     """
    #     pass

###########
# Internal Functions
###########

    def _addSwapFeeAmount(self, amount):
        # This returns amount + fee amount, so we round up (favoring a higher fee amount).
        return self.data.fixedPoint['divUp']((amount, FixedPoint.complement(self.data.entries['swapFeePercentage'])))

    def _subtractSwapFeeAmount(self, amount):
        # This returns amount - fee amount, so we round up (favoring a higher fee amount).
        feeAmount = self.data.fixedPoint['mulUp'](
            (amount, self.data.entries['swapFeePercentage']))
        return sp.as_nat(amount - feeAmount)

    def _setSwapFeePercentage(self, swapFeePercentage):
        sp.verify(swapFeePercentage >= _MIN_SWAP_FEE_PERCENTAGE,
                  Errors.MIN_SWAP_FEE_PERCENTAGE)
        sp.verify(swapFeePercentage <= _MAX_SWAP_FEE_PERCENTAGE,
                  Errors.MAX_SWAP_FEE_PERCENTAGE)

        self.data.entries['swapFeePercentage'] = swapFeePercentage

        sp.emit(swapFeePercentage, 'SwapFeePercentageChanged')

    def _computeScalingFactor(self, decimals):
        sp.set_type(decimals, sp.TNat)
        decimalsDifference = sp.as_nat(18 - decimals)
        return FixedPoint.ONE * (self.data.fixedPoint['pow']((sp.nat(10), decimalsDifference)))

    def _payProtocolFees(self, sptAmount):
        with sp.if_(sptAmount > 0):
            self._mintPoolTokens(
                self.data.protocolFeesCollector, sptAmount)

    def _setRecoveryMode(self, enabled):
        self.data.recoveryMode = enabled

        with sp.if_(enabled == False):
            self._onDisableRecoveryMode()

        sp.emit(enabled, 'RecoverModeStateChanged', with_type=True)
