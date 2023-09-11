import smartpy as sp

import contracts.interfaces.SymmetricEnums as Enums

import tests.helpers.MockSymmetric as helpers 

@sp.add_test(name="Successful batch swap")
def successful_batch_swap():
    env = helpers.setup_test_environment()
    pools = helpers.setup_test_pools(env["pool_factory"])
    helpers.add_test_liquidity(pools, env["vault"], env["admin"].address)    
    assets = {
        0: helpers.TOKENS["SYMM"],
        1: helpers.TOKENS["CTZ"],
        2: helpers.TOKENS["USDT"],
        3: helpers.TOKENS["uBTC"],
        4: helpers.TOKENS["YOU"],
    }
    # Assuming the function batchSwap takes a list of swaps
    swaps = {
        # Define swap1
        0: sp.record(
            poolId=pools["pool_1"]["pool_id"],
            assetInIndex=1,
            assetOutIndex=0,
            amount=sp.nat(1000000000000)
        ),
        1: sp.record(
            poolId=pools["pool_2"]["pool_id"],
            assetInIndex=0,
            assetOutIndex=2,
            amount=sp.nat(100)
        ),
        2: sp.record(
            poolId=pools["pool_3"]["pool_id"],
            assetInIndex=2,
            assetOutIndex=3,
            amount=sp.nat(10)
        ),
        3: sp.record(
            poolId=pools["pool_7"]["pool_id"],
            assetInIndex=3,
            assetOutIndex=4,
            amount=sp.nat(1000000000000)
        ),
        # Define swap2
        # ... and so on
    }

    swapLimits = {
        0: 10000000000000000000000,
        1: 10000000000000000000000,
        2: 10000000000000000000000,
        3: 10000000000000000000000,
        4: 10000000000000000000000,
    }

    funds = sp.record(
        sender=env["admin"].address, 
        recipient=env["admin"].address
        )

    env["vault"].batchSwap(sp.record(
        kind=Enums.GIVEN_OUT,
        swaps=swaps,
        assets=assets,
        funds=funds,
        limits=swapLimits,
        deadline=sp.timestamp(1),
    )).run(source=env["admin"].address)
        
    # Add verification checks
    # sp.verify(...)

@sp.add_test(name="Batch swap with mismatched asset and limit lengths")
def mismatched_asset_and_limit_lengths():
    env = helpers.setup_test_environment()
    pools = helpers.setup_test_pools(env["pool_factory"])
    helpers.add_test_liquidity(pools, env["vault"], env["admin"].address)    
    assets = {
        0: helpers.TOKENS["SYMM"],
        1: helpers.TOKENS["CTZ"],
        2: helpers.TOKENS["USDT"],
        3: helpers.TOKENS["uBTC"],
        4: helpers.TOKENS["YOU"],
    }
    # Assuming the function batchSwap takes a list of swaps
    swaps = {
        # Define swap1
        0: sp.record(
            poolId=pools["pool_1"]["pool_id"],
            assetInIndex=1,
            assetOutIndex=0,
            amount=sp.nat(1000000000000)
        ),
        1: sp.record(
            poolId=pools["pool_2"]["pool_id"],
            assetInIndex=0,
            assetOutIndex=2,
            amount=sp.nat(100)
        ),
        2: sp.record(
            poolId=pools["pool_3"]["pool_id"],
            assetInIndex=2,
            assetOutIndex=3,
            amount=sp.nat(10)
        ),
        3: sp.record(
            poolId=pools["pool_7"]["pool_id"],
            assetInIndex=3,
            assetOutIndex=4,
            amount=sp.nat(1000000000000)
        ),
        # Define swap2
        # ... and so on
    }

    swapLimits = {
        0: 10000000000000000000000,
        1: 10000000000000000000000,
        2: 10000000000000000000000,
        3: 10000000000000000000000,
    }

    funds = sp.record(
        sender=env["admin"].address, 
        recipient=env["admin"].address
        )

    env["vault"].batchSwap(sp.record(
        kind=Enums.GIVEN_OUT,
        swaps=swaps,
        assets=assets,
        funds=funds,
        limits=swapLimits,
        deadline=sp.timestamp(1),
    )).run(
        source=env["admin"].address,
        valid=False
        )


