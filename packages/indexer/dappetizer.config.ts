import { DappetizerConfigUsingDb } from '@tezos-dappetizer/database';
import { loadDappetizerNetworkConfigs } from '@tezos-dappetizer/indexer';

const network = require('../../.taq/config.local.development.json');

const config: DappetizerConfigUsingDb = {
    modules: [{
        id: './src/index.ts', // This project is the indexer module itself.
    }],
    networks: {
      mainnet: {
        "indexing": {
          "fromBlockLevel": 129929,
          "contracts": [
            {
              "name": "WeightedPoolFactory",
              "addresses": [
                network.contracts.WeightedPoolFactory.address,
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
