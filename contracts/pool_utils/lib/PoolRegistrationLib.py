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
    """
    Helper function to register a new pool with the Vault contract.
    
    This function first fetches the next available nonce for the new pool, 
    constructs the pool ID using the nonce and the address of the current contract 
    (pool), and then registers the pool and its associated tokens with the Vault.
    
    Args:
        vault (sp.TAddress): The address of the Vault contract.
        tokens (Types.TOKENS): A map of tokens that will be associated with the pool.
        assetManagers (sp.TOption(sp.TMap)): Optional map of asset managers for each token. 
                                             If not provided, the Vault will assume the pool 
                                             itself will be the asset manager.

    Returns:
        sp.TPair(sp.TAddress, sp.TNat): The pool ID, consisting of the current contract's 
                                        address and the fetched nonce.
        
    Raises:
        Errors.GET_NEXT_POOL_NONCE_INVALID: If there's an error fetching the next nonce 
                                            from the Vault.
        "registerPoolFail": If there's an error invoking the `registerPool` entry point 
                            on the Vault.
        "registerTokensFail": If there's an error invoking the `registerTokens` entry 
                              point on the Vault.
    """
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
