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
        // Implement your indexing logic here or delete the method if not needed.

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
