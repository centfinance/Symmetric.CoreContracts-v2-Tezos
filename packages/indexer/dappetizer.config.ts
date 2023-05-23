import * as dotenv from "dotenv"; // see https://github.com/motdotla/dotenv#how-do-i-use-dotenv-with-import
dotenv.config();
import { DappetizerConfigUsingDb } from "@tezos-dappetizer/database";

export const config: DappetizerConfigUsingDb = {
  modules: [
    {
      id: "./src/index.ts", // This project is the indexer module itself.
    },
  ],
  networks: {
    mainnet: {
      indexing: {
        fromBlockLevel: Number(process.env.FROM_LEVEL),
        contracts: [
          {
            name: "WeightedPoolFactory",
            addresses: [process.env.WEIGHTED_FACTORY_ADDRESS!],
          },
          {
            name: "Vault",
            addresses: [process.env.VAULT_ADDRESS!],
          },
        ],
        contractBoost: {
          type: "tzkt",
          apiUrl: process.env.TZKT_API,
        },
      },
      tezosNode: {
        url: process.env.TEZOS_NODE!,
      },
    },
  },
  database: {
    // type: 'sqlite',
    // database: 'database.sqlite',

    // If you want to use PostgreSQL:
    type: "postgres",
    host: process.env.POSTGRES_HOST,
    port: Number(process.env.POSTGRES_PORT),
    username: process.env.POSTGRES_USERNAME,
    password: process.env.POSTGRES_PASSWORD,
    database: "postgres",
    schema: "indexer",
  },
  // hasura: {
  //   url: "http://localhost:8080/",
  //   autotrackEntities: true,
  //   dropExistingTracking: true,
  // },
  usageStatistics: {
    enabled: true,
  },
};

export default config;
