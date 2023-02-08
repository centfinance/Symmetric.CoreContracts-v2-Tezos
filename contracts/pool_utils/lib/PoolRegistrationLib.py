import smartpy as sp


class PoolRegistrationLib:

    def registerPool(
        self,
        vault,
        specialization,
        tokens
    ):
        return self.registerPoolWithAssetManagers(self, vault, specialization, tokens)

    def registerPoolWithAssetManagers(
        self,
        vault,
        specialization,
        tokens,
        assetManagers
    ):
        # // The Vault only requires the token list to be ordered for the Two Token Pools specialization. However,
        # // to make the developer experience consistent, we are requiring this condition for all the native pools.
        # //
        # // Note that for Pools which can register and deregister tokens after deployment, this property may not hold
        # // as tokens which are added to the Pool after deployment are always added to the end of the array.
        InputHelpers.ensureArrayIsSorted(tokens)

        return self._registerPool(self, vault, specialization, tokens, assetManagers)

    def _registerPool(
        self,
        vault,
        specialization,
        tokens,
        assetManagers
    ):
        # call an onchain view on PoolRegistry to get the nonce for the next pool id
        nonce = 0
        # poolId = vault.registerPool(specialization)
        poolId = self._toPoolId(sp.self_address, specialization, nonce)
        registerPool = sp.contract(sp.TNat, vault, "registerPool").open_some(
            "INTERFACE_MISMATCH")
        sp.transfer(specialization, sp.tez(0), registerPool)
        # We don't need to check that tokens and assetManagers have the same length, since the Vault already performs
        # that check.
        # vault.registerTokens(poolId, tokens, assetManagers)
        tregister_tokens_params = sp.TRecord(
            poolId=sp.TBytes,
            tokens=sp.TList(sp.TAddress),
            assetManagers=sp.TList(sp.TAddress),
        )
        registerTokens = sp.contract(tregister_tokens_params, vault, "registerTokens").open_some(
            "INTERFACE_MISMATCH")
        registerTokensParams = sp.record(poolId, tokens, assetManagers)
        sp.transfer(registerTokensParams, sp.tez(0), registerTokens)

        return poolId

    #     function _toPoolId(
    #     address pool,
    #     PoolSpecialization specialization,
    #     uint80 nonce
    # ) internal pure returns (bytes32) {
    #     bytes32 serialized;

    #     serialized |= bytes32(uint256(nonce));
    #     serialized |= bytes32(uint256(specialization)) << (10 * 8);
    #     serialized |= bytes32(uint256(pool)) << (12 * 8);

    #     return serialized;
    # }

    def _toPoolId(pool, specialization, nonce):
        return sp.pack(sp.record(
            nonce,
            specialization,
            pool,
        ))
