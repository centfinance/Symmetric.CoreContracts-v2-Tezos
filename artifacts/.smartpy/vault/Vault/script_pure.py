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
    """
    The `Vault` is Symmetric V2's core contract. A single instance of it exists for the entire network, and it is the
    entity used to interact with Pools by Liquidity Providers who join and exit them, Traders who swap, and Asset
    Managers who withdraw and deposit tokens.
  
    The `Vault`'s source code is split among a number of sub-contracts, with the goal of improving readability and making
    understanding the system easier. Most sub-contracts have been marked as `abstract` to explicitly indicate that only
    the full `Vault` is meant to be deployed.
  
    Roughly speaking, these are the contents of each sub-contract:
    - `PoolBalances`: Pool joins and exits.
    - `PoolRegistry`: Pool registration, ID management, and basic queries.
    - `PoolTokens`: Pool token registration and registration, and balance queries.
    - `Swaps`: Pool swaps.
    - `Administrable`: Access control
    - `Pausable: Pause Entrypoints
    """
    def __init__(
            self,
            owner=sp.address('tz1UGWQQ5YFkZqWgE3gqmPyuwy2R5VGpMM9B'),
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
