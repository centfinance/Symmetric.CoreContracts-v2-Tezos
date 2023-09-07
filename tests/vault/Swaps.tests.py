import smartpy as sp

from contracts.vault.Swaps import Swaps

from contracts.pool_utils.BaseMinimalSwapInfoPool import Types as BMSIPTypes

import contracts.interfaces.SymmetricEnums as Enums

import tests.helpers.MockSymmetric as helpers 

t_joinUserData = sp.TRecord(
    kind=sp.TString,
    amountsIn=sp.TMap(sp.TNat, sp.TNat),
    minSPTAmountOut=sp.TOption(sp.TNat),
    tokenIndex=sp.TOption(sp.TNat),
    sptAmountOut=sp.TOption(sp.TNat),
    allT=sp.TOption(sp.TNat),
)

t_exitUserData = sp.TRecord(
    kind=sp.TString,
    amountsOut=sp.TMap(sp.TNat, sp.TNat),
    maxSPTAmountIn=sp.TOption(sp.TNat),
    tokenIndex=sp.TOption(sp.TNat),
    sptAmountIn=sp.TOption(sp.TNat),
    allT=sp.TOption(sp.TNat),
)

t_onJoinPool_params = sp.TRecord(
    poolId=sp.TBytes,
    sender=sp.TAddress,
    recipient=sp.TAddress,
    balances=sp.TMap(sp.TNat, sp.TNat),
    lastChangeBlock=sp.TNat,
    protocolSwapFeePercentage=sp.TNat,
    userData=t_joinUserData,
)

t_onExitPool_params = sp.TRecord(
    poolId=sp.TBytes,
    sender=sp.TAddress,
    recipient=sp.TAddress,
    balances=sp.TMap(sp.TNat, sp.TNat),
    lastChangeBlock=sp.TNat,
    protocolSwapFeePercentage=sp.TNat,
    userData=t_exitUserData,
)


class MockPool(sp.Contract):
    def __init__(self):
        sp.Contract.__init__(self)

    @sp.onchain_view()
    def onSwap(self, params):
        sp.set_type(params, BMSIPTypes.t_onSwap_params)
        sp.result(sp.nat(1000000000000000000))

    @sp.onchain_view()
    def beforeJoinPool(self, params):
        sp.set_type(params, t_onJoinPool_params)
        sp.result((sp.nat(0), sp.map(l={
            0: sp.nat(1000000000000000000),
            1: sp.nat(1000000000000000000),
        }, tkey=sp.TNat, tvalue=sp.TNat)))

    @sp.entry_point
    def onJoinPool(self, params):
        sp.set_type(params, t_onJoinPool_params)
        pass

    @sp.onchain_view()
    def beforeExitPool(self, params):
        sp.set_type(params, t_onExitPool_params)
        sp.result((sp.nat(0), sp.map(l={
            0: sp.nat(1000000000000000000),
            1: sp.nat(1000000000000000000),
        }, tkey=sp.TNat, tvalue=sp.TNat)))

    @sp.entry_point
    def onExitPool(self, params):
        sp.set_type(params, t_onExitPool_params)
        pass


class MockVault(sp.Contract, Swaps):
    def __init__(self):
        sp.Contract.__init__(self)
        Swaps.__init__(self)


def _toPoolId(pool, specialization, nonce):
    pack = sp.record(
        nonce=nonce,
        pool=pool,
        specialization=specialization
    )
    return sp.pack(pack)


# @sp.add_test(name="SwapsTest_1", profile=True)
# def test():
#     sc = sp.test_scenario()

#     alice = sp.test_account('Alice')

#     pool = MockPool()
#     sc += pool
#     pool2 = MockPool()
#     sc += pool2

#     c = MockVault()
#     sc += c

#     c.registerPool(sp.nat(1)).run(sender=pool.address)
#     c.registerPool(sp.nat(1)).run(sender=pool2.address)

#     assets = {
#         0: sp.record(
#             address=sp.address('tz1'),
#             id=sp.nat(0),
#             FA2=False,),
#         1: sp.record(
#             address=sp.address('tz1'),
#             id=sp.nat(1),
#             FA2=False,)
#     }

#     assets2 = {
#         0: sp.record(
#             address=sp.address('tz1'),
#             id=sp.nat(56),
#             FA2=True,),
#         1: sp.record(
#             address=sp.address('tz1'),
#             id=sp.nat(13),
#             FA2=False,)
#     }

