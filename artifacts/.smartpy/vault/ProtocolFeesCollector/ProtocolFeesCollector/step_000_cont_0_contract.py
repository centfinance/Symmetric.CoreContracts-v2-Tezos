import smartpy as sp

class Contract(sp.Contract):
  def __init__(self):
    self.init_type(sp.TRecord(admin = sp.TAddress, proposed_admin = sp.TOption(sp.TAddress), swapFeePercentage = sp.TNat, vault = sp.TAddress, yieldFeePercentage = sp.TNat).layout((("admin", "proposed_admin"), ("swapFeePercentage", ("vault", "yieldFeePercentage")))))
    self.init(admin = sp.address('tz1UGWQQ5YFkZqWgE3gqmPyuwy2R5VGpMM9B'),
              proposed_admin = sp.none,
              swapFeePercentage = 0,
              vault = sp.address('KT1L6L7n9cq7ExJFDD45PkpPACedufffKRbP'),
              yieldFeePercentage = 0)

  @sp.entrypoint
  def accept_admin(self, params):
    sp.verify(sp.some(sp.sender) == self.data.proposed_admin, 'NOT_PROPOSED_ADMIN')
    self.data.admin = sp.sender
    self.data.proposed_admin = sp.none

  @sp.entrypoint
  def run_lambda(self, params):
    sp.set_type(params, sp.TLambda(sp.TUnit, sp.TList(sp.TOperation), with_storage="read-write", tstorage=sp.TRecord(admin = sp.TAddress, proposed_admin = sp.TOption(sp.TAddress), swapFeePercentage = sp.TNat, vault = sp.TAddress, yieldFeePercentage = sp.TNat).layout((("admin", "proposed_admin"), ("swapFeePercentage", ("vault", "yieldFeePercentage")))), with_operations=True))
    sp.verify(self.data.admin == sp.set_type_expr(sp.sender, sp.TAddress), 'ONLY_ADMIN')
    sp.for op in params(sp.unit):
      sp.operations().push(op)

  @sp.entrypoint
  def setSwapFeePercentage(self, params):
    sp.verify(self.data.admin == sp.set_type_expr(sp.sender, sp.TAddress), 'ONLY_ADMIN')
    sp.verify(params <= 500000000000000000, 600)
    self.data.swapFeePercentage = params
    sp.emit(params, tag = "SwapFeePercentageChanged")

  @sp.entrypoint
  def setYieldFeePercentage(self, params):
    sp.verify(self.data.admin == sp.set_type_expr(sp.sender, sp.TAddress), 'ONLY_ADMIN')
    sp.verify(params <= 500000000000000000, 600)
    self.data.yieldFeePercentage = params
    sp.emit(params, tag = "YieldFeePercentageChanged")

  @sp.entrypoint
  def transfer_admin(self, params):
    sp.verify(self.data.admin == sp.set_type_expr(sp.sender, sp.TAddress), 'ONLY_ADMIN')
    self.data.proposed_admin = sp.some(params)

  @sp.entrypoint
  def withdrawCollectedFees(self, params):
    sp.set_type(params.tokens, sp.TMap(sp.TNat, sp.TPair(sp.TAddress, sp.TOption(sp.TNat))))
    sp.set_type(params.amounts, sp.TMap(sp.TNat, sp.TNat))
    sp.verify(self.data.admin == sp.set_type_expr(sp.sender, sp.TAddress), 'ONLY_ADMIN')
    sp.verify(sp.len(params.tokens) == sp.len(params.amounts), 103)
    sp.for i in sp.range(0, sp.len(params.tokens)):
      sp.verify(params.amounts[i] > 0, 'Zero_Transfer')
      sp.if sp.snd(params.tokens[i]) != sp.none:
        sp.transfer(sp.list([sp.record(from_ = sp.self_address, txs = sp.list([sp.record(amount = params.amounts[i], to_ = params.recipient, token_id = sp.snd(params.tokens[i]).open_some())]))]), sp.tez(0), sp.contract(sp.TList(sp.TRecord(from_ = sp.TAddress, txs = sp.TList(sp.TRecord(amount = sp.TNat, to_ = sp.TAddress, token_id = sp.TNat).layout(("to_", ("token_id", "amount"))))).layout(("from_", "txs"))), sp.fst(params.tokens[i]), entrypoint='transfer').open_some())
      sp.else:
        sp.transfer(sp.record(from_ = sp.self_address, to_ = params.recipient, value = params.amounts[i]), sp.tez(0), sp.contract(sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value"))), sp.fst(params.tokens[i]), entrypoint='transfer').open_some())

sp.add_compilation_target("test", Contract())