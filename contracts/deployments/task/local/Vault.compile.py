import smartpy as sp

from contracts.vault.Vault import Vault

sp.add_compilation_target('local', Vault())
