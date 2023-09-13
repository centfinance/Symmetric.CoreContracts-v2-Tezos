'''
BasePool Smart Contract for Tezos
----------------------------------
The BasePool smart contract provides the core functionalities for user interactions in a pool setting. 
Users can join or exit the pool, and the contract ensures proper handling of assets and tokens during 
these operations. The contract is designed to be secure and integrates administrative and pausable 
functionalities to provide enhanced control over the pool's operations.

Main Features:
- Administrable: Allows administrative control over the contract.
- Pausable: Permits pausing the contract operations.
- SymmetricPoolToken: Handles the creation and management of pool tokens.
'''

# Import required modules and contracts
import smartpy as sp
import contracts.interfaces.SymmetricErrors as Errors
import contracts.interfaces.SymmetricEnums as Enums
import contracts.utils.math.FixedPoint as FixedPoint
import contracts.pool_utils.lib.PoolRegistrationLib as PoolRegistrationLib
from contracts.pool_utils.SymmetricPoolToken import SymmetricPoolToken
from contracts.utils.mixins.Administrable import Administrable
from contracts.utils.mixins.Pausable import Pausable

# Define constants
_DEFAULT_MINIMUM_SPT = 1000000
_MIN_SWAP_FEE_PERCENTAGE = 1000000000000
_MAX_SWAP_FEE_PERCENTAGE = 100000000000000000

