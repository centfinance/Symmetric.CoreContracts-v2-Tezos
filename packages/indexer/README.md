# Symmetric Indexer for Tezos

## Overview

The Symmetric Indexer is a key component of the Symmetric decentralized exchange (DEX) on the Tezos blockchain. The indexer is responsible for tracking and storing event data from the DEX's smart contracts. This ensures transparency and traceability of the DEX operations.

The system has been developed using TypeScript and Dappetizer and stores indexed data in a PostgreSQL database. The data can be queried using a Hasura GraphQL API.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Node.js
- PostgreSQL
- Hasura GraphQL Engine

### Installation

1. Clone the repo:
```
git clone https://github.com/centfinance/Symmetric.CoreContracts-v2-Tezos.git
```

2. Navigate to the Indexer package:
```
cd /packages/indexer

2. Install NPM packages:
```
npm install
```

3. Create a `.env` file in the root directory and fill it with your environment variables. Use env.example as a template

4. Run the indexer:
```
npm run start
```

## Usage

To use the indexer, deploy your smart contracts to the Tezos blockchain and ensure the indexer is running. The indexer will automatically track and store event data from the smart contracts.

You can then query the indexed data using the Hasura GraphQL API. Navigate to the API explorer at `http://<your-api-url>/console/api/api-explorer` to write and run queries.

You can also inspect the database schema and try example queries for each table by navigating to `http://<your-api-url>/console/data/default/schema/indexer`.


## Contributing

If you would like to contribute to the Symmetric Indexer, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.
