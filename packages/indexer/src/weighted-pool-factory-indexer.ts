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
import { Pool } from './entities';

import { 
  WeightedPoolFactoryCreateParameter, 
  WeightedPoolFactoryIsPoolFromFactoryKey, 
  WeightedPoolFactoryIsPoolFromFactoryValue 
} from './weighted-pool-factory-indexer-interfaces.generated';

const ZERO_BD = '0';

export function newPoolEntity(poolId: string): Pool {
  let pool = new Pool();
  pool.id = poolId;
  pool.vaultID = '1';
  pool.tokensList = [];
  pool.totalWeight = ZERO_BD;
  pool.totalSwapVolume = ZERO_BD;
  pool.totalSwapFee = ZERO_BD;
  pool.totalLiquidity = ZERO_BD;
  pool.totalShares = ZERO_BD;
  pool.swapsCount = BigInt(0);
  pool.holdersCount = BigInt(0);

  return pool;
}

@contractFilter({ name: 'WeightedPoolFactory' })
export class WeightedPoolFactoryIndexer {
  @indexEvent('PoolCreated')
  async indexCreate(
      key: WeightedPoolFactoryIsPoolFromFactoryKey,
      parameter: WeightedPoolFactoryIsPoolFromFactoryValue,
      dbContext: DbContext,
      indexingContext: TransactionIndexingContext,
  ): Promise<void> {
      // Implement your indexing logic here or delete the method if not needed.
      const poolAddress = key
      
      const pool = newPoolEntity('poolId')
      pool.swapFee = scaleDown(swapFee, 18);
      pool.createTime = indexingContext.block.timestamp.getTime();
      pool.address = poolAddress;
      pool.factory = indexingContext.contract.address;
      pool.oracleEnabled = false;
      // pool.tx = event.transaction.hash;
      pool.swapEnabled = true;
      pool.isPaused = false;

      pool.name = '';
      pool.symbol = '';
  }
}