import smartpy as sp


class Types:
    # TOKEN = sp.TRecord(
    #     address=sp.TAddress,
    #     id=sp.TNat,
    #     FA2=sp.TBool,
    # )
    TOKEN = sp.TPair(sp.TAddress, sp.TOption(sp.TNat))

    TOKENS = sp.TMap(sp.TNat, TOKEN)

    REGISTER_TOKENS_PARAMS = sp.TRecord(
        poolId=sp.TPair(sp.TAddress, sp.TNat),
        tokens=TOKENS,
        assetManagers=sp.TOption(sp.TMap(sp.TNat, sp.TAddress)),
    )


def registerPool(vault, tokens, assetManagers):
    nonce = sp.compute(sp.view('getNextPoolNonce', vault, sp.unit,
                               t=sp.TNat).open_some("Invalid view"))

    poolId = (sp.self_address, nonce)

    registerPool = sp.contract(sp.TUnit, vault, "registerPool").open_some(
        "INTERFACE_MISMATCH")

    registerTokens = sp.contract(Types.REGISTER_TOKENS_PARAMS, vault, "registerTokens").open_some(
        "INTERFACE_MISMATCH")
    registerTokensParams = sp.record(
        poolId=poolId,
        tokens=tokens,
        assetManagers=assetManagers
    )

    sp.transfer(sp.unit, sp.tez(0), registerPool)
    sp.transfer(registerTokensParams, sp.tez(0), registerTokens)

    return poolId
