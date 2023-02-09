import smartpy as sp


class Types:
    TOKENS = sp.TList(sp.TRecord(address=sp.TAddress, id=sp.TNat))

    REGISTER_TOKENS_PARAMS = sp.TRecord(
        poolId=sp.TBytes,
        tokens=TOKENS,
        assetManagers=sp.TList(sp.TAddress),
    )


class PoolRegistrationLib:

    def registerPool(
        self,
        vault,
        specialization,
        tokens
    ):
        # Create empty list of size tokens.length as we don't need assetManagers
        assetManagers = [sp.address(
            'tz100000000000000000000000000000000000000')] * tokens.length
        return self.registerPoolWithAssetManagers(self, vault, specialization, tokens, assetManagers)

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
        # TODO: Decide if this is needed on Tezos
        # InputHelpers.ensureListIsSorted(tokens)

        return self._registerPool(self, vault, specialization, tokens, assetManagers)

    def _registerPool(
        self,
        vault,
        specialization,
        tokens,
        assetManagers
    ):
        nonce = sp.view('getNextNonce', vault, sp.unit, t=sp.TRecord(
            nonce=sp.TNat)).open_some("Invalid view")

        poolId = self._toPoolId(sp.self_address, specialization, nonce)

        registerPool = sp.contract(sp.TNat, vault, "registerPool").open_some(
            "INTERFACE_MISMATCH")
        sp.transfer(specialization, sp.tez(0), registerPool)
        # We don't need to check that tokens and assetManagers have the same length, since the Vault already performs
        # that check.
        # vault.registerTokens(poolId, tokens, assetManagers)
        registerTokens = sp.contract(Types.REGISTER_TOKENS_PARAMS, vault, "registerTokens").open_some(
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

    #
    def _toPoolId(pool, specialization, nonce):
        return sp.pack(sp.record(
            nonce,
            specialization,
            pool,
        ))