# Interface for the BasePool
class IBasePool:
    '''
    JOIN_USER_DATA:
    A structure defining the specific user data related to joining the pool.

    Fields:
    - kind (TNat): Specifies the type or method of joining. Different numbers can represent different join strategies or logic.
    - amountsIn (TOption(TMap(TNat, sp.TNat))): An optional map of token IDs to the respective amounts the user intends to deposit into the pool. This may not be set if the kind implies a different strategy.
    - minSPTAmountOut (TOption(TNat)): The minimum amount of pool tokens the user expects to receive for their deposit. It can act as a safety mechanism to ensure the user receives an expected value.
    - sptAmountOut (TOption(TNat)): An optional field specifying the exact amount of pool tokens the user intends to receive.
    - tokenIndex (TOption(TNat)): An optional field indicating the index or ID of a specific token in context, used for operations that concern a single token.
    - allT (TOption(TNat)): An optional field, the exact purpose of which would be derived from the pool's logic or requirements.
    '''
    JOIN_USER_DATA = sp.TRecord(
        kind=sp.TNat,
        amountsIn=sp.TOption(sp.TMap(sp.TNat, sp.TNat)),
        minSPTAmountOut=sp.TOption(sp.TNat),
        sptAmountOut=sp.TOption(sp.TNat),
        tokenIndex=sp.TOption(sp.TNat),
        allT=sp.TOption(sp.TNat),
    )

    '''
    EXIT_USER_DATA:
    A structure defining the specific user data related to exiting the pool.

    Fields:
    - kind (TNat): Specifies the type or method of exiting. Different numbers can represent different exit strategies or logic.
    - amountsOut (TOption(TMap(TNat, sp.TNat))): An optional map of token IDs to the respective amounts the user intends to withdraw from the pool. This may not be set if the kind implies a different strategy.
    - maxSPTAmountIn (TOption(TNat)): The maximum amount of pool tokens the user is willing to spend to retrieve their assets. Acts as a safety mechanism.
    - sptAmountIn (TOption(TNat)): An optional field specifying the exact number of pool tokens the user intends to use for the exit.
    - tokenIndex (TOption(TNat)): An optional field indicating the index or ID of a specific token in context, used for operations that concern a single token.
    - recoveryModeExit (TBool): Indicates if the exit action is being done in the context of a recovery mode scenario, usually indicating exceptional or emergency circumstances.
    '''
    EXIT_USER_DATA = sp.TRecord(
        kind=sp.TNat,
        amountsOut=sp.TOption(sp.TMap(sp.TNat, sp.TNat)),
        maxSPTAmountIn=sp.TOption(sp.TNat),
        sptAmountIn=sp.TOption(sp.TNat),
        tokenIndex=sp.TOption(sp.TNat),
        recoveryModeExit=sp.TBool,
    )

    # Parameters after joining the pool
    t_after_join_pool_params = sp.TRecord(
        poolId=sp.TPair(sp.TAddress, sp.TNat),
        balances=sp.TMap(sp.TNat, sp.TNat),
        recipient=sp.TAddress,
        amountsIn=sp.TMap(sp.TNat, sp.TNat),
        sptAmountOut=sp.TNat,
        invariant=sp.TNat,
    )

    # Parameters after exiting the pool
    t_after_exit_pool_params = sp.TRecord(
        poolId=sp.TPair(sp.TAddress, sp.TNat),
        balances=sp.TMap(sp.TNat, sp.TNat),
        sender=sp.TAddress,
        amountsOut=sp.TMap(sp.TNat, sp.TNat),
        sptAmountIn=sp.TNat,
        invariant=sp.TNat,
        recoveryModeExit=sp.TBool,
    )

    # Parameters before joining the pool
    t_before_join_pool_params = sp.TRecord(
        balances=sp.TMap(sp.TNat, sp.TNat),
        userData=JOIN_USER_DATA,
    )

    # Parameters before exiting the pool
    t_before_exit_pool_params = sp.TRecord(
        balances=sp.TMap(sp.TNat, sp.TNat),
        userData=EXIT_USER_DATA,
    )

    # Helpers for interacting with BasePool from other contracts
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
    """
    Reference implementation for the base layer of a Pool contract.
    
    Manages a single Pool with optional Asset Managers, an admin-controlled swap fee percentage,
    and an emergency pause mechanism.
    
    This Pool pays protocol fees by minting SPT directly to the ProtocolFeeCollector. This results in the underlying tokens continuing to provide liquidity
    for traders, while still keeping gas usage to a minimum since only a single token (the SPT) is transferred.
    
    Note:
        - Neither swap fees nor the pause mechanism are used by this contract. They are passed through so that
          derived contracts can use them via the `_addSwapFeeAmount` and `_subtractSwapFeeAmount` functions, and the
          `whenNotPaused` modifier.
          
        - Because this contract doesn't implement the swap hooks, derived contracts should generally inherit from
          BaseGeneralPool or BaseMinimalSwapInfoPool. Otherwise, subclasses must inherit from the corresponding interfaces
          and implement the swap callbacks themselves.
    """

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
        """
        Initializes the pool by registering it using the PoolRegistrationLib.
        
        This operation is only allowed once per pool. On successful registration, 
        the poolId is stored and the pool is marked as initialized.
        
        Raises:
            - VerificationError if the pool is already initialized.

        Side Effects:
            - Sets the poolId for the contract.
            - Marks the pool as initialized.
        """
        sp.verify(self.data.initialized == False)

        poolId = PoolRegistrationLib.registerPool(
            vault=self.data.vault,
            tokens=self.data.tokens,
            assetManagers=sp.none,
        )

        self.data.poolId = sp.some(poolId)
        self.data.initialized = True

    @sp.entry_point(lazify=False)
    def setSwapFeePercentage(self, swapFeePercentage):
        """
        Set the swap fee percentage.

        This is a permissioned function and is disabled if the pool is paused. The swap fee must fall within the
        bounds set by MIN_SWAP_FEE_PERCENTAGE and MAX_SWAP_FEE_PERCENTAGE.

        Raises:
            - `SwapFeePercentageChanged` event.

        :param swapFeePercentage: The swap fee percentage to be set.
        """
        self.onlyUnpaused()
        self.onlyAdministrator()
        self._setSwapFeePercentage(swapFeePercentage)

    @sp.entry_point(lazify=False)
    def enableRecoveryMode(self):
        '''
        @notice Enable recovery mode, offering a specialized safe exit pathway for LPs.
        @dev Does not affect other pool operations. Some pools might 
        operate in a "safer" manner to prevent failures, striving to maintain the pool running, even under 
        abnormal conditions.
        
        Requires:
        - Only an administrator can call this function.
        - Recovery mode must not be currently active.
        '''
        self.onlyAdministrator()
        sp.verify(self.data.recoveryMode == False, Errors.IN_RECOVERY_MODE)
        self._setRecoveryMode(True)

    @sp.entry_point(lazify=False)
    def disableRecoveryMode(self):
        '''
        @notice Disable recovery mode, turning off the special safe exit route for LPs.
        @dev It's advised to keep the mode active solely as long as absolutely required.
        
        Requires:
        - Only an administrator can call this function.
        - Recovery mode must currently be active.
        '''
        self.onlyAdministrator()
        sp.verify(self.data.recoveryMode == True, Errors.NOT_IN_RECOVERY_MODE)
        self._setRecoveryMode(False)


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
        '''
        This entry point is called by the Vault after the result from beforeJoinPool.

        Params:
        - poolId (TPair(TAddress, TNat)): Identifies the pool with an address and a natural number.
        - balances (TMap(TNat, TNat)): Represents the balance of each token in the pool with a mapping of token ID to its respective balance.
        - recipient (TAddress): Address of the recipient who will receive the tokens.
        - amountsIn (TMap(TNat, TNat)): Maps each token ID to the amount that has been deposited into the pool.
        - sptAmountOut (TNat): The amount of pool tokens the user will receive in exchange for their deposit.
        - invariant (TNat): A value representing the invariant of the pool after the join action, useful for mathematical calculations and ensuring pool stability.
        '''
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
        '''
        This entry point is called by the Vault after the result from beforeJExitPool.

        Params:
        - poolId (TPair(TAddress, TNat)): Identifies the pool with an address and a natural number.
        - balances (TMap(TNat, TNat)): Represents the balance of each token in the pool with a mapping of token ID to its respective balance.
        - sender (TAddress): Address of the user who is exiting the pool.
        - amountsOut (TMap(TNat, TNat)): Maps each token ID to the amount that will be withdrawn from the pool.
        - sptAmountIn (TNat): The amount of pool tokens the user is using to exit and retrieve their assets.
        - invariant (TNat): A value representing the invariant of the pool after the exit action.
        - recoveryModeExit (TBool): Indicates if the exit action was triggered during a recovery mode scenario.
        '''
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
        '''
        This on chain view is called by the vault before the afterJoinPool entrypoint

        Params:
        - balances (TMap(TNat, TNat)): Represents the expected balance of each token in the pool.
        - userData (JOIN_USER_DATA): Specific user data related to joining the pool. The exact fields and purposes are defined within the JOIN_USER_DATA type.
        '''
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

        sp.result((sptAmountOut, downscaledAmounts, invariant))

    @sp.onchain_view()
    def beforeExitPool(
        self,
        params,
    ):
        '''
        This on chain view is called by the vault before the afterJoinPool entrypoint

        Params:
        - balances (TMap(TNat, TNat)): Represents the expected balance of each token in the pool.
        - userData (EXIT_USER_DATA): Specific user data related to exiting the pool. The exact fields and purposes are defined within the EXIT_USER_DATA type.
        '''
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



###########
# Internal Functions
###########
    @sp.private_lambda(with_storage='read-only')
    def onlyVault(self, poolId):
        sp.verify(sp.sender == self.data.vault)
        sp.verify(poolId == self.data.poolId)
        
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
    
    def _setRecoveryMode(self, enabled):
        self.data.recoveryMode = enabled

        with sp.if_(enabled == False):
            self._onDisableRecoveryMode()

        sp.emit(enabled, 'RecoveryModeStateChanged', with_type=True)
