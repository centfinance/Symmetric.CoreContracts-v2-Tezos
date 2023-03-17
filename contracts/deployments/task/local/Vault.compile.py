import smartpy as sp

from contracts.vault.Vault import Vault

metadata = {
    'name': 'Symmetric Vault Contract',
    'description': '',

}

sp.add_compilation_target('local', Vault())
