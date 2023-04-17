import { DbContext } from '@tezos-dappetizer/database';
import {
    contractFilter,
    indexBigMapUpdate,
    indexEntrypoint,
    indexEvent,
    indexOrigination,
    indexStorageChange,
} from '@tezos-dappetizer/decorators';
import {
    BigMapUpdateIndexingContext,
    EventIndexingContext,
    OriginationIndexingContext,
    StorageChangeIndexingContext,
    TransactionIndexingContext,
} from '@tezos-dappetizer/indexer';
import { Pool, Symmetric, Token } from './entities';
import { getStorage, getTokenMetadata, newPoolEntity, scaleDown } from './helpers/misc';
import { address, nat } from './types/type-aliases';
import { Storage } from './types/weighted-pool-types';

import { 
  WeightedPoolFactoryCreateParameter, 
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
  indexingContext: EventIndexingContext, 
  dbContext: DbContext
) {
  const params = indexingContext.transactionParameter?.value.convert() as WeightedPoolFactoryCreateParameter
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

async function createWeightedLikePool(poolAddress: string, indexingContext: EventIndexingContext, dbContext: DbContext): string | null {
  const poolStorage = await getStorage(poolAddress);

  let pool = await handleNewPool(poolAddress, poolStorage.poolId, indexingContext, dbContext);
  pool.poolType = 'Weighted';
  pool.poolTypeVersion = 1;
  pool.owner = poolStorage.admin;

  // let tokens = getPoolTokens(poolId);
  // if (tokens == null) return null;
  // pool.tokensList = tokens;

  dbContext.transaction.save(Pool, pool)

  // handleNewPoolTokens(pool, tokens);

  // // Load pool with initial weights
  // updatePoolWeights(poolId.toHexString());

  // // Create PriceRateProvider entities for WeightedPoolV2
  // if (poolTypeVersion == 2) setPriceRateProviders(poolId.toHex(), poolAddress, tokens);

  return poolId.toHexString();
}