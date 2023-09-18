import smartpy as sp

from contracts.vault.Swaps import Swaps

from contracts.utils.mixins.Administrable import Administrable

from contracts.utils.mixins.Pausable import Pausable

CONTRACT_METADATA = {
    "": "https://raw.githubusercontent.com/centfinance/Symmetric.CoreContracts-v2-Tezos/main/metadata/testnet/Vault.json",
}


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
    def __init__(
            self,
            owner=sp.address('tz1aSkwEot3L2kmUvcoxzjMomb9mvBNuzFK6'),
            metadata=CONTRACT_METADATA,
    ):
        self.init(
            metadata=sp.big_map(
                normalize_metadata(self, metadata))
        )
        sp.Contract.__init__(self)
        Administrable.__init__(self, owner, False)
        Pausable.__init__(self, False, False)
        Swaps.__init__(self)


sp.add_compilation_target('Vault', Vault())