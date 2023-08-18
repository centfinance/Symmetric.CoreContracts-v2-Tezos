
import json
import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

from contracts.utils.mixins.Administrable import Administrable

from contracts.vault.AssetTransfersHandler import AssetTransfersHandler

f = open(".taq/config.local.testing.json")

data = json.load(f)

MAX_PROTOCOL_SWAP_FEE_PERCENTAGE = 500000000000000000  # 50%
# MAX_PROTOCOL_FLASH_LOAN_FEE_PERCENTAGE = 10000000000000000  # 1%

TOKEN = sp.TPair(sp.TAddress, sp.TOption(sp.TNat))


class ProtocolFeesCollector(
    sp.Contract,
    Administrable
):
    def __init__(
            self,
            vault=sp.address(data["contracts"]["Vault"]["address"]),
            admin=sp.address('tz1UGWQQ5YFkZqWgE3gqmPyuwy2R5VGpMM9B'),
    ):
        self.init(
            vault=vault,
            swapFeePercentage=sp.nat(0),
            flashLoanFeePercentage=sp.nat(0),
        )
        Administrable.__init__(self, admin)

    @sp.entry_point
    def withdrawCollectedFees(
        self,
        tokens,
        amounts,
        recipient
    ):
        sp.set_type(tokens, sp.TMap(sp.TNat, TOKEN))
        sp.set_type(amounts, sp.TMap(sp.TNat, sp.TNat))
        self.onlyAdministrator()

        sp.verify((sp.len(tokens) == sp.len(amounts)),
                  Errors.INPUT_LENGTH_MISMATCH)

        with sp.for_('i', sp.range(0, sp.len(tokens))) as i:
            token = tokens[i]
            amount = amounts[i]
            AssetTransfersHandler.TransferToken(
                sp.self_address,
                recipient,
                amount,
                sp.fst(token),
                sp.snd(token),
            )

    # @sp.entry_point
    # def setSwapFeePercentage(self, newSwapFeePercentage):
    #     self.onlyAdministrator()

    #     sp.verify(newSwapFeePercentage <= MAX_PROTOCOL_SWAP_FEE_PERCENTAGE,
    #               Errors.SWAP_FEE_PERCENTAGE_TOO_HIGH)
    #     self.data.swapFeePercentage = newSwapFeePercentage
    #     sp.emit(newSwapFeePercentage, 'SwapFeePercentageChanged', with_type=True)

    # @sp.entry_point
    # def setFlashLoanFeePercentage(self, newFlashLoanFeePercentage):
    #     self.onlyAdministrator()

    #     sp.verify(
    #         newFlashLoanFeePercentage <= MAX_PROTOCOL_FLASH_LOAN_FEE_PERCENTAGE,
    #         Errors.FLASH_LOAN_FEE_PERCENTAGE_TOO_HIGH
    #     )
    #     self.data.flashLoanFeePercentage = newFlashLoanFeePercentage
    #     sp.emit(newFlashLoanFeePercentage,
    #             'FlashLoanFeePercentageChanged', with_type=True)

    # @sp.onchain_view()
    # def getCollectedFeeAmounts(self, tokens):
    #     sp.set_type(tokens, sp.TMap(sp.TNat, TOKEN))
    #     feeAmounts = sp.compute(sp.map({}, tkey=sp.TNat, tvalue=sp.TNat))
    #     with sp.for_('i', sp.range(0, sp.len(tokens))) as i:
    #         feeAmounts[i] = sp.compute(sp.view(
    #             'getBalance',
    #             tokens[i].address,
    #             self.address,
    #             t=sp.TNat
    #         ).open_some('Invalid View'))


sp.add_compilation_target('ProtocolFeesCollector', ProtocolFeesCollector())
