import smartpy as sp

from contracts.vault.Swaps import Swaps


def normalize_metadata(self, metadata):
    meta = {}
    for key in metadata:
        meta[key] = sp.utils.bytes_of_string(metadata[key])

    return meta


class Vault(
    sp.Contract,
    Swaps
):
    def __init__(self, metadata):
        self.init(
            metadata=sp.big_map(
                normalize_metadata(self, metadata))
        )
        sp.Contract.__init__(self)
        Swaps.__init__(self)
