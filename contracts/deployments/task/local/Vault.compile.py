import smartpy as sp

from contracts.vault.Vault import Vault

metadata = {
    'name': 'Symmetric Vault',
    'version': 'v1.0.0',
    'description': 'The Vault is the core of Symmetric; it is a smart contract that holds and manages all tokens in each Symmetric pool. It is also the portal through which most Symmetric operations (swaps / joins / exits) take place.',
    'authors': ['Cent Finance'],
    'homepage': 'https://symmetric.exchange',
    'license': 'GPL-3.0',
    'interfaces': ['TZIP-016']
}

CONTRACT_METADATA = {
    "": "https://raw.githubusercontent.com/centfinance/Symmetric.CoreContracts-v2-Tezos/main/metadata/testnet/Vault.json",
}

sp.add_compilation_target('local', Vault(CONTRACT_METADATA))
