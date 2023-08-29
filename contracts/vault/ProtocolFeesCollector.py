
import json
import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors

from contracts.utils.mixins.Administrable import Administrable

from contracts.vault.AssetTransfersHandler import AssetTransfersHandler

f = open(".taq/config.local.testing.json")

data = json.load(f)

MAX_PROTOCOL_SWAP_FEE_PERCENTAGE = 500000000000000000  # 50%

MAX_PROTOCOL_YIELD_FEE_PERCENTAGE = 500000000000000000 
# MAX_PROTOCOL_FLASH_LOAN_FEE_PERCENTAGE = 10000000000000000  # 1%

TOKEN = sp.TPair(sp.TAddress, sp.TOption(sp.TNat))

class IProtocolFeesCollector:
    def getSwapFeePercentage(collector):
        return sp.compute(sp.view('getSwapFeePercentage', collector, sp.unit,
                                  t=sp.TNat).open_some(Errors.GET_SWAP_FEE_PERCEMTAGE_INVALID))
    def getYieldFeePercentage(collector):
        return sp.compute(sp.view('getYieldFeePercentage', collector, sp.unit,
                                  t=sp.TNat).open_some(Errors.GET_YIELD_FEE_PERCEMTAGE_INVALID))

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
            yieldFeePercentage=sp.nat(0),
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

    @sp.entry_point
    def setSwapFeePercentage(self, newSwapFeePercentage):
        self.onlyAdministrator()

        sp.verify(newSwapFeePercentage <= MAX_PROTOCOL_SWAP_FEE_PERCENTAGE,
                  Errors.SWAP_FEE_PERCENTAGE_TOO_HIGH)
        self.data.swapFeePercentage = newSwapFeePercentage
        sp.emit(newSwapFeePercentage, 'SwapFeePercentageChanged', with_type=True)

    @sp.entry_point
    def setYieldFeePercentage(self, newYieldFeePercentage):
        self.onlyAdministrator()

        sp.verify(newYieldFeePercentage <= MAX_PROTOCOL_YIELD_FEE_PERCENTAGE,
                  Errors.SWAP_FEE_PERCENTAGE_TOO_HIGH)
        self.data.yieldFeePercentage = newYieldFeePercentage
        sp.emit(newYieldFeePercentage, 'YieldFeePercentageChanged', with_type=True)

    @sp.onchain_view()
    def getSwapFeePercentage(self):
        sp.result(self.data.swapFeePercentage)

    @sp.onchain_view()
    def getYieldFeePercentage(self):
        sp.result(self.data.yieldFeePercentage)

sp.add_compilation_target('ProtocolFeesCollector', ProtocolFeesCollector())
