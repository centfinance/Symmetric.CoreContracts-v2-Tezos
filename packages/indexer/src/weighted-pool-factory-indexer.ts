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
import { WeightedPoolFactoryCreateParameter } from './weighted-pool-factory-indexer-interfaces.generated';


@contractFilter({ name: 'WeightedPoolFactory' })
export class WeightedPoolFactoryIndexer {
  @indexEntrypoint('accept_admin')
  async indexCreate(
      parameter: WeightedPoolFactoryCreateParameter,
      dbContext: DbContext,
      indexingContext: TransactionIndexingContext,
  ): Promise<void> {
      // Implement your indexing logic here or delete the method if not needed.
  }
}