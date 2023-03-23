import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

from contracts.vault.AssetTransfersHandler import AssetTransfersHandler


class ProtocolFeesCollector(sp.Contract):
    def __init__(
            self,
            vault,
    ):
        sp.Contract.__init__(self)
        self.init(
            vault=vault,
            swapFeePercentage=sp.nat(0),
            flashFeePercentage=sp.nat(0),
        )

    @sp.entry_point
    def withdrawCollectedFees(
        self,
        tokens,
        amounts,
        recipient
    ):
        sp.verify((sp.len(tokens) == sp.len(amounts)),
                  Errors.INPUT_LENGTH_MISMATCH)

        with sp.for_('i', sp.range(0, sp.len(tokens))) as i:
            token = tokens[i]
            amount = amounts[i]
            AssetTransfersHandler.TransferToken(
                self.address,
                recipient,
                amount,
                token.address,
                token.id,
                token.FA2,
            )

    @sp.onchain_view()
    def getCollectedFeeAmounts(self, tokens):
        feeAmounts = sp.compute(sp.map({}, tkey=sp.TNat, tvalue=sp.TNat))
        with sp.for_('i', sp.range(0, sp.len(tokens))) as i:
            feeAmounts[i] = sp.compute(sp.view(
                'getBalance',
                tokens[i].address,
                self.address,
                t=sp.TNat
            ).open_some('Invalid View'))
