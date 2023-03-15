import smartpy as sp

from contracts.vault.Swaps import Swaps


class Vault(
    sp.Contract,
    Swaps
):
    def __init__(self):
        sp.Contract.__init__(self)
        Swaps.__init__(self)
