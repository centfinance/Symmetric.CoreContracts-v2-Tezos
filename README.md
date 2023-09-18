# Symmetric V2 Tezos Smart Contracts

This repository contains the Symmetric Protocol V2 core smart contracts for Tezos, including the `Vault` and Weighted Pools, along with their tests, configuration, and deployment information. The contracts are written in Python using [SmartPy](https://smartpy.io).

## Documentation

[Symmetric V2 Tezos Smart Contracts Documentation](https://symmetric.gitbook.io/tezos-contracts/)

## Pre-requisites

This package requires the following software to be installed on your system:

1. [Poetry](https://python-poetry.org/docs/#installation) for dependency management and packaging in Python.
2. [SmartPy CLI](https://legacy.smartpy.io/docs/introduction/project_management) for Tezos smart contract development.
3. [Taqueria](https://taqueria.io/docs/getting-started/installation/) for building, testing, and deploying the contracts.

Please make sure you have these software installed on your system before proceeding.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/centfinance/Symmetric.CoreContracts-v2-Tezos.git
cd Symmetric.CoreContracts-v2-Tezos
```

2. Install the required dependencies:

```bash
npm install
```

## Compilation

To compile the contracts:

1. For standard compilation:

```bash
npm run compile <path_to_contract_file>
```

Replace `<path_to_contract_file>` with the path to your contract, for example: `vault/ProtocolFeesCollector.py`.

1. To compile and get the output in JSON format:

```bash
npm run compile:json <path_to_contract_file>
```

Replace `<path_to_contract_file>` with the path to your contract file.

## Running Tests

1. Run the tests:

```bash
npm run test <test_path>
```

Replace `<test_path>` with the path to your test, for example: `vault/ProtocolFeesCollector`.
