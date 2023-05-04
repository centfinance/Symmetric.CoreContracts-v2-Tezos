import { IndexerModuleUsingDb } from '@tezos-dappetizer/database';
import { createContractIndexerFromDecorators } from '@tezos-dappetizer/decorators';

import { WeightedPoolFactoryIndexer } from './weighted-pool-factory-indexer';

import { Pool } from './entities/Pool'
import { PoolToken } from './entities/PoolToken';
import { Token } from './entities/Token';
import { Symmetric } from './entities/Symmetric';
import { PriceRateProvider } from './entities/PriceRateProvider';
import { TradePairSnapshot } from './entities/TradePairSnapshot';
import { TradePair } from './entities/TradePair';
import { TokenSnapshot } from './entities/TokenSnapshot';
import { SymmetricSnapshot } from './entities/SymmetricSnapshot';
import { PoolSnapshot } from './entities/PoolSnapshot';
import { JoinExit } from './entities/JoinExit';
import { User } from './entities/User';
import { PoolHistoricalLiquidity } from './entities/PoolHistoricalLiquidity';

export const indexerModule: IndexerModuleUsingDb = {
    name: 'Indexer',
    dbEntities: [
        // Register your DB entity classes to TypeORM here:
        // MyDbEntity,
        Pool,
        PoolSnapshot,
        PoolToken,
        Token, 
        Symmetric,
        PriceRateProvider,
        PoolHistoricalLiquidity,
        SymmetricSnapshot, 
        TokenSnapshot, 
        TradePair, 
        TradePairSnapshot,
        JoinExit,
        User,
        // PriceRateProvider,

    ],
    contractIndexers: [
        // Create your contract indexers here:
        createContractIndexerFromDecorators(new WeightedPoolFactoryIndexer()),
    ],
};
