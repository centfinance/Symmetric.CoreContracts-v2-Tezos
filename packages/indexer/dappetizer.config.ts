import { DappetizerConfigUsingDb } from '@tezos-dappetizer/database';
import { loadDappetizerNetworkConfigs } from '@tezos-dappetizer/indexer';

const config: DappetizerConfigUsingDb = {
    modules: [{
        id: './src/index.ts', // This project is the indexer module itself.
    }],
    networks: {
      mainnet: {
        "indexing": {
          "fromBlockLevel": 127988,
          "contracts": [
            {
              "name": "WeightedPoolFactory",
              "addresses": [
                "KT19oE9Va1mU57gipENohDzHPcTj5MbKrhdb"
              ]
            }
          ]
        },
        "tezosNode": {
          "url": "http://localhost:20000"
        }
      },
    }, 
    database: {
        // type: 'sqlite',
        // database: 'database.sqlite',

        // If you want to use PostgreSQL:
        type: 'postgres',
        host: 'localhost',
        port: 5432,
        username: 'tzkt',
        password: 'local',
        database: 'postgres',
        schema: 'indexer',
    },
    usageStatistics: {
        enabled: true,
    },
};

export default config;