@sp.add_test(name="Batch swap with zero amount in between")
def zero_amount_in_between():
    env = helpers.setup_test_environment()
    pools = helpers.setup_test_pools(env["pool_factory"])
    helpers.add_test_liquidity(pools, env["vault"], env["admin"].address)    
    assets = {
        0: helpers.TOKENS["SYMM"],
        1: helpers.TOKENS["CTZ"],
        2: helpers.TOKENS["USDT"],
        3: helpers.TOKENS["uBTC"],
        4: helpers.TOKENS["YOU"],
    }
    # Assuming the function batchSwap takes a list of swaps
    swaps = {
        # Define swap1
        0: sp.record(
            poolId=pools["pool_1"]["pool_id"],
            assetInIndex=1,
            assetOutIndex=0,
            amount=sp.nat(1000000000000)
        ),
        1: sp.record(
            poolId=pools["pool_2"]["pool_id"],
            assetInIndex=0,
            assetOutIndex=2,
            amount=sp.nat(0)
        ),
        2: sp.record(
            poolId=pools["pool_3"]["pool_id"],
            assetInIndex=2,
            assetOutIndex=3,
            amount=sp.nat(10)
        ),
        3: sp.record(
            poolId=pools["pool_7"]["pool_id"],
            assetInIndex=3,
            assetOutIndex=4,
            amount=sp.nat(1000000000000)
        ),
        # Define swap2
        # ... and so on
    }

    swapLimits = {
        0: 10000000000000000000000,
        1: 10000000000000000000000,
        2: 10000000000000000000000,
        3: 10000000000000000000000,
        4: 10000000000000000000000,
    }

    funds = sp.record(
        sender=env["admin"].address, 
        recipient=env["admin"].address
        )

    env["vault"].batchSwap(sp.record(
        kind=Enums.GIVEN_OUT,
        swaps=swaps,
        assets=assets,
        funds=funds,
        limits=swapLimits,
        deadline=sp.timestamp(1),
    )).run(
        source=env["admin"].address,
        valid=False
        )

@sp.add_test(name="Batch swap after deadline")
def batch_swap_after_deadline():
    env = helpers.setup_test_environment()
    pools = helpers.setup_test_pools(env["pool_factory"])
    helpers.add_test_liquidity(pools, env["vault"], env["admin"].address)    
    assets = {
        0: helpers.TOKENS["SYMM"],
        1: helpers.TOKENS["CTZ"],
        2: helpers.TOKENS["USDT"],
        3: helpers.TOKENS["uBTC"],
        4: helpers.TOKENS["YOU"],
    }
    # Assuming the function batchSwap takes a list of swaps
    swaps = {
        # Define swap1
        0: sp.record(
            poolId=pools["pool_1"]["pool_id"],
            assetInIndex=1,
            assetOutIndex=0,
            amount=sp.nat(1000000000000)
        ),
        1: sp.record(
            poolId=pools["pool_2"]["pool_id"],
            assetInIndex=0,
            assetOutIndex=2,
            amount=sp.nat(100)
        ),
        2: sp.record(
            poolId=pools["pool_3"]["pool_id"],
            assetInIndex=2,
            assetOutIndex=3,
            amount=sp.nat(10)
        ),
        3: sp.record(
            poolId=pools["pool_7"]["pool_id"],
            assetInIndex=3,
            assetOutIndex=4,
            amount=sp.nat(1000000000000)
        ),
        # Define swap2
        # ... and so on
    }

    swapLimits = {
        0: 10000000000000000000000,
        1: 10000000000000000000000,
        2: 10000000000000000000000,
        3: 10000000000000000000000,
        4: 10000000000000000000000,
    }

    funds = sp.record(
        sender=env["admin"].address, 
        recipient=env["admin"].address
        )

    env["vault"].batchSwap(sp.record(
        kind=Enums.GIVEN_OUT,
        swaps=swaps,
        assets=assets,
        funds=funds,
        limits=swapLimits,
        deadline=sp.timestamp(0),
    )).run(
        source=env["admin"].address,
        now=sp.timestamp(1),
        valid=False
        )

@sp.add_test(name="Batch swap exceeding limit")
def batch_swap_exceed_limit():
    env = helpers.setup_test_environment()
    pools = helpers.setup_test_pools(env["pool_factory"])
    helpers.add_test_liquidity(pools, env["vault"], env["admin"].address)    
    assets = {
        0: helpers.TOKENS["SYMM"],
        1: helpers.TOKENS["CTZ"],
        2: helpers.TOKENS["USDT"],
        3: helpers.TOKENS["uBTC"],
        4: helpers.TOKENS["YOU"],
    }
    # Assuming the function batchSwap takes a list of swaps
    swaps = {
        # Define swap1
        0: sp.record(
            poolId=pools["pool_1"]["pool_id"],
            assetInIndex=1,
            assetOutIndex=0,
            amount=sp.nat(1000000000000)
        ),
        1: sp.record(
            poolId=pools["pool_2"]["pool_id"],
            assetInIndex=0,
            assetOutIndex=2,
            amount=sp.nat(100)
        ),
        2: sp.record(
            poolId=pools["pool_3"]["pool_id"],
            assetInIndex=2,
            assetOutIndex=3,
            amount=sp.nat(10)
        ),
        3: sp.record(
            poolId=pools["pool_7"]["pool_id"],
            assetInIndex=3,
            assetOutIndex=4,
            amount=sp.nat(1000000000000)
        ),
        # Define swap2
        # ... and so on
    }

    swapLimits = {
        0: 10000000000000000000000,
        1: 10000000000000000000000,
        2: 10000000000000000000000,
        3: 10000000000000000000000,
        4: 10000000000000000000000,
    }

    funds = sp.record(
        sender=env["admin"].address, 
        recipient=env["admin"].address
        )

    env["vault"].batchSwap(sp.record(
        kind=Enums.GIVEN_OUT,
        swaps=swaps,
        assets=assets,
        funds=funds,
        limits=swapLimits,
        deadline=sp.timestamp(1),
    )).run(source=env["admin"].address)