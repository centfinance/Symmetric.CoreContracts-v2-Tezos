import smartpy as sp

from contracts.vault.Swaps import Swaps

from contracts.utils.mixins.Administrable import Administrable

from contracts.utils.mixins.Pausable import Pausable


def normalize_metadata(self, metadata):
    meta = {}
    for key in metadata:
        meta[key] = sp.utils.bytes_of_string(metadata[key])

    return meta


class Vault(
    sp.Contract,
    Administrable,
    Pausable,
    Swaps,
):
    def __init__(self, owner, metadata):
        self.init(
            metadata=sp.big_map(
                normalize_metadata(self, metadata))
        )
        sp.Contract.__init__(self)
        Administrable.__init__(self, owner, False)
        Pausable.__init__(self, False, False)
        Swaps.__init__(self)
