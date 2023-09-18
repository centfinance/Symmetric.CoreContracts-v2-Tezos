import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

import contracts.utils.Utils as Utils

import contracts.vault.balances.BalanceAllocation as BalanceAllocation

from contracts.vault.PoolRegistry import PoolRegistry

class Types:

    TOKEN = sp.TPair(sp.TAddress, sp.TOption(sp.TNat))
    BALANCE = sp.TPair(sp.TNat, sp.TNat)

    REGISTER_TOKENS_PARAMS = sp.TRecord(
        poolId=sp.TPair(sp.TAddress, sp.TNat),
        tokens=sp.TMap(sp.TNat, TOKEN),
        assetManagers=sp.TOption(sp.TMap(sp.TNat, sp.TAddress))
    )

    TOKENS_TYPE = sp.TMap(sp.TNat, TOKEN)

    BALANCES_TYPE = sp.TMap(TOKEN, BALANCE)


class PoolTokens(
    PoolRegistry,
):
    """
    Represents a SmartPy contract to manage token registrations, balances, and queries for pools.

    The class enables a pool to register tokens and manage balances associated with those tokens. It also provides 
    mechanisms to query tokens and balances associated with a specific pool.

    Inheritance:
        Inherits from PoolRegistry.

    Attributes:
        poolsTokens (sp.big_map): A big map storing the tokens registered to each pool.
        poolsBalances (sp.big_map): A big map storing the balances of each token for a given pool.

    Entry Points:
        - registerTokens: Allows for the registration of tokens to a specified pool.
        - getPoolTokens: An on-chain view to fetch the tokens and their balances for a specific pool.

    Internal Methods:
        - _getPoolTokens: Retrieves the tokens and their respective total balances for a given pool.
        - _setPoolBalances: Sets the balances of tokens for a specific pool.
        - _getPoolBalance: Retrieves the balance for a specific token of a specific pool.
        - onlyPool: Verifies if the caller of an entry point is a registered pool.

    Note:
        The pools are uniquely identified by a pair of address and natural number (sp.TPair(sp.TAddress, sp.TNat)).
    """
    def __init__(self):
        """
        Initializes the PoolTokens with default values and sets up the initial storage.

        This constructor sets up the initial storage for the `poolsTokens` and `poolsBalances` attributes. It initializes
        these attributes with empty big_maps. Additionally, it calls the constructor of the inherited `PoolRegistry` class.
        """        
        self.update_initial_storage(
            poolsTokens=sp.big_map(
                l={},
                tkey=sp.TPair(sp.TAddress, sp.TNat),
                tvalue=Types.TOKENS_TYPE
            ),
            poolsBalances=sp.big_map(
                l={},
                tkey=sp.TPair(sp.TAddress, sp.TNat),
                tvalue=Types.BALANCES_TYPE,
            ),
        ),
        PoolRegistry.__init__(self)

    @sp.entry_point(lazify=False)
    def registerTokens(self, params):
        """
        Registers the specified tokens for a given pool.

        This entry point can only be called when the contract is not paused and can only be accessed by the specified pool.
        Tokens are added to the pool's registered token list. If the pool is registering tokens for the first time, 
        an empty balance map is also initialized for the pool.

        Parameters:
            params (REGISTER_TOKENS_PARAMS): Contains the pool ID, tokens to be registered, and optional asset managers.

        Events:
            - Emits a 'TokensRegistered' event upon successful registration of tokens.

        Notes:
            - The entry point verifies if the tokens are already registered to avoid duplicate registration.
            - The token list for the pool is either appended to or initialized based on whether the pool already has 
              registered tokens.

        """
        sp.set_type(params, Types.REGISTER_TOKENS_PARAMS)
        self.onlyUnpaused()
        self.onlyPool(params.poolId)

        with sp.if_(self.data.poolsTokens.contains(params.poolId)):
            registeredTokens = self.data.poolsTokens[params.poolId].values(
            )
            tokensAmount = sp.len(params.tokens)
            with sp.for_('i', sp.range(0, tokensAmount)) as i:
                prevSize = sp.len(
                    self.data.poolsTokens[params.poolId])
                t = params.tokens[i]
                sp.verify(Utils.list_contains(registeredTokens, t) == False)
                self.data.poolsTokens[params.poolId][prevSize] = t
        with sp.else_():
            self.data.poolsTokens[params.poolId] = params.tokens
            self.data.poolsBalances[params.poolId] = sp.map(
                l={}, tkey=Types.TOKEN, tvalue=Types.BALANCE)

        poolEvent = sp.record(
            poolId=params.poolId,
            tokens=params.tokens,
        )
        sp.emit(poolEvent, tag='TokensRegistered', with_type=True)

    @sp.onchain_view()
    def getPoolTokens(self, poolId):
        """
        Retrieves the tokens and their respective total balances for a given pool.

        This on-chain view function returns a tuple consisting of the list of tokens and their associated total balances for 
        a specified pool. 

        Parameters:
            poolId (TPair(sp.TAddress, sp.TNat)): Identifier for the pool for which tokens and balances are being fetched.

        Returns:
            tuple: A tuple containing:
                - List of tokens associated with the pool.
                - List of total balances for each token.

        Note:
            - The returned balances are the aggregate or total balances after applying the `BalanceAllocation.totals` 
              transformation on the raw balances fetched.

        """
        sp.set_type(poolId, sp.TPair(sp.TAddress, sp.TNat))
        (tokens, rawBalances) = self._getPoolTokens(poolId)
        balances = BalanceAllocation.totals(rawBalances)
        sp.result((
            tokens,
            balances,
        ))

    def _getPoolTokens(self, poolId):
        """
        Private method to retrieve the tokens and their respective balances for a given pool.

        Parameters:
            poolId (TPair(sp.TAddress, sp.TNat)): Identifier for the pool for which tokens and balances are being fetched.

        Returns:
            tuple: A tuple containing:
                - Dictionary (map) where each key is an index and the value is the associated token.
                - Dictionary (map) where each key is an index and the value is the balance for the corresponding token.

        Note:
            - This method provides raw data for the tokens and their balances, without applying any additional transformations.
        """
        poolTokens = self.data.poolsTokens[poolId]
        tokens = sp.compute(sp.map(l={}, tkey=sp.TNat, tvalue=Types.TOKEN))
        balances = sp.compute(
            sp.map(l={}, tkey=sp.TNat, tvalue=Types.BALANCE))

        with sp.for_('i', sp.range(0, sp.len(poolTokens))) as i:
            token = poolTokens[i]
            tokens[i] = token
            balances[i] = self.data.poolsBalances.get(poolId, {}).get(token, sp.pair(
                sp.nat(0),
                sp.nat(0),
            ))

        return (tokens, balances)

    def _setPoolBalances(
        self,
        params
    ):
        """
        Private method to set the balances of tokens for a specific pool.

        Parameters:
            params (object): Object containing the following keys:
                - poolId: Identifier for the pool for which the balances are being set.
                - tokens: Dictionary (map) where each key is an index and the value is the associated token.
                - balances: Dictionary (map) where each key is an index and the value is the balance for the corresponding token.

        Note:
            - This method updates the `poolsBalances` attribute with the balances provided for the specified tokens and pool.
        """
        with sp.for_('i', sp.range(0, sp.len(params.tokens))) as i:
            self.data.poolsBalances[params.poolId][params.tokens[i]
                                                   ] = params.balances[i]

    def _getPoolBalance(self, params):
        """
        Private method to retrieve the balance for a specific token of a specific pool.

        Parameters:
            params (object): Object containing the following keys:
                - poolId: Identifier for the pool from which the balance is being fetched.
                - token: The specific token for which the balance is being retrieved.

        Returns:
            tuple: Balance of the specified token for the given pool.

        Raises:
            Errors.INVALID_POOL_ID: If the provided poolId is not registered.
            Errors.TOKEN_NOT_REGISTERED: If the specified token is not registered for the pool.
        """
        return self.data.poolsBalances.get(
            params.poolId, message=Errors.INVALID_POOL_ID).get(params.token, message=Errors.TOKEN_NOT_REGISTERED)

    def onlyPool(self, poolId):
        """
        Verifies if the caller of an entry point is a registered pool.

        Parameters:
            poolId (TPair(sp.TAddress, sp.TNat)): Identifier for the pool being checked.

        Raises:
            Errors.INVALID_POOL_ID: If the provided poolId is not registered.
            Errors.CALLER_NOT_POOL: If the caller's address does not match the address associated with the poolId.
        """
        sp.verify(self.data.isPoolRegistered.contains(
            poolId), Errors.INVALID_POOL_ID)
        sp.verify(sp.sender == sp.fst(
            poolId), Errors.CALLER_NOT_POOL)
