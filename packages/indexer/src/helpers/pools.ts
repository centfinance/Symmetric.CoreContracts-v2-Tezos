// export function getPoolTokens(poolId: Bytes): Bytes[] | null {
//   let vaultContract = Vault.bind(VAULT_ADDRESS);
//   let tokensCall = vaultContract.try_getPoolTokens(poolId);

import { MichelsonMap } from "@taquito/michelson-encoder";
import { DbContext } from "@tezos-dappetizer/database";
import BigNumber from "bignumber.js";
import { Pool, PoolToken, PriceRateProvider } from "../entities";

//   if (tokensCall.reverted) {
//     log.warning('Failed to get pool tokens: {}', [poolId.toHexString()]);
//     return null;
//   }

//   let tokensValue = tokensCall.value.value0;
//   let tokens = changetype<Bytes[]>(tokensValue);

//   return tokens;
// }

export function getPoolTokenId(poolId: string, tokenAddress: string): string {
  return poolId.concat('-').concat(tokenAddress);
}


export async function setPriceRateProviders(
  poolId: string, 
  rateProviders: MichelsonMap<BigNumber, string | null>, 
  tokensList: string[],
  dbContext: DbContext,
): Promise<void> {
  if (rateProviders.size != tokensList.length) return;

  for (let i: number = 0; i < rateProviders.size; i++) {
    let tokenAddress = tokensList[i];
    let providerId = getPoolTokenId(poolId, tokenAddress);
    let provider = new PriceRateProvider();
    provider.id = providerId;
    provider.poolId = poolId;
    provider.token = providerId;
    provider.address = rateProviders.get(BigNumber(i));
    await dbContext.transaction.save(PriceRateProvider, provider);
  }
}