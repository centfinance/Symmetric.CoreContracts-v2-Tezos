import smartpy as sp


class Types:
    TOKENS = sp.TMap(sp.TNat, sp.TRecord(address=sp.TAddress, id=sp.TNat))

    REGISTER_TOKENS_PARAMS = sp.TRecord(
        poolId=sp.TBytes,
        tokens=TOKENS,
        assetManagers=sp.TList(sp.TAddress),
    )


# def preparePool(vault, specialization, tokens):
#     # Create empty list of size tokens.length as we don't need assetManagers
#     assetManagers = [sp.address(
#         'tz100000000000000000000000000000000000000')] * tokens.length
#     return (registerPool(sp.record(vault=vault, specialization=specialization,
#                                          tokens=tokens, assetManagers=assetManagers)))


def registerPool(vault, specialization, tokens, assetManagers):
    def _toPoolId(pool, specialization, nonce):
        return sp.pack(sp.record(
            nonce=nonce,
            specialization=specialization,
            pool=pool,
        ))
    nonce = sp.view('getNextNonce', vault, sp.unit,
                    t=sp.TNat).open_some("Invalid view")

    poolId = _toPoolId(sp.self_address, specialization, nonce)

    registerPool = sp.contract(sp.TNat, vault, "registerPool").open_some(
        "INTERFACE_MISMATCH")
    sp.transfer(specialization, sp.tez(0), registerPool)
    # # We don't need to check that tokens and assetManagers have the same length, since the Vault already performs
    # # that check.
    # # vault.registerTokens(poolId, tokens, assetManagers)
    registerTokens = sp.contract(Types.REGISTER_TOKENS_PARAMS, vault, "registerTokens").open_some(
        "INTERFACE_MISMATCH")
    registerTokensParams = sp.record(
        poolId=poolId, tokens=tokens, assetManagers=assetManagers)
    sp.transfer(registerTokensParams, sp.tez(0), registerTokens)

    return poolId
