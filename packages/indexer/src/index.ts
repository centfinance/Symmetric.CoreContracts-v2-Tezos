import { IndexerModuleUsingDb } from '@tezos-dappetizer/database';
import { createContractIndexerFromDecorators } from '@tezos-dappetizer/decorators';

import { WeightedPoolFactoryIndexer } from './weighted-pool-factory-indexer';

import { Pool } from './entities/Pool'
import { PoolToken } from './entities/PoolToken';
import { Token } from './entities/Token';
import { Symmetric } from './entities/Symmetric';
import { PriceRateProvider } from './entities/PriceRateProvider';

export const indexerModule: IndexerModuleUsingDb = {
    name: 'Indexer',
    dbEntities: [
        // Register your DB entity classes to TypeORM here:
        // MyDbEntity,
        Pool,
        // PoolSnapshot,
        // Token,  
        PoolToken,
        Token, 
        Symmetric,
        PriceRateProvider,
        // SymmetricSnapshot, 
        // TokenSnapshot, 
        // TradePair, 
        // TradePairSnapshot,
        // PriceRateProvider,

    ],
    contractIndexers: [
        // Create your contract indexers here:
        createContractIndexerFromDecorators(new WeightedPoolFactoryIndexer()),
    ],
    blockDataIndexers: [
        // Create your block data indexers here:
        // new MyBlockDataIndexer(),
    ],
    // Create your indexing cycle handler here:
    // indexingCycleHandler: new MyIndexingCycleHandler(),
};
