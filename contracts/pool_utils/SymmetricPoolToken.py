import smartpy as sp

import contracts.utils.tokens.FA12 as FA12


CONTRACT_METADATA = {
    "": "<ipfs://....>",
}


class SymmetricPoolToken(
        FA12.FA12_token_metadata,
        FA12.FA12_contract_metadata,
        FA12.FA12_core):
    """
    SymmetricPoolToken represents the FA1.2 token standard used to track a user's liquidity within a liquidity pool.

    This token is meant to symbolize the amount of liquidity a user has provided to the pool and can be used for 
    subsequent operations related to the pool, like withdrawals or swaps. This contract is commonly inherited 
    by BasePool contracts, allowing pools to have their own native liquidity token.
    
    Inherits:
        - FA12.FA12_token_metadata: Provides metadata functionalities for the FA1.2 token.
        - FA12.FA12_contract_metadata: Provides additional contract metadata functionalities.
        - FA12.FA12_core: Provides core FA1.2 functionalities like transfers and approvals.
    
    Attributes:
        name (str): Name of the liquidity token.
        symbol (str): Symbol representing the liquidity token.
        vault (sp.TAddress): Address of the vault managing the pool's assets.
        contract_metadata (dict): Metadata about the contract.
    
    Methods:
        getVault() -> sp.TAddress:
            Returns the address of the associated vault.
        
        is_allowed(owner: sp.TAddress, spender: sp.TAddress, value: sp.TNat) -> bool:
            Checks if a spender is allowed to spend a certain amount of tokens on behalf of an owner.
            The vault is always allowed.
        
        _mintPoolTokens(recipient: sp.TAddress, amount: sp.TNat) -> None:
            Mints (creates) a given amount of pool tokens for a specific recipient.
        
        _burnPoolTokens(sender: sp.TAddress, amount: sp.TNat) -> None:
            Burns (destroys) a given amount of pool tokens from a specific sender's balance.
    """
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
    
    # Add mint and burn functionality used by pool
    def _mintPoolTokens(self, recipient, amount):
        self._mint(sp.record(address=recipient, value=amount))

    def _burnPoolTokens(self, sender, amount):
        self._burn(sp.record(address=sender, value=amount))
