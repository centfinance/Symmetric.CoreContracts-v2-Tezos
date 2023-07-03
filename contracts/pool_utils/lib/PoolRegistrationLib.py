import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

class Types:
    TOKEN = sp.TPair(sp.TAddress, sp.TOption(sp.TNat))

    TOKENS = sp.TMap(sp.TNat, TOKEN)

    REGISTER_TOKENS_PARAMS = sp.TRecord(
        poolId=sp.TPair(sp.TAddress, sp.TNat),
        tokens=TOKENS,
        assetManagers=sp.TOption(sp.TMap(sp.TNat, sp.TAddress)),
    )


def registerPool(vault, tokens, assetManagers):
    nonce = sp.compute(sp.view('getNextPoolNonce', vault, sp.unit,
                               t=sp.TNat).open_some(Errors.GET_NEXT_POOL_NONCE_INVALID))

    poolId = (sp.self_address, nonce)

    registerPool = sp.contract(sp.TUnit, vault, "registerPool").open_some(
        "registerPoolFail")

    registerTokens = sp.contract(Types.REGISTER_TOKENS_PARAMS, vault, "registerTokens").open_some(
        "registerTokensFail")
    registerTokensParams = sp.record(
        poolId=poolId,
        tokens=tokens,
        assetManagers=assetManagers
    )

    sp.transfer(sp.unit, sp.tez(0), registerPool)
    sp.transfer(registerTokensParams, sp.tez(0), registerTokens)

    return poolId
