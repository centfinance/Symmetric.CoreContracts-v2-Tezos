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
import { Pool, Token } from './entities';

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

export function scaleDown(num: bigint, decimals: number): string {
  return (num / BigInt(10 ** decimals)).toString()
}
@contractFilter({ name: 'WeightedPoolFactory' })
export class WeightedPoolFactoryIndexer {
  @indexEvent('PoolCreated')
  async indexCreate(
      key: WeightedPoolFactoryIsPoolFromFactoryKey,
      parameter: WeightedPoolFactoryIsPoolFromFactoryValue,
      dbContext: DbContext,
      indexingContext: BigMapUpdateIndexingContext,
  ): Promise<void> {
      // Implement your indexing logic here or delete the method if not needed.
      const poolAddress = key
      const params = indexingContext.transactionParameter?.value.convert()
      const metadata = await indexingContext.contract.abstraction.tzip12().getTokenMetadata(0)
      const token = {
        name: metadata.name,
        symbol: metadata.symbol,
      }
      const pool = newPoolEntity('poolId')
      pool.swapFee = scaleDown(params.swapFee, 18);
      pool.createTime = indexingContext.block.timestamp.getTime();
      pool.address = poolAddress;
      pool.factory = indexingContext.contract.address;
      pool.oracleEnabled = false;
      // pool.tx = event.transaction.hash;
      pool.swapEnabled = true;
      pool.isPaused = false;

      pool.name = token.name!;
      pool.symbol = token.symbol!;

      dbContext.transaction.insert(Pool, pool)

      let vault = findOrInitializeVault();
      vault.poolCount += 1;
      vault.save();
  
      let vaultSnapshot = getBalancerSnapshot(vault.id, event.block.timestamp.toI32());
      vaultSnapshot.poolCount += 1;
      vaultSnapshot.save();
  
      let poolContract = PoolContract.load(poolAddress.toHexString());
      if (poolContract == null) {
        poolContract = new PoolContract(poolAddress.toHexString());
        poolContract.pool = poolId.toHexString();
        poolContract.save();
      }
  }
}