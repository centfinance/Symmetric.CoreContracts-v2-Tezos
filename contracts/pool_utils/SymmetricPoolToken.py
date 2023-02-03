import smartpy as sp

import contracts.utils.tokens.FA12 as FA12


CONTRACT_METADATA = {
    "": "<ipfs://....>",
}


class SymmetricPoolToken(
        FA12.FA12_token_metadata,
        FA12.FA12_contract_metadata,
        FA12.FA12_core):
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

    @sp.onchain_view()
    def getVault(self):
        sp.result(self.data.vault)

    def is_allowed(self, owner, spender, value):
        result = sp.local("result", False)
        with sp.if_(sp.sender == self.data.vault):
            result.value = True
        with sp.else_():
            result.value = self.data.balances[owner].approvals.get(
                spender, 0) >= value

        return result.value

    def _mintPoolTokens(self, recipient, amount):
        self._mint(self, sp.record(address=recipient, value=amount))

    def _burnPoolTokens(self, sender, amount):
        self._burn(self, sp.record(address=sender, value=amount))
