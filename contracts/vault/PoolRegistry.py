import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors



class PoolRegistry:
    """
    Represents a SmartPy contract to manage the registration of pools.

    The class facilitates pool registration, tracking registered pools, and querying pool-related information. 
    Pools are uniquely identified by a pair comprising of the address and a nonce (sp.TPair(sp.TAddress, sp.TNat)).

    Attributes:
        isPoolRegistered (sp.big_map): A big map to track registered pools. A registered pool is identified 
            by its unique poolId and mapped to sp.TUnit to indicate its presence.
        nextPoolNonce (sp.nat): A counter that helps in generating a unique nonce for every new pool.

    Entry Points:
        - registerPool: Allows for the registration of new pools.
        - getNextPoolNonce: An on-chain view to fetch the next nonce for pool registration.

    Internal Methods:
        - _ensureRegisteredPool: Ensures that a given poolId is registered in the contract.
    """
    def __init__(self):
        """
        Initializes the PoolRegistry with default values.

        Sets up the initial storage with an empty `isPoolRegistered` big_map and a `nextPoolNonce` starting from 1.
        """
        self.update_initial_storage(
            isPoolRegistered=sp.big_map(
                l={},
                tkey=sp.TPair(sp.TAddress, sp.TNat),
                tvalue=sp.TUnit,
            ),
            nextPoolNonce=sp.nat(1)
        )

    @sp.entry_point(lazify=False)
    def registerPool(self):
        """
        Registers a new pool to the contract.

        This entry point can only be called when the contract is not paused. On successful registration, 
        the pool is added to the `isPoolRegistered` big_map, and the `nextPoolNonce` is incremented.

        Events:
            - Emits a 'PoolRegistered' event upon successful registration of a pool.

        Note:
            - The poolId for a new pool is generated using the sender's address and the current value 
              of `nextPoolNonce`.
        """
        self.onlyUnpaused()
        poolId = (sp.sender, sp.compute(self.data.nextPoolNonce))

        self.data.isPoolRegistered[poolId] = sp.unit

        self.data.nextPoolNonce += 1

        poolEvent = sp.record(
            poolId=poolId,
            pool=sp.sender,
        )
        sp.emit(poolEvent, tag='PoolRegistered', with_type=True)

    @sp.onchain_view()
    def getNextPoolNonce(self):
        """
        Fetches the next available nonce for pool registration.

        This on-chain view function returns the next nonce which will be used to generate the poolId for 
        the next pool registration.

        Returns:
            sp.nat: The next available nonce for pool registration.
        """
        sp.result(self.data.nextPoolNonce)

    def _ensureRegisteredPool(self, poolId):
        """
        Validates that a given poolId is registered in the contract.

        Parameters:
            poolId (TPair(sp.TAddress, sp.TNat)): Identifier for the pool to be checked.

        Raises:
            Errors.INVALID_POOL_ID: If the provided poolId is not registered.
        """
        sp.verify(self.data.isPoolRegistered.contains(poolId), Errors.INVALID_POOL_ID)