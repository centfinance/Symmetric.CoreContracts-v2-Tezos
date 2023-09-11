import smartpy as sp

import contracts.interfaces.SymmetricEnums as Enums

import tests.helpers.MockSymmetric as helpers 

# Assuming the necessary imports are already done at the beginning.

# 1. Successful exit
@sp.add_test(name="Successful exit")
def successful_exit():
    env = helpers.setup_test_environment()
    pools = helpers.setup_test_pools(env["pool_factory"])
    helpers.add_test_liquidity(pools, env["vault"], env["admin"].address)

    exact_spt_in_userData = sp.record(
        kind=Enums.EXACT_SPT_IN_FOR_TOKENS_OUT,
        amountsOut=sp.none,
        maxSPTAmountIn=sp.none,
        sptAmountIn=sp.some(sp.nat(999999997888455688)),
        tokenIndex=sp.none,
        recoveryModeExit=False,
    )

    # Define exit request
    exact_spt_in_request = sp.record(
        userData=exact_spt_in_userData,
        assets=pools["pool_1"]["tokens"],
        limits={
            0: sp.nat(500000000000000000),
            1: sp.nat(300000000000000000),
        }
    )

    env["vault"].exitPool(
        poolId=pools["pool_1"]["pool_id"],
        sender=env["admin"].address,
        recipient=env["admin"].address,
        request=exact_spt_in_request
    ).run(source=env["admin"].address)


    exact_token_out_userData = sp.record(
        kind=Enums.EXACT_SPT_IN_FOR_ONE_TOKEN_OUT,
        amountsOut=sp.none,
        maxSPTAmountIn=sp.none,
        sptAmountIn=sp.some(sp.nat(999999997888455688)),
        tokenIndex=sp.some(sp.nat(0)),
        recoveryModeExit=False,
    )

    # Define exit request
    exact_token_out_request = sp.record(
        userData=exact_token_out_userData,
        assets=pools["pool_1"]["tokens"],
        limits={
            0: sp.nat(500000000000000000),
            1: sp.nat(0),
        }
    )

    env["vault"].exitPool(
        poolId=pools["pool_1"]["pool_id"],
        sender=env["admin"].address,
        recipient=env["admin"].address,
        request=exact_token_out_request
    ).run(source=env["admin"].address)



    exact_tokens_out_userData = sp.record(
        kind=Enums.SPT_IN_FOR_EXACT_TOKENS_OUT,
        amountsOut=sp.some({
            0: sp.nat(3000000000000000000),
            1: sp.nat(5000000),
            2: sp.nat(200000000),
        }),
        maxSPTAmountIn=sp.some(sp.nat(10000000000000000000000)),
        sptAmountIn=sp.none,
        tokenIndex=sp.none,
        recoveryModeExit=False,
    )

    # Define exit request
    exact_tokens_out_request = sp.record(
        userData=exact_tokens_out_userData,
        assets=pools["pool_2"]["tokens"],
        limits={
            0: sp.nat(2000000000000000000),
            1: sp.nat(4000000),
            2: sp.nat(100000000),
        }
    )

    env["vault"].exitPool(
        poolId=pools["pool_2"]["pool_id"],
        sender=env["admin"].address,
        recipient=env["admin"].address,
        request=exact_tokens_out_request
    ).run(source=env["admin"].address)

# 1. Exit with a limit that's too low
@sp.add_test(name="Exit with a limit that is too high")
def exit_high_limit():
    env = helpers.setup_test_environment()
    pools = helpers.setup_test_pools(env["pool_factory"])
    helpers.add_test_liquidity(pools, env["vault"], env["admin"].address)

    exact_spt_in_userData = sp.record(
        kind=Enums.EXACT_SPT_IN_FOR_TOKENS_OUT,
        amountsOut=sp.none,
        maxSPTAmountIn=sp.none,
        sptAmountIn=sp.some(sp.nat(999999997888455688)),
        tokenIndex=sp.none,
        recoveryModeExit=False,
    )

    # Define exit request with a higher limit
    low_limit_request = sp.record(
        userData=exact_spt_in_userData,
        assets=pools["pool_1"]["tokens"],
        limits={
            0: sp.nat(100000000000000000000000),
            1: sp.nat(5),
        }
    )

    env["vault"].exitPool(
        poolId=pools["pool_1"]["pool_id"],
        sender=env["admin"].address,
        recipient=env["admin"].address,
        request=low_limit_request
    ).run(source=env["admin"].address, valid=False)


