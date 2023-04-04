import { IndexerModuleUsingDb } from '@tezos-dappetizer/database';
import { createContractIndexerFromDecorators } from '@tezos-dappetizer/decorators';

import { VaultIndexer } from './vault-indexer';

export const indexerModule: IndexerModuleUsingDb = {
    name: 'Indexer',
    dbEntities: [
        // Register your DB entity classes to TypeORM here:
        // MyDbEntity,
    ],
    contractIndexers: [
        // Create your contract indexers here:
        createContractIndexerFromDecorators(new VaultIndexer()),
    ],
    blockDataIndexers: [
        // Create your block data indexers here:
        // new MyBlockDataIndexer(),
    ],
    // Create your indexing cycle handler here:
    // indexingCycleHandler: new MyIndexingCycleHandler(),
};
