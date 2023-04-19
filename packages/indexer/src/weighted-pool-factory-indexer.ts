import { MichelsonMap } from '@taquito/michelson-encoder';
import { DbContext } from '@tezos-dappetizer/database';
import {
    contractFilter,
    indexEvent,
} from '@tezos-dappetizer/decorators';
import {
    EventIndexingContext,
} from '@tezos-dappetizer/indexer';
import BigNumber from 'bignumber.js';
import { Pool, Symmetric, Token } from './entities';
import { createPoolTokenEntity, getStorage, getTokenMetadata, newPoolEntity, scaleDown } from './helpers/misc';
import { setPriceRateProviders } from './helpers/pools';
import { address, nat } from './types/type-aliases';

import { 
  WeightedPoolFactoryCreateParameter, 
  WeightedPoolFactoryCreateParameterTokensValue, 
  WeightedPoolFactoryIsPoolFromFactoryKey, 
  WeightedPoolFactoryIsPoolFromFactoryValue 
} from './weighted-pool-factory-indexer-interfaces.generated';






@contractFilter({ name: 'WeightedPoolFactory' })
export class WeightedPoolFactoryIndexer {
  @indexEvent('PoolCreated')
  async indexCreate(
      key: WeightedPoolFactoryIsPoolFromFactoryKey,
      parameter: WeightedPoolFactoryIsPoolFromFactoryValue,
      dbContext: DbContext,
      indexingContext: EventIndexingContext,
  ): Promise<void> {
      // Implement your indexing logic here or delete the method if not needed.
      createWeightedLikePool(key, indexingContext, dbContext);

  }
}

async function handleNewPool(
  poolAddress: string, 
  poolId: {
    0: address;
    1: nat;
  }| undefined,
  params: WeightedPoolFactoryCreateParameter,
  indexingContext: EventIndexingContext, 
  dbContext: DbContext
) {
  const pool = newPoolEntity(JSON.stringify(poolId))
  pool.swapFee = scaleDown(params.swapFeePercentage, 18);
  pool.createTime = indexingContext.block.timestamp.getTime();
  pool.address = poolAddress;
  pool.factory = indexingContext.contract.address;
  pool.oracleEnabled = false;
  // pool.tx = event.transaction.hash;
  pool.swapEnabled = true;
  pool.isPaused = false;

  const metadata = await getTokenMetadata(poolAddress, 0)
  pool.name = metadata.name!;
  pool.symbol = metadata.symbol!;

  dbContext.transaction.save(Pool, pool)
  
  const vault = await dbContext.transaction.findOneOrFail(Symmetric, {
    where: {
      id: '1',
    }
  })

  vault.poolCount += 1;
  dbContext.transaction.save(Symmetric, vault)

  // let vaultSnapshot = getBalancerSnapshot(vault.id, event.block.timestamp.toI32());
  // vaultSnapshot.poolCount += 1;
  // vaultSnapshot.save();

  // let poolContract = PoolContract.load(poolAddress.toHexString());
  // if (poolContract == null) {
  //   poolContract = new PoolContract(poolAddress.toHexString());
  //   poolContract.pool = poolId.toHexString();
  //   poolContract.save();
  // }
  return pool;
}

async function createWeightedLikePool(poolAddress: string, indexingContext: EventIndexingContext, dbContext: DbContext): Promise<void> {
  const params = indexingContext.transactionParameter?.value.convert() as WeightedPoolFactoryCreateParameter
  const poolStorage = await getStorage(poolAddress);

  let pool = await handleNewPool(poolAddress, poolStorage.poolId, params, indexingContext, dbContext);
  pool.poolType = 'Weighted';
  pool.poolTypeVersion = 1;
  pool.owner = poolStorage.admin;
  params.tokens
  pool.tokensList = [...params.tokens.values()].map(t => JSON.stringify(t));
  pool.totalWeight = '100';

  dbContext.transaction.save(Pool, pool)

  handleNewPoolTokens(pool, params.tokens, dbContext);

  setPriceRateProviders(JSON.stringify(poolStorage.poolId),  params.rateProviders!, pool.tokensList, dbContext);
}

async function handleNewPoolTokens(pool: Pool, tokens: MichelsonMap<BigNumber, WeightedPoolFactoryCreateParameterTokensValue>, dbContext:DbContext): void {
  for (let i: number = 0; i < tokens.size; i++) {
    const tokenData = tokens.get(BigNumber(i))!;
    
    await createPoolTokenEntity(pool, tokenData?.[0], tokenData?.[1]?.toNumber(), i, dbContext);
  }
}
