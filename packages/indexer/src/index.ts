import { IndexerModuleUsingDb } from "@tezos-dappetizer/database";
import { createContractIndexerFromDecorators } from "@tezos-dappetizer/decorators";

import { WeightedPoolFactoryIndexer } from "./weighted-pool-factory-indexer";
import { VaultIndexer } from "./vault-indexer";

import { Pool } from "./entities/Pool";
import { PoolToken } from "./entities/PoolToken";
import { Token } from "./entities/Token";
import { Symmetric } from "./entities/Symmetric";
import { PriceRateProvider } from "./entities/PriceRateProvider";
import { TradePairSnapshot } from "./entities/TradePairSnapshot";
import { TradePair } from "./entities/TradePair";
import { TokenSnapshot } from "./entities/TokenSnapshot";
import { SymmetricSnapshot } from "./entities/SymmetricSnapshot";
import { PoolSnapshot } from "./entities/PoolSnapshot";
import { JoinExit } from "./entities/JoinExit";
import { User } from "./entities/User";
import { PoolHistoricalLiquidity } from "./entities/PoolHistoricalLiquidity";
import { TokenPrice } from "./entities/TokenPrice";
import { LatestPrice } from "./entities/LatestPrice";
import { Swap } from "./entities/Swap";

export const indexerModule: IndexerModuleUsingDb = {
  name: "Indexer",
  dbEntities: [
    // Register your DB entity classes to TypeORM here:
    // MyDbEntity,
    LatestPrice,
    Pool,
    PoolSnapshot,
    PoolToken,
    Token,
    Symmetric,
    PriceRateProvider,
    PoolHistoricalLiquidity,
    Swap,
    SymmetricSnapshot,
    TokenSnapshot,
    TradePair,
    TradePairSnapshot,
    TokenPrice,
    JoinExit,
    User,
    // PriceRateProvider,
  ],
  contractIndexers: [
    // Create your contract indexers here:
    createContractIndexerFromDecorators(new WeightedPoolFactoryIndexer()),
    createContractIndexerFromDecorators(new VaultIndexer()),
  ],
};