# 2. Exit without enough SPT tokens
@sp.add_test(name="Exit without enough SPT tokens")
def exit_no_tokens():
    env = helpers.setup_test_environment()
    pools = helpers.setup_test_pools(env["pool_factory"])

    exact_spt_in_userData = sp.record(
        kind=Enums.EXACT_SPT_IN_FOR_TOKENS_OUT,
        amountsOut=sp.none,
        maxSPTAmountIn=sp.none,
        sptAmountIn=sp.some(sp.nat(99999999788845568800000000000)),
        tokenIndex=sp.none,
        recoveryModeExit=False,
    )

    # Define exit request
    exact_spt_in_request = sp.record(
        userData=exact_spt_in_userData,
        assets=pools["pool_1"]["tokens"],
        limits={
            0: sp.nat(500000000000000000),
            1: sp.nat(300000000000000000),
        }
    )

    env["vault"].exitPool(
        poolId=pools["pool_1"]["pool_id"],
        sender=env["admin"].address,
        recipient=env["admin"].address,
        request=exact_spt_in_request
    ).run(source=env["admin"].address, valid=False)


# 3. Exit from a different source than `sp.source`
@sp.add_test(name="Exit from a different source")
def exit_different_source():
    env = helpers.setup_test_environment()
    pools = helpers.setup_test_pools(env["pool_factory"])
    helpers.add_test_liquidity(pools, env["vault"], env["admin"].address)
    wrong_source = sp.test_account('wrong_source').address

    exact_spt_in_userData = sp.record(
        kind=Enums.EXACT_SPT_IN_FOR_TOKENS_OUT,
        amountsOut=sp.none,
        maxSPTAmountIn=sp.none,
        sptAmountIn=sp.some(sp.nat(999999997888455688)),
        tokenIndex=sp.none,
        recoveryModeExit=False,
    )

    # Define exit request
    exact_spt_in_request = sp.record(
        userData=exact_spt_in_userData,
        assets=pools["pool_1"]["tokens"],
        limits={
            0: sp.nat(500000000000000000),
            1: sp.nat(300000000000000000),
        }
    )

    env["vault"].exitPool(
        poolId=pools["pool_1"]["pool_id"],
        sender=env["admin"].address,
        recipient=env["admin"].address,
        request=exact_spt_in_request
    ).run(source=wrong_source, valid=False)


# 4. Exit from an unregistered pool
@sp.add_test(name="Exit from an unregistered pool")
def exit_unregistered_pool():
    env = helpers.setup_test_environment()
    wrong_pool = sp.test_account('wrong_pool').address

    exact_spt_in_userData = sp.record(
        kind=Enums.EXACT_SPT_IN_FOR_TOKENS_OUT,
        amountsOut=sp.none,
        maxSPTAmountIn=sp.none,
        sptAmountIn=sp.some(sp.nat(999999997888455688)),
        tokenIndex=sp.none,
        recoveryModeExit=False,
    )
    
    tokens = sp.map({
        0: (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.some(sp.nat(0))),
        1: (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.some(sp.nat(1))),
    })
    # Define exit request
    exact_spt_in_request = sp.record(
        userData=exact_spt_in_userData,
        assets=tokens,
        limits={
            0: sp.nat(500000000000000000),
            1: sp.nat(300000000000000000),
        }
    )

    env["vault"].exitPool(
        poolId=(wrong_pool, sp.nat(1)),
        sender=env["admin"].address,
        recipient=env["admin"].address,
        request=exact_spt_in_request
    ).run(source=env["admin"].address, valid=False)


# 5. Exit with mismatched tokens
@sp.add_test(name="Exit with mismatched tokens")
def exit_mismatched_tokens():
    env = helpers.setup_test_environment()
    pools = helpers.setup_test_pools(env["pool_factory"])
    helpers.add_test_liquidity(pools, env["vault"], env["admin"].address)
    
    exact_spt_in_userData = sp.record(
        kind=Enums.EXACT_SPT_IN_FOR_TOKENS_OUT,
        amountsOut=sp.none,
        maxSPTAmountIn=sp.none,
        sptAmountIn=sp.some(sp.nat(999999997888455688)),
        tokenIndex=sp.none,
        recoveryModeExit=False,
    )

    # Modify the tokens to create a mismatch
    mismatched_assets = pools["pool_1"]["tokens"]
    mismatched_assets[1] = (sp.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'), sp.none)

    mismatched_request = sp.record(
        userData=exact_spt_in_userData,
        assets=mismatched_assets,
        limits={
            0: sp.nat(500000000000000000),
            1: sp.nat(300000000000000000),
        }
    )

    env["vault"].exitPool(
        poolId=pools["pool_1"]["pool_id"],
        sender=env["admin"].address,
        recipient=env["admin"].address,
        request=mismatched_request
    ).run(source=env["admin"].address, valid=False)