#     limits = {
#         0: 100000000000000000000,
#         1: 100000000000000000000,
#     }
#     amountsIn = {
#         0: 1000000000000000000,
#         1: 1000000000000000000,
#     }
#     userData = sp.record(
#         kind='INIT',
#         amountsIn=amountsIn,
#         minSPTAmountOut=sp.none,
#         tokenIndex=sp.none,
#         sptAmountOut=sp.none,
#         allT=sp.none,
#     )

#     request = sp.record(
#         userData=userData,
#         assets=assets,
#         limits=limits,
#         useInternalBalance=False,
#     )

#     request2 = sp.record(
#         userData=userData,
#         assets=assets2,
#         limits=limits,
#         useInternalBalance=False,
#     )
#     sender = sp.test_account('sender').address
#     recipient = sender

#     assetManagers = [
#         sp.address('tz100000000000000000000000000000000000000')] * 2

#     poolId = _toPoolId(
#         pool.address,
#         sp.nat(1),
#         sp.nat(1),
#     )

#     poolId2 = _toPoolId(
#         pool2.address,
#         sp.nat(1),
#         sp.nat(1),
#     )
#     c.registerTokens(sp.record(
#         poolId=poolId,
#         tokens=assets,
#         assetManagers=assetManagers
#     ))

#     c.joinPool(
#         sp.record(
#             poolId=poolId,
#             sender=sender,
#             recipient=recipient,
#             request=request,
#         )
#     )

#     c.registerTokens(sp.record(
#         poolId=poolId2,
#         tokens=assets2,
#         assetManagers=assetManagers
#     ))

#     c.joinPool(
#         sp.record(
#             poolId=poolId2,
#             sender=sender,
#             recipient=recipient,
#             request=request2,
#         )
#     )

#     singleSwap = sp.record(
#         poolId=poolId,
#         kind='GIVEN_IN',
#         assetIn=assets[0],
#         assetOut=assets[1],
#         amount=sp.nat(12384759483945037),
#     )

#     funds = sp.record(
#         sender=sender,
#         fromInternalBalance=False,
#         recipient=recipient,
#         toInternalBalance=False,
#     )

#     swapParams = sp.record(
#         singleSwap=singleSwap,
#         funds=funds,
#         limit=sp.nat(0),
#         deadline=sp.timestamp(1)
#     )

#     c.swap(swapParams)

#     singleSwap = sp.record(
#         poolId=poolId,
#         kind='GIVEN_OUT',
#         assetIn=assets[1],
#         assetOut=assets[0],
#         amount=sp.nat(12384759483945037),
#     )

#     swapParams2 = sp.record(
#         singleSwap=singleSwap,
#         funds=funds,
#         limit=sp.nat(2000000000000000000),
#         deadline=sp.timestamp(1)
#     )

#     c.swap(swapParams2)

#     batchAssets = {
#         0: assets[0],
#         1: assets[1],
#         2: assets2[0],
#         3: assets2[1],
#     }

#     swaps = {
#         0: sp.record(
#             poolId=poolId,
#             assetInIndex=sp.nat(0),
#             assetOutIndex=sp.nat(1),
#             amount=sp.nat(12384759483945037),
#         ),
#         1: sp.record(
#             poolId=poolId2,
#             assetInIndex=sp.nat(2),
#             assetOutIndex=sp.nat(3),
#             amount=sp.nat(123847594839450),
#         ),
#     }

#     limits2 = {
#         0: 100000000000000000000,
#         1: 100000000000000000000,
#         2: 100000000000000000000,
#         3: 100000000000000000000,
#     }

#     c.batchSwap(sp.record(
#         kind='GIVEN_IN',
#         swaps=swaps,
#         assets=batchAssets,
#         funds=funds,
#         limits=limits2,
#         deadline=sp.timestamp(1,)
#     ))

# Test 1: Successful single swap
@sp.add_test(name="Successful single swap")
def successful_single_swap():
    # Setting up the test environment
    env = helpers.setup_test_environment()
    
    pools = helpers.setup_test_pools(env["pool_factory"])

    helpers.add_test_liquidity(pools, env["vault"])
    # Define the swap details
    singleSwap = sp.record(
        poolId=pools["pool_1"]["pool_id"], # Placeholder, you need to set it based on your system
        kind=Enums.GIVEN_IN,  # Assuming 0 represents GIVEN_IN
        assetIn=pools["pool_1"]["tokens"][0],
        assetOut=pools["pool_1"]["tokens"][1], # Placeholder
        amount=sp.nat(1000000000000000000),
    )

    funds = sp.record(
        sender=env["admin"].address, 
        recipient=env["admin"].address
        )
    
    env["vault"].swap(
        sp.record(
            singleSwap = singleSwap, 
            funds = funds, 
            limit = sp.nat(0), 
            deadline = sp.timestamp(1)
        )).run(source=env["admin"].address)
    
    # sp.verify(env.vault.balances["bobAddress"]["token2"] == 100)  # Or another assertion based on the swap logic

