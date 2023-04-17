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
import { newPoolEntity, scaleDown } from './helpers/misc';

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
      const poolAddress = key
      const params = indexingContext.transactionParameter?.value.convert() as WeightedPoolFactoryCreateParameter

      const pool = newPoolEntity('poolId')
      pool.swapFee = scaleDown(params.swapFeePercentage, 18);
      pool.createTime = indexingContext.block.timestamp.getTime();
      pool.address = poolAddress;
      pool.factory = indexingContext.contract.address;
      pool.oracleEnabled = false;
      // pool.tx = event.transaction.hash;
      pool.swapEnabled = true;
      pool.isPaused = false;

      pool.name = token.name!;
      pool.symbol = token.symbol!;

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
  }
}

// function createWeightedLikePool(poolAddress: string, poolType: string, poolTypeVersion: number = 1): string | null {
//   let poolContract = WeightedPool.bind(poolAddress);

//   let poolIdCall = poolContract.try_getPoolId();
//   let poolId = poolIdCall.value;

//   let swapFeeCall = poolContract.try_getSwapFeePercentage();
//   let swapFee = swapFeeCall.value;

//   let ownerCall = poolContract.try_getOwner();
//   let owner = ownerCall.value;

//   let pool = handleNewPool(poolAddress, poolId, swapFee);
//   pool.poolType = poolType;
//   pool.poolTypeVersion = poolTypeVersion;
//   pool.owner = owner;

//   // let tokens = getPoolTokens(poolId);
//   // if (tokens == null) return null;
//   // pool.tokensList = tokens;

//   pool.save();

//   // handleNewPoolTokens(pool, tokens);

//   // // Load pool with initial weights
//   // updatePoolWeights(poolId.toHexString());

//   // // Create PriceRateProvider entities for WeightedPoolV2
//   // if (poolTypeVersion == 2) setPriceRateProviders(poolId.toHex(), poolAddress, tokens);

//   return poolId.toHexString();
// }