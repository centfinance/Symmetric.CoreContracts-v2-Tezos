import smartpy as sp

import contracts.interfaces.SymmetricEnums as Enums

import tests.helpers.MockSymmetric as helpers 

@sp.add_test(name="Successful join")
def successful_join():
    env = helpers.setup_test_environment()
    pools = helpers.setup_test_pools(env["pool_factory"])
    helpers.add_test_liquidity(pools, env["vault"], env["admin"].address)    
    amountsIn = {
        0: sp.nat(1000000000000000000000),
        1: sp.nat(1000000000000000000000),
    }

    exact_tokens_in_userData = sp.record(
        kind=Enums.EXACT_TOKENS_IN_FOR_SPT_OUT,
        amountsIn=sp.some(amountsIn),
        minSPTAmountOut=sp.some(sp.nat(1)),
        tokenIndex=sp.none,
        sptAmountOut=sp.none,
        allT=sp.none,
    )
    # Define join request
    exact_tokens_In_request = sp.record(
        userData=exact_tokens_in_userData,
        assets=pools["pool_1"]["tokens"],
        limits={
            0: sp.nat(1000000000000000000001),
            1: sp.nat(1000000000000000000001),
            }
    )

    env["vault"].joinPool(
        poolId=pools["pool_1"]["pool_id"],
        sender=env["admin"].address,
        recipient=env["admin"].address,
        request=exact_tokens_In_request
    ).run(source=env["admin"].address)

    exact_spt_amounts_in = {
        0: sp.nat(1000000000000000000000),
        1: sp.nat(1000000000000000000000),
    }

    join_tokens_in_for_spt_userData = sp.record(
        kind=Enums.TOKEN_IN_FOR_EXACT_SPT_OUT,
        amountsIn=sp.some(exact_spt_amounts_in),
        minSPTAmountOut=sp.none,
        tokenIndex=sp.some(sp.nat(0)),
        sptAmountOut=sp.some(sp.nat(1000000000000000000000)),
        allT=sp.none,
    )
    # Define join request
    join_tokens_in_for_spt_request = sp.record(
        userData=join_tokens_in_for_spt_userData,
        assets=pools["pool_1"]["tokens"],
        limits={
            0: sp.nat(1000000000000000000001),
            1: sp.nat(1000000000000000000001),
            }
    )

    env["vault"].joinPool(
        poolId=pools["pool_1"]["pool_id"],
        sender=env["admin"].address,
        recipient=env["admin"].address,
        request=join_tokens_in_for_spt_request
    ).run(source=env["admin"].address)

    join_all_tokens_in_userData = sp.record(
        kind=Enums.ALL_TOKENS_IN_FOR_EXACT_SPT_OUT,
        amountsIn=sp.none,
        minSPTAmountOut=sp.none,
        tokenIndex=sp.none,
        sptAmountOut=sp.none,
        allT=sp.some(sp.nat(1000000000000000000000)),
    )
    # Define join request
    join_all_tokens_in_request = sp.record(
        userData=join_all_tokens_in_userData,
        assets=pools["pool_1"]["tokens"],
        limits={
            0: sp.nat(1000000000000000000001),
            1: sp.nat(1000000000000000000001),
            }
    )

    env["vault"].joinPool(
        poolId=pools["pool_1"]["pool_id"],
        sender=env["admin"].address,
        recipient=env["admin"].address,
        request=join_all_tokens_in_request
    ).run(source=env["admin"].address)

    # Add verification checks
    # sp.verify(...)

# 1. Join with a limit that's too low
@sp.add_test(name="Join with a limit that is too low")
def join_low_limit():
    env = helpers.setup_test_environment()
    pools = helpers.setup_test_pools(env["pool_factory"])
    helpers.add_test_liquidity(pools, env["vault"], env["admin"].address)    
    # Define join request with a lower limit
    amountsIn = {
        0: sp.nat(1000000000000000000000),
        1: sp.nat(1000000000000000000000),
    }

    exact_tokens_in_userData = sp.record(
        kind=Enums.EXACT_TOKENS_IN_FOR_SPT_OUT,
        amountsIn=sp.some(amountsIn),
        minSPTAmountOut=sp.some(sp.nat(1)),
        tokenIndex=sp.none,
        sptAmountOut=sp.none,
        allT=sp.none,
    )
    # Define join request
    low_limit_request = sp.record(
        userData=exact_tokens_in_userData,
        assets=pools["pool_1"]["tokens"],
        limits={
            0: sp.nat(50),
            1: sp.nat(50),
            }
    )
    
    # Expecting an error here
    env["vault"].joinPool(
            poolId=pools["pool_1"]["pool_id"],
            sender=env["admin"].address,
            recipient=env["admin"].address,
            request=low_limit_request
        ).run(source=env["admin"].address, valid=False)