# Test 2: Swap with the same token for assetIn and assetOut
@sp.add_test(name="Swap with the same token")
def swap_same_token():
    env = helpers.setup_test_environment()

    pools = helpers.setup_test_pools(env["pool_factory"])

    helpers.add_test_liquidity(pools, env["vault"])

    singleSwap = sp.record(
        poolId=pools["pool_1"]["pool_id"], # Placeholder, you need to set it based on your system
        kind=Enums.GIVEN_IN,  # Assuming 0 represents GIVEN_IN
        assetIn=pools["pool_1"]["tokens"][0],
        assetOut=pools["pool_1"]["tokens"][0], # Placeholder
        amount=sp.nat(1000000000000000000),
    )

    funds = sp.record(
        sender=env["admin"].address, 
        recipient=env["admin"].address
        )
    
    env["vault"].swap(
        sp.record(
            singleSwap = singleSwap, 
            funds = funds, 
            limit = sp.nat(0), 
            deadline = sp.timestamp(1)
        )).run(
        source=env["admin"].address,
        valid=False
        )
    # Assuming the contract will raise an exception on an invalid swap. If it doesn't and returns an error value instead, adjust the assertion.

@sp.add_test(name="Swap with zero amount")
def swap_zero_amount():
    env = helpers.setup_test_environment()
    pools = helpers.setup_test_pools(env["pool_factory"])
    helpers.add_test_liquidity(pools, env["vault"])

    singleSwap = sp.record(
        poolId=pools["pool_1"]["pool_id"],
        kind=Enums.GIVEN_IN,
        assetIn=pools["pool_1"]["tokens"][0],
        assetOut=pools["pool_1"]["tokens"][1],
        amount=sp.nat(0),
    )

    funds = sp.record(
        sender=env["admin"].address, 
        recipient=env["admin"].address
        )
    
    env["vault"].swap(
        sp.record(
            singleSwap = singleSwap, 
            funds = funds, 
            limit = sp.nat(0), 
            deadline = sp.timestamp(1)
        )).run(
        source=env["admin"].address,
        valid=False
        )

@sp.add_test(name="Swap after deadline")
def swap_after_deadline():
    env = helpers.setup_test_environment()
    pools = helpers.setup_test_pools(env["pool_factory"])
    helpers.add_test_liquidity(pools, env["vault"])

    singleSwap = sp.record(
        poolId=pools["pool_1"]["pool_id"],
        kind=Enums.GIVEN_IN,
        assetIn=pools["pool_1"]["tokens"][0],
        assetOut=pools["pool_1"]["tokens"][1],
        amount=sp.nat(1000000000000000000),
    )

    past_deadline = sp.timestamp(0)  # Assuming the current timestamp is greater than 0
    
    funds = sp.record(
        sender=env["admin"].address, 
        recipient=env["admin"].address
        )
    
    env["vault"].swap(
        sp.record(
            singleSwap = singleSwap, 
            funds = funds, 
            limit = sp.nat(0), 
            deadline = past_deadline
        )).run(
        source=env["admin"].address,
        now=sp.timestamp(1),
        valid=False
        )

@sp.add_test(name="Swap with unsatisfied limit")
def swap_unsatisfied_limit():
    env = helpers.setup_test_environment()
    pools = helpers.setup_test_pools(env["pool_factory"])
    helpers.add_test_liquidity(pools, env["vault"])

    singleSwap = sp.record(
        poolId=pools["pool_1"]["pool_id"],
        kind=Enums.GIVEN_IN,
        assetIn=pools["pool_1"]["tokens"][0],
        assetOut=pools["pool_1"]["tokens"][1],
        amount=sp.nat(1000000000000000000),
    )

    unsatisfied_limit = sp.nat(1000000000000000000000)  # Assuming this limit will not be satisfied by the swap
    funds = sp.record(
        sender=env["admin"].address, 
        recipient=env["admin"].address
        )
    
    env["vault"].swap(
        sp.record(
            singleSwap = singleSwap, 
            funds = funds, 
            limit = unsatisfied_limit, 
            deadline = sp.timestamp(1)
        )).run(
        source=env["admin"].address,
        valid=False
        )
