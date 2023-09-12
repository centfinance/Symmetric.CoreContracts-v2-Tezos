import smartpy as sp

import tests.helpers.MockSymmetric as helpers 


@sp.add_test(name="Enable and Disable Recovery Mode")
def enable_recovery_mode():
    env = helpers.setup_test_environment()
    sc = env["scenario"]
    pools = helpers.setup_test_pools(env["pool_factory"])
    helpers.add_test_liquidity(pools, env["vault"], env["admin"].address)
    
    weighted_pool = sc.dynamic_contract(0, env["pool_factory"]._creationCode)

    weighted_pool.call("enableRecoveryMode", sp.unit).run(sender=env["admin"])

    sc.verify(weighted_pool.data.recoveryMode == True)
    
    weighted_pool.call("disableRecoveryMode", sp.unit).run(sender=env["admin"])

    sc.verify(weighted_pool.data.recoveryMode == False)

@sp.add_test(name="Recovery mode must be enabled by admin")
def recovery_mode_must_be_enabled_by_admin():
    env = helpers.setup_test_environment()
    sc = env["scenario"]
    pools = helpers.setup_test_pools(env["pool_factory"])
    helpers.add_test_liquidity(pools, env["vault"], env["admin"].address)
    not_admin = sp.test_account("not_admin").address
    
    weighted_pool = sc.dynamic_contract(0, env["pool_factory"]._creationCode)

    weighted_pool.call("enableRecoveryMode", sp.unit).run(sender=not_admin, valid=False)

    sc.verify(weighted_pool.data.recoveryMode == False)
    
    weighted_pool.call("disableRecoveryMode", sp.unit).run(sender=not_admin, valid=False)

@sp.add_test(name="Can exit pool when recovery mode is enabled")
def can_exit_pool_when_recovery_mode_enabled():
    env = helpers.setup_test_environment()
    sc = env["scenario"]
    pools = helpers.setup_test_pools( env["pool_factory"])
    helpers.add_test_liquidity(pools, env["vault"], env["admin"].address)

    weighted_pool = sc.dynamic_contract(0, env["pool_factory"]._creationCode)

    weighted_pool.call("enableRecoveryMode", sp.unit).run(sender=env["admin"])

    recovery_exit_userData = sp.record(
        kind=0,
        amountsOut=sp.none,
        maxSPTAmountIn=sp.none,
        sptAmountIn=sp.some(sp.nat(999999997888455688)),
        tokenIndex=sp.none,
        recoveryModeExit=True,
    )

    # Define exit request
    recovery_exit_request = sp.record(
        userData=recovery_exit_userData,
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
        request=recovery_exit_request
    ).run(source=env["admin"].address)

@sp.add_test(name="Can not exit pool when recovery mode is disabled")
def can_not_exit_pool_when_recovery_mode_disabled():
    env = helpers.setup_test_environment()
    pools = helpers.setup_test_pools( env["pool_factory"])
    helpers.add_test_liquidity(pools, env["vault"], env["admin"].address)

    recovery_exit_userData = sp.record(
        kind=0,
        amountsOut=sp.none,
        maxSPTAmountIn=sp.none,
        sptAmountIn=sp.some(sp.nat(999999997888455688)),
        tokenIndex=sp.none,
        recoveryModeExit=True,
    )

    # Define exit request
    recovery_exit_request = sp.record(
        userData=recovery_exit_userData,
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
        request=recovery_exit_request
    ).run(source=env["admin"].address, valid=False)


