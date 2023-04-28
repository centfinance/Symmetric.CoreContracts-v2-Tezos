// export function getPoolTokens(poolId: Bytes): Bytes[] | null {
//   let vaultContract = Vault.bind(VAULT_ADDRESS);
//   let tokensCall = vaultContract.try_getPoolTokens(poolId);

import { MichelsonMap } from "@taquito/michelson-encoder";
import { DbContext } from "@tezos-dappetizer/database";
import BigNumber from "bignumber.js";
import { Pool } from "../entities/Pool";
import { PriceRateProvider } from "../entities/PriceRateProvider";
// import { Pool, PoolToken, PriceRateProvider } from "../entities";
import { WeightedPoolFactoryCreateParameterTokensValue } from "../weighted-pool-factory-indexer-interfaces.generated";

export namespace PoolType {
  export const Weighted = 'Weighted';
  export const Stable = 'Stable';
  export const MetaStable = 'MetaStable';
  export const ComposableStable = 'ComposableStable';
  export const HighAmpComposableStable = 'HighAmpComposableStable';
}

//   if (tokensCall.reverted) {
//     log.warning('Failed to get pool tokens: {}', [poolId.toHexString()]);
//     return null;
//   }

//   let tokensValue = tokensCall.value.value0;
//   let tokens = changetype<Bytes[]>(tokensValue);

//   return tokens;
// }

export function getPoolTokenId(poolId: string, tokenAddress: string, tokenId: BigNumber): string {
  return poolId.concat('-').concat(tokenAddress).concat('-').concat(tokenId.toString());
}


export async function setPriceRateProviders(
  poolId: string, 
  rateProviders: MichelsonMap<BigNumber, string | null>, 
  tokensList: string[],
  dbContext: DbContext,
): Promise<void> {
  if (rateProviders.size != tokensList.length) return;

  for (let i: number = 0; i < rateProviders.size; i++) {
    let token = JSON.parse(tokensList[i]) as WeightedPoolFactoryCreateParameterTokensValue;
    let tokenAddress = token[0];
    let tokenId = token[1];
    let providerId = getPoolTokenId(poolId, tokenAddress, tokenId ? tokenId : BigNumber(0));
    let provider = new PriceRateProvider();
    provider.id = providerId;
    provider.poolId = poolId;
    provider.token = providerId;
    provider.address = rateProviders.get(BigNumber(i));
    await dbContext.transaction.save(PriceRateProvider, provider);
  }
}

export function isComposableStablePool(pool: Pool): boolean {
  return pool.poolType == PoolType.ComposableStable || pool.poolType == PoolType.HighAmpComposableStable;
}