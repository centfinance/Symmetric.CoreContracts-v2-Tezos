import smartpy as sp

import contracts.utils.tokens.FA12 as FA12


CONTRACT_METADATA = {
    "": "<ipfs://....>",
}


class SymmetricPoolToken(FA12.FA12_core):
    def __init__(
        self,
        name,
        symbol,
        vault,
        contract_metadata=CONTRACT_METADATA,
    ):
        FA12.FA12_core.__init__(self)
        self.update_initial_storage(
            vault=vault
        )

        token_metadata = {
            "name": name,
            "symbol": symbol,
            "decimals": "18",
            "thumbnailUri": "ipfs://......",
        }
        self.set_token_metadata(token_metadata)
        self.set_contract_metadata(contract_metadata)
