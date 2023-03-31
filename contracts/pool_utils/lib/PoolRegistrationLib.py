import smartpy as sp


class Types:
    TOKEN = sp.TRecord(
        address=sp.TAddress,
        id=sp.TNat,
        FA2=sp.TBool,
    )

    TOKENS = sp.TMap(sp.TNat, TOKEN)

    REGISTER_TOKENS_PARAMS = sp.TRecord(
        poolId=sp.TPair(sp.TAddress, sp.TNat),
        tokens=TOKENS,
        assetManagers=sp.TOption(sp.TMap(sp.TNat, sp.TAddress)),
    )


# def preparePool(vault, specialization, tokens):
#     # Create empty list of size tokens.length as we don't need assetManagers
#     assetManagers = [sp.address(
#         'tz100000000000000000000000000000000000000')] * tokens.length
#     return (registerPool(sp.record(vault=vault, specialization=specialization,
#                                          tokens=tokens, assetManagers=assetManagers)))


def registerPool(vault, specialization, tokens, assetManagers):
    nonce = sp.compute(sp.view('getNextPoolNonce', vault, sp.unit,
                               t=sp.TNat).open_some("Invalid view"))

    poolId = (sp.self_address, nonce)

    registerPool = sp.contract(sp.TNat, vault, "registerPool").open_some(
        "INTERFACE_MISMATCH")
    # # We don't need to check that tokens and assetManagers have the same length, since the Vault already performs
    # # that check.
    # # vault.registerTokens(poolId, tokens, assetManagers)
    registerTokens = sp.contract(Types.REGISTER_TOKENS_PARAMS, vault, "registerTokens").open_some(
        "INTERFACE_MISMATCH")
    registerTokensParams = sp.record(
        poolId=poolId,
        tokens=tokens,
        assetManagers=assetManagers
    )

    sp.transfer(specialization, sp.tez(0), registerPool)
    sp.transfer(registerTokensParams, sp.tez(0), registerTokens)

    return poolId