# 2. Join without enough tokens
@sp.add_test(name="Join without enough tokens")
def join_no_tokens():
    env = helpers.setup_test_environment()
    pools = helpers.setup_test_pools(env["pool_factory"])
    
    amountsIn = {
        0: sp.nat(1000000000000000000000),
        1: sp.nat(1000000000000000000000),
    }

    exact_tokens_in_userData = sp.record(
        kind=Enums.EXACT_TOKENS_IN_FOR_SPT_OUT,
        amountsIn=sp.some(amountsIn),
        minSPTAmountOut=sp.some(sp.nat(1)),
        tokenIndex=sp.none,
        sptAmountOut=sp.none,
        allT=sp.none,
    )
    # Define join request
    exact_tokens_In_request = sp.record(
        userData=exact_tokens_in_userData,
        assets=pools["pool_1"]["tokens"],
        limits={
            0: sp.nat(1000000000000000000001),
            1: sp.nat(1000000000000000000001),
            }
    )
    # Don't add liquidity, so there are no tokens
    env["vault"].joinPool(
            poolId=pools["pool_1"]["pool_id"],
            sender=env["admin"].address,
            recipient=env["admin"].address,
            request=exact_tokens_In_request
        ).run(source=env["admin"].address, valid=False)

# 3. Join from a different source than `sp.source`
@sp.add_test(name="Join from a different source")
def join_different_source():
    env = helpers.setup_test_environment()
    pools = helpers.setup_test_pools(env["pool_factory"])
    helpers.add_test_liquidity(pools, env["vault"], env["admin"].address)    
    wrong_source = sp.test_account('wrong_source').address
    
    amountsIn = {
        0: sp.nat(1000000000000000000000),
        1: sp.nat(1000000000000000000000),
    }

    exact_tokens_in_userData = sp.record(
        kind=Enums.EXACT_TOKENS_IN_FOR_SPT_OUT,
        amountsIn=sp.some(amountsIn),
        minSPTAmountOut=sp.some(sp.nat(1)),
        tokenIndex=sp.none,
        sptAmountOut=sp.none,
        allT=sp.none,
    )
    # Define join request
    exact_tokens_In_request = sp.record(
        userData=exact_tokens_in_userData,
        assets=pools["pool_1"]["tokens"],
        limits={
            0: sp.nat(1000000000000000000001),
            1: sp.nat(1000000000000000000001),
            }
    )
    
    # Using a different source than sender
    env["vault"].joinPool(
            poolId=pools["pool_1"]["pool_id"],
            sender=env["admin"].address,
            recipient=env["admin"].address,
            request=exact_tokens_In_request
        ).run(source=wrong_source, valid=False)

# 4. Join with an unregistered pool
@sp.add_test(name="Join with an unregistered pool")
def join_unregistered_pool():
    env = helpers.setup_test_environment()
    wrong_pool = sp.test_account('wrong_source').address

    amountsIn = {
        0: sp.nat(1000000000000000000000),
        1: sp.nat(1000000000000000000000),
    }

    exact_tokens_in_userData = sp.record(
        kind=Enums.EXACT_TOKENS_IN_FOR_SPT_OUT,
        amountsIn=sp.some(amountsIn),
        minSPTAmountOut=sp.some(sp.nat(1)),
        tokenIndex=sp.none,
        sptAmountOut=sp.none,
        allT=sp.none,
    )

    tokens = sp.map({
        0: (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.some(sp.nat(0))),
        1: (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.some(sp.nat(1))),
    })
    # Define join request
    exact_tokens_In_request = sp.record(
        userData=exact_tokens_in_userData,
        assets=tokens,
        limits={
            0: sp.nat(1000000000000000000001),
            1: sp.nat(1000000000000000000001),
            }
    )
    # Don't set up pools, so the pool remains unregistered
    env["vault"].joinPool(
            poolId=(wrong_pool, sp.nat(1)),
            sender=env["admin"].address,
            recipient=env["admin"].address,
            request=exact_tokens_In_request
        ).run(source=env["admin"].address, valid=False)

# 5. Join with mismatched tokens
@sp.add_test(name="Join with mismatched tokens")
def join_mismatched_tokens():
    env = helpers.setup_test_environment()
    pools = helpers.setup_test_pools(env["pool_factory"])
    helpers.add_test_liquidity(pools, env["vault"], env["admin"].address)    
    amountsIn = {
        0: sp.nat(1000000000000000000000),
        1: sp.nat(1000000000000000000000),
    }

    exact_tokens_in_userData = sp.record(
        kind=Enums.EXACT_TOKENS_IN_FOR_SPT_OUT,
        amountsIn=sp.some(amountsIn),
        minSPTAmountOut=sp.some(sp.nat(1)),
        tokenIndex=sp.none,
        sptAmountOut=sp.none,
        allT=sp.none,
    )
        # Modify the tokens to create a mismatch
    mismatched_assets = pools["pool_1"]["tokens"]
    mismatched_assets[1] = (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.none)

    # Define join request
    mismatched_request = sp.record(
        userData=exact_tokens_in_userData,
        assets=mismatched_assets,
        limits={
            0: sp.nat(1000000000000000000001),
            1: sp.nat(1000000000000000000001),
            }
    )

    env["vault"].joinPool(
            poolId=pools["pool_1"]["pool_id"],
            sender=env["admin"].address,
            recipient=env["admin"].address,
            request=mismatched_request
        ).run(source=env["admin"].address, valid=False)

