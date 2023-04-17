// export function getPoolTokens(poolId: Bytes): Bytes[] | null {
//   let vaultContract = Vault.bind(VAULT_ADDRESS);
//   let tokensCall = vaultContract.try_getPoolTokens(poolId);

//   if (tokensCall.reverted) {
//     log.warning('Failed to get pool tokens: {}', [poolId.toHexString()]);
//     return null;
//   }

//   let tokensValue = tokensCall.value.value0;
//   let tokens = changetype<Bytes[]>(tokensValue);

//   return tokens;
// }
