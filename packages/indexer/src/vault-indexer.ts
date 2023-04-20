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
import { JoinExit } from './entities';

import {
    VaultAcceptAdminParameter,
    VaultBatchSwapParameter,
    VaultChangedStorage,
    VaultExitPoolParameter,
    VaultInitialStorage,
    VaultIsPoolRegisteredKey,
    VaultIsPoolRegisteredValue,
    VaultJoinPoolParameter,
    VaultMetadataKey,
    VaultMetadataValue,
    VaultPoolBalanceChangedPayload,
    VaultPoolRegisteredPayload,
    VaultPoolsBalancesKey,
    VaultPoolsBalancesValue,
    VaultPoolsTokensKey,
    VaultPoolsTokensValue,
    VaultRegisterPoolParameter,
    VaultRegisterTokensParameter,
    VaultSetPausedParameter,
    VaultSwapParameter,
    VaultSwapPayload,
    VaultTokensRegisteredPayload,
    VaultTransferAdminParameter,
} from './vault-indexer-interfaces.generated';

@contractFilter({ name: 'Vault' })
export class VaultIndexer {
    @indexOrigination()
    async indexOrigination(
        initialStorage: VaultInitialStorage,
        dbContext: DbContext,
        indexingContext: OriginationIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexEntrypoint('accept_admin')
    async indexAcceptAdmin(
        parameter: VaultAcceptAdminParameter,
        dbContext: DbContext,
        indexingContext: TransactionIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexEntrypoint('batchSwap')
    async indexBatchSwap(
        parameter: VaultBatchSwapParameter,
        dbContext: DbContext,
        indexingContext: TransactionIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexEntrypoint('exitPool')
    async indexExitPool(
        parameter: VaultExitPoolParameter,
        dbContext: DbContext,
        indexingContext: TransactionIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexEntrypoint('joinPool')
    async indexJoinPool(
      parameter: VaultJoinPoolParameter,
      dbContext: DbContext,
      indexingContext: TransactionIndexingContext,
    ): Promise<void> {
      // const poolId: string = parameter.poolId;
      // const amounts = parameter.request.assets.map((_, key) => parameter.request.limits.get(key));
      // const blockTimestamp = indexingContext.timestamp.toI32();
      // const logIndex = indexingContext.logIndex;
      // const transactionHash = indexingContext.transaction.hash;
  
      // const pool = await dbContext.poolRepository.findOne(poolId);
      // if (pool === undefined) {
      //   console.warn('Pool not found in indexJoinPool: {} {}', [poolId, transactionHash.toHexString()]);
      //   return;
      // }
  
      // const tokenAddresses = pool.tokensList;
  
      // const joinId = transactionHash.toHexString().concat(logIndex.toString());

      // const joinAmounts: string[] = [];
      // let valueUSD = '0';
  
      // for (let i = 0; i < tokenAddresses.length; i++) {
      //   const tokenAddress = tokenAddresses[i];
      //   const poolToken = await dbContext.poolTokenRepository.findOne({ pool: pool, token: tokenAddress });
      //   if (poolToken === undefined) {
      //     throw new Error('poolToken not found');
      //   }
  
      //   // You'll need to implement the scaleDown function
      //   const joinAmount = scaleDown(amounts[i], poolToken.decimals);
      //   joinAmounts[i] = joinAmount.toString();
      //   const tokenJoinAmountInUSD = valueInUSD(joinAmount, tokenAddress); // You'll need to implement the valueInUSD function
      //   valueUSD = (parseFloat(valueUSD) + parseFloat(tokenJoinAmountInUSD)).toString();
      // }
      // const join = {
      //   id: joinId,
      //   sender: parameter.sender,
      //   type: 'Join',
      //   amounts: joinAmounts,
      //   pool: pool,
      //   user: await dbContext.userRepository.findOne(parameter.sender) ?? new User(parameter.sender), // Assuming that User has a constructor taking the user address as the only argument
      //   timestamp: blockTimestamp,
      //   tx: transactionHash,
      //   valueUSD: valueUSD,
      // }


      // await dbContext.transaction.insert(JoinExit, join);
  
      // The rest of the function depends on functions and data structures that are specific to the Balancer v2 subgraph
      // You may need to adjust or implement these functions and data structures accordingly
      // Also, note that some of the entity updates should be adjusted to work with your dbContext and TypeORM
  
      // ...
  
    }

    @indexEntrypoint('registerPool')
    async indexRegisterPool(
        parameter: VaultRegisterPoolParameter,
        dbContext: DbContext,
        indexingContext: TransactionIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
        
    }

    @indexEntrypoint('registerTokens')
    async indexRegisterTokens(
        parameter: VaultRegisterTokensParameter,
        dbContext: DbContext,
        indexingContext: TransactionIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexEntrypoint('set_paused')
    async indexSetPaused(
        parameter: VaultSetPausedParameter,
        dbContext: DbContext,
        indexingContext: TransactionIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexEntrypoint('swap')
    async indexSwap(
        parameter: VaultSwapParameter,
        dbContext: DbContext,
        indexingContext: TransactionIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexEntrypoint('transfer_admin')
    async indexTransferAdmin(
        parameter: VaultTransferAdminParameter,
        dbContext: DbContext,
        indexingContext: TransactionIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexStorageChange()
    async indexStorageChange(
        newStorage: VaultChangedStorage,
        dbContext: DbContext,
        indexingContext: StorageChangeIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexBigMapUpdate({ path: ['isPoolRegistered'] })
    async indexIsPoolRegisteredUpdate(
        key: VaultIsPoolRegisteredKey,
        value: VaultIsPoolRegisteredValue | undefined, // Undefined represents a removal.
        dbContext: DbContext,
        indexingContext: BigMapUpdateIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexBigMapUpdate({ path: ['metadata'] })
    async indexMetadataUpdate(
        key: VaultMetadataKey,
        value: VaultMetadataValue | undefined, // Undefined represents a removal.
        dbContext: DbContext,
        indexingContext: BigMapUpdateIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexBigMapUpdate({ path: ['poolsBalances'] })
    async indexPoolsBalancesUpdate(
        key: VaultPoolsBalancesKey,
        value: VaultPoolsBalancesValue | undefined, // Undefined represents a removal.
        dbContext: DbContext,
        indexingContext: BigMapUpdateIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexBigMapUpdate({ path: ['poolsTokens'] })
    async indexPoolsTokensUpdate(
        key: VaultPoolsTokensKey,
        value: VaultPoolsTokensValue | undefined, // Undefined represents a removal.
        dbContext: DbContext,
        indexingContext: BigMapUpdateIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }


    @indexEvent('PoolBalanceChanged')
    async indexPoolBalanceChangedEvent(
        payload: VaultPoolBalanceChangedPayload,
        dbContext: DbContext,
        indexingContext: EventIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.

    }

    @indexEvent('PoolRegistered')
    async indexPoolRegisteredEvent(
        payload: VaultPoolRegisteredPayload,
        dbContext: DbContext,
        indexingContext: EventIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexEvent('Swap')
    async indexSwapEvent(
        payload: VaultSwapPayload,
        dbContext: DbContext,
        indexingContext: EventIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexEvent('TokensRegistered')
    async indexTokensRegisteredEvent(
        payload: VaultTokensRegisteredPayload,
        dbContext: DbContext,
        indexingContext: EventIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }
}
