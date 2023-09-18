import smartpy as sp

class Contract(sp.Contract):
  def __init__(self):
    self.init_type(sp.TRecord(admin = sp.TAddress, isPoolRegistered = sp.TBigMap(sp.TPair(sp.TAddress, sp.TNat), sp.TUnit), metadata = sp.TBigMap(sp.TString, sp.TBytes), nextPoolNonce = sp.TNat, poolsBalances = sp.TBigMap(sp.TPair(sp.TAddress, sp.TNat), sp.TMap(sp.TPair(sp.TAddress, sp.TOption(sp.TNat)), sp.TPair(sp.TNat, sp.TNat))), poolsTokens = sp.TBigMap(sp.TPair(sp.TAddress, sp.TNat), sp.TMap(sp.TNat, sp.TPair(sp.TAddress, sp.TOption(sp.TNat)))), proposed_admin = sp.TOption(sp.TAddress), settings = sp.TRecord(paused = sp.TBool).layout("paused")).layout(((("admin", "isPoolRegistered"), ("metadata", "nextPoolNonce")), (("poolsBalances", "poolsTokens"), ("proposed_admin", "settings")))))
    self.init(admin = sp.address('tz1UGWQQ5YFkZqWgE3gqmPyuwy2R5VGpMM9B'),
              isPoolRegistered = {},
              metadata = {'' : sp.bytes('0x68747470733a2f2f7261772e67697468756275736572636f6e74656e742e636f6d2f63656e7466696e616e63652f53796d6d65747269632e436f7265436f6e7472616374732d76322d54657a6f732f6d61696e2f6d657461646174612f746573746e65742f5661756c742e6a736f6e')},
              nextPoolNonce = 1,
              poolsBalances = {},
              poolsTokens = {},
              proposed_admin = sp.none,
              settings = sp.record(paused = False))

  @sp.entrypoint
  def accept_admin(self, params):
    sp.verify(sp.some(sp.sender) == self.data.proposed_admin, 'NOT_PROPOSED_ADMIN')
    self.data.admin = sp.sender
    self.data.proposed_admin = sp.none

  @sp.entrypoint
  def batchSwap(self, params):
    sp.verify(self.data.settings.paused == False, 'ONLY_UNPAUSED')
    sp.verify(params.funds.sender == sp.source, 401)
    sp.verify(sp.now <= params.deadline, 508)
    sp.verify(sp.len(params.assets) == sp.len(params.limits), 103)
    compute_Swaps_199 = sp.local("compute_Swaps_199", {}, sp.TMap(sp.TNat, sp.TInt))
    previousTokenCalculated = sp.local("previousTokenCalculated", (sp.address('tz1burnburnburnburnburnburnburjAYjjX'), sp.none))
    previousAmountCalculated = sp.local("previousAmountCalculated", 0)
    sp.for i in sp.range(0, sp.len(params.swaps)):
      sp.verify((params.swaps[i].assetInIndex < sp.len(params.assets)) & (params.swaps[i].assetOutIndex < sp.len(params.assets)), 100)
      sp.verify(params.assets[params.swaps[i].assetInIndex] != params.assets[params.swaps[i].assetOutIndex], 509)
      amount = sp.local("amount", params.swaps[i].amount)
      sp.if params.swaps[i].amount == 0:
        sp.verify(i > 0, 510)
        compute_Swaps_223 = sp.local("compute_Swaps_223", sp.eif(params.kind == 7, params.assets[params.swaps[i].assetInIndex], params.assets[params.swaps[i].assetOutIndex]))
        sp.verify(previousTokenCalculated.value == compute_Swaps_223.value, 511)
        amount.value = previousAmountCalculated.value
      compute_Swaps_325 = sp.local("compute_Swaps_325", sp.view("onSwap", sp.record(balanceTokenIn = sp.fst(self.data.poolsBalances.get(params.swaps[i].poolId, message = 500).get(params.assets[params.swaps[i].assetInIndex], message = 521)) + sp.snd(self.data.poolsBalances.get(params.swaps[i].poolId, message = 500).get(params.assets[params.swaps[i].assetInIndex], message = 521)), balanceTokenOut = sp.fst(self.data.poolsBalances.get(params.swaps[i].poolId, message = 500).get(params.assets[params.swaps[i].assetOutIndex], message = 521)) + sp.snd(self.data.poolsBalances.get(params.swaps[i].poolId, message = 500).get(params.assets[params.swaps[i].assetOutIndex], message = 521)), request = sp.record(amount = amount.value, kind = params.kind, tokenIn = params.assets[params.swaps[i].assetInIndex], tokenOut = params.assets[params.swaps[i].assetOutIndex])), sp.fst(params.swaps[i].poolId), sp.TNat).open_some(message = 812))
      compute_Swaps_328 = sp.local("compute_Swaps_328", sp.eif(params.kind == 7, (amount.value, compute_Swaps_325.value), (compute_Swaps_325.value, amount.value)))
      match_pair_Swaps_328_fst, match_pair_Swaps_328_snd = sp.match_tuple(compute_Swaps_328.value, "match_pair_Swaps_328_fst", "match_pair_Swaps_328_snd")
      self.data.poolsBalances[params.swaps[i].poolId][params.assets[params.swaps[i].assetInIndex]] = (sp.fst(self.data.poolsBalances.get(params.swaps[i].poolId, message = 500).get(params.assets[params.swaps[i].assetInIndex], message = 521)) + match_pair_Swaps_328_fst, sp.snd(self.data.poolsBalances.get(params.swaps[i].poolId, message = 500).get(params.assets[params.swaps[i].assetInIndex], message = 521)))
      self.data.poolsBalances[params.swaps[i].poolId][params.assets[params.swaps[i].assetOutIndex]] = (sp.as_nat(sp.fst(self.data.poolsBalances.get(params.swaps[i].poolId, message = 500).get(params.assets[params.swaps[i].assetOutIndex], message = 521)) - match_pair_Swaps_328_snd), sp.snd(self.data.poolsBalances.get(params.swaps[i].poolId, message = 500).get(params.assets[params.swaps[i].assetOutIndex], message = 521)))
      match_pair_Swaps_269_fst, match_pair_Swaps_269_snd = sp.match_tuple(sp.eif(params.kind == 7, (amount.value, compute_Swaps_325.value), (compute_Swaps_325.value, amount.value)), "match_pair_Swaps_269_fst", "match_pair_Swaps_269_snd")
      sp.emit(sp.record(amountIn = match_pair_Swaps_269_fst, amountOut = match_pair_Swaps_269_snd, poolId = params.swaps[i].poolId, tokenIn = (sp.fst(params.assets[params.swaps[i].assetInIndex]), sp.snd(params.assets[params.swaps[i].assetInIndex])), tokenOut = (sp.fst(params.assets[params.swaps[i].assetOutIndex]), sp.snd(params.assets[params.swaps[i].assetOutIndex]))), tag = "Swap")
      previousAmountCalculated.value = compute_Swaps_325.value
      compute_Swaps_243 = sp.local("compute_Swaps_243", sp.eif(params.kind == 7, params.assets[params.swaps[i].assetOutIndex], params.assets[params.swaps[i].assetInIndex]))
      previousTokenCalculated.value = compute_Swaps_243.value
      compute_Swaps_199.value[params.swaps[i].assetInIndex] = compute_Swaps_199.value.get(params.swaps[i].assetInIndex, default_value = 0) + sp.to_int(match_pair_Swaps_269_fst)
      compute_Swaps_199.value[params.swaps[i].assetOutIndex] = compute_Swaps_199.value.get(params.swaps[i].assetOutIndex, default_value = 0) - sp.to_int(match_pair_Swaps_269_snd)
    sp.for i in sp.range(0, sp.len(params.assets)):
      sp.verify(compute_Swaps_199.value[i] <= params.limits[i], 507)
      sp.if compute_Swaps_199.value[i] > 0:
        sp.if sp.as_nat(compute_Swaps_199.value[i]) > 0:
          sp.verify(sp.as_nat(compute_Swaps_199.value[i]) > 0, 'Zero_Transfer')
          sp.if sp.snd(params.assets[i]) != sp.none:
            sp.transfer(sp.list([sp.record(from_ = params.funds.sender, txs = sp.list([sp.record(amount = sp.as_nat(compute_Swaps_199.value[i]), to_ = sp.self_address, token_id = sp.snd(params.assets[i]).open_some())]))]), sp.tez(0), sp.contract(sp.TList(sp.TRecord(from_ = sp.TAddress, txs = sp.TList(sp.TRecord(amount = sp.TNat, to_ = sp.TAddress, token_id = sp.TNat).layout(("to_", ("token_id", "amount"))))).layout(("from_", "txs"))), sp.fst(params.assets[i]), entrypoint='transfer').open_some())
          sp.else:
            sp.transfer(sp.record(from_ = params.funds.sender, to_ = sp.self_address, value = sp.as_nat(compute_Swaps_199.value[i])), sp.tez(0), sp.contract(sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value"))), sp.fst(params.assets[i]), entrypoint='transfer').open_some())
      sp.if compute_Swaps_199.value[i] < 0:
        sp.if (abs(compute_Swaps_199.value[i])) > 0:
          sp.verify((abs(compute_Swaps_199.value[i])) > 0, 'Zero_Transfer')
          sp.if sp.snd(params.assets[i]) != sp.none:
            sp.transfer(sp.list([sp.record(from_ = sp.self_address, txs = sp.list([sp.record(amount = abs(compute_Swaps_199.value[i]), to_ = params.funds.recipient, token_id = sp.snd(params.assets[i]).open_some())]))]), sp.tez(0), sp.contract(sp.TList(sp.TRecord(from_ = sp.TAddress, txs = sp.TList(sp.TRecord(amount = sp.TNat, to_ = sp.TAddress, token_id = sp.TNat).layout(("to_", ("token_id", "amount"))))).layout(("from_", "txs"))), sp.fst(params.assets[i]), entrypoint='transfer').open_some())
          sp.else:
            sp.transfer(sp.record(from_ = sp.self_address, to_ = params.funds.recipient, value = abs(compute_Swaps_199.value[i])), sp.tez(0), sp.contract(sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value"))), sp.fst(params.assets[i]), entrypoint='transfer').open_some())

  @sp.entrypoint
  def exitPool(self, params):
    sp.verify(self.data.settings.paused == False, 'ONLY_UNPAUSED')
    sp.verify(params.sender == sp.source, 401)
    sp.verify(self.data.isPoolRegistered.contains(params.poolId), 500)
    compute_PoolBalances_164 = sp.local("compute_PoolBalances_164", self._validateTokensAndGetBalances(sp.record(expectedTokens = params.request.assets, limits = params.request.limits, poolId = params.poolId)))
    compute_BalanceAllocation_5 = sp.local("compute_BalanceAllocation_5", {}, sp.TMap(sp.TNat, sp.TNat))
    sp.for i in sp.range(0, sp.len(compute_PoolBalances_164.value)):
      compute_BalanceAllocation_5.value[i] = sp.fst(compute_PoolBalances_164.value[i]) + sp.snd(compute_PoolBalances_164.value[i])
    compute_PoolBalances_176 = sp.local("compute_PoolBalances_176", sp.view("beforeExitPool", sp.record(balances = compute_BalanceAllocation_5.value, userData = params.request.userData), sp.fst(params.poolId), sp.TTuple(sp.TNat, sp.TMap(sp.TNat, sp.TNat), sp.TNat)).open_some(message = 811))
    sptAmountIn, amountsOut, invariant = sp.match_tuple(compute_PoolBalances_176.value, "sptAmountIn", "amountsOut", "invariant")
    sp.transfer(sp.record(amountsOut = amountsOut, balances = compute_BalanceAllocation_5.value, invariant = invariant, poolId = params.poolId, recoveryModeExit = params.request.userData.recoveryModeExit, sender = params.sender, sptAmountIn = sptAmountIn), sp.tez(0), sp.contract(sp.TRecord(amountsOut = sp.TMap(sp.TNat, sp.TNat), balances = sp.TMap(sp.TNat, sp.TNat), invariant = sp.TNat, poolId = sp.TPair(sp.TAddress, sp.TNat), recoveryModeExit = sp.TBool, sender = sp.TAddress, sptAmountIn = sp.TNat).layout((("amountsOut", ("balances", "invariant")), (("poolId", "recoveryModeExit"), ("sender", "sptAmountIn")))), sp.fst(params.poolId), entrypoint='afterExitPool').open_some(message = 'INTERFACE_MISMATCH'))
    sp.verify(sp.len(compute_PoolBalances_164.value) == sp.len(amountsOut))
    compute_PoolBalances_258 = sp.local("compute_PoolBalances_258", {}, sp.TMap(sp.TNat, sp.TPair(sp.TNat, sp.TNat)))
    sp.for x in sp.range(0, sp.len(params.request.assets)):
      sp.verify(amountsOut[x] >= params.request.limits[x], 505)
      sp.if amountsOut[x] > 0:
        sp.verify(amountsOut[x] > 0, 'Zero_Transfer')
        sp.if sp.snd(params.request.assets[x]) != sp.none:
          sp.transfer(sp.list([sp.record(from_ = sp.self_address, txs = sp.list([sp.record(amount = amountsOut[x], to_ = params.sender, token_id = sp.snd(params.request.assets[x]).open_some())]))]), sp.tez(0), sp.contract(sp.TList(sp.TRecord(from_ = sp.TAddress, txs = sp.TList(sp.TRecord(amount = sp.TNat, to_ = sp.TAddress, token_id = sp.TNat).layout(("to_", ("token_id", "amount"))))).layout(("from_", "txs"))), sp.fst(params.request.assets[x]), entrypoint='transfer').open_some())
        sp.else:
          sp.transfer(sp.record(from_ = sp.self_address, to_ = params.sender, value = amountsOut[x]), sp.tez(0), sp.contract(sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value"))), sp.fst(params.request.assets[x]), entrypoint='transfer').open_some())
      compute_PoolBalances_258.value[x] = (sp.as_nat(sp.fst(compute_PoolBalances_164.value[x]) - amountsOut[x]), sp.snd(compute_PoolBalances_164.value[x]))
    sp.for i in sp.range(0, sp.len(params.request.assets)):
      self.data.poolsBalances[params.poolId][params.request.assets[i]] = compute_PoolBalances_258.value[i]
    sp.emit(sp.record(amountsInOrOut = self._castToInt(sp.record(amounts = amountsOut, positive = False)), poolId = params.poolId, sender = params.sender, tokens = params.request.assets), tag = "PoolBalanceChanged")

  @sp.entrypoint
  def joinPool(self, params):
    sp.verify(self.data.settings.paused == False, 'ONLY_UNPAUSED')
    sp.verify(params.sender == sp.source, 401)
    sp.verify(self.data.isPoolRegistered.contains(params.poolId), 500)
    compute_PoolBalances_86 = sp.local("compute_PoolBalances_86", self._validateTokensAndGetBalances(sp.record(expectedTokens = params.request.assets, limits = params.request.limits, poolId = params.poolId)))
    compute_BalanceAllocation_5 = sp.local("compute_BalanceAllocation_5", {}, sp.TMap(sp.TNat, sp.TNat))
    sp.for i in sp.range(0, sp.len(compute_PoolBalances_86.value)):
      compute_BalanceAllocation_5.value[i] = sp.fst(compute_PoolBalances_86.value[i]) + sp.snd(compute_PoolBalances_86.value[i])
    compute_PoolBalances_97 = sp.local("compute_PoolBalances_97", sp.view("beforeJoinPool", sp.record(balances = compute_BalanceAllocation_5.value, userData = params.request.userData), sp.fst(params.poolId), sp.TTuple(sp.TNat, sp.TMap(sp.TNat, sp.TNat), sp.TNat)).open_some(message = 810))
    sptAmountOut, amountsIn, invariant = sp.match_tuple(compute_PoolBalances_97.value, "sptAmountOut", "amountsIn", "invariant")
    sp.transfer(sp.record(amountsIn = amountsIn, balances = compute_BalanceAllocation_5.value, invariant = invariant, poolId = params.poolId, recipient = params.recipient, sptAmountOut = sptAmountOut), sp.tez(0), sp.contract(sp.TRecord(amountsIn = sp.TMap(sp.TNat, sp.TNat), balances = sp.TMap(sp.TNat, sp.TNat), invariant = sp.TNat, poolId = sp.TPair(sp.TAddress, sp.TNat), recipient = sp.TAddress, sptAmountOut = sp.TNat).layout((("amountsIn", ("balances", "invariant")), ("poolId", ("recipient", "sptAmountOut")))), sp.fst(params.poolId), entrypoint='afterJoinPool').open_some(message = 'INTERFACE_MISMATCH'))
    sp.verify(sp.len(compute_PoolBalances_86.value) == sp.len(amountsIn))
    compute_PoolBalances_231 = sp.local("compute_PoolBalances_231", {}, sp.TMap(sp.TNat, sp.TPair(sp.TNat, sp.TNat)))
    sp.for x in sp.range(0, sp.len(params.request.assets)):
      sp.verify(amountsIn[x] <= params.request.limits[x], 506)
      sp.if amountsIn[x] > 0:
        sp.verify(amountsIn[x] > 0, 'Zero_Transfer')
        sp.if sp.snd(params.request.assets[x]) != sp.none:
          sp.transfer(sp.list([sp.record(from_ = params.sender, txs = sp.list([sp.record(amount = amountsIn[x], to_ = sp.self_address, token_id = sp.snd(params.request.assets[x]).open_some())]))]), sp.tez(0), sp.contract(sp.TList(sp.TRecord(from_ = sp.TAddress, txs = sp.TList(sp.TRecord(amount = sp.TNat, to_ = sp.TAddress, token_id = sp.TNat).layout(("to_", ("token_id", "amount"))))).layout(("from_", "txs"))), sp.fst(params.request.assets[x]), entrypoint='transfer').open_some())
        sp.else:
          sp.transfer(sp.record(from_ = params.sender, to_ = sp.self_address, value = amountsIn[x]), sp.tez(0), sp.contract(sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value"))), sp.fst(params.request.assets[x]), entrypoint='transfer').open_some())
      compute_PoolBalances_231.value[x] = (sp.fst(compute_PoolBalances_86.value[x]) + amountsIn[x], sp.snd(compute_PoolBalances_86.value[x]))
    sp.for i in sp.range(0, sp.len(params.request.assets)):
      self.data.poolsBalances[params.poolId][params.request.assets[i]] = compute_PoolBalances_231.value[i]
    sp.emit(sp.record(amountsInOrOut = self._castToInt(sp.record(amounts = amountsIn, positive = True)), poolId = params.poolId, sender = params.sender, tokens = params.request.assets), tag = "PoolBalanceChanged")

  @sp.entrypoint
  def registerPool(self):
    sp.verify(self.data.settings.paused == False, 'ONLY_UNPAUSED')
    compute_PoolRegistry_57 = sp.local("compute_PoolRegistry_57", self.data.nextPoolNonce)
    self.data.isPoolRegistered[(sp.sender, compute_PoolRegistry_57.value)] = sp.unit
    self.data.nextPoolNonce += 1
    sp.emit(sp.record(pool = sp.sender, poolId = (sp.sender, compute_PoolRegistry_57.value)), tag = "PoolRegistered")

  @sp.entrypoint
  def registerTokens(self, params):
    sp.set_type(params, sp.TRecord(assetManagers = sp.TOption(sp.TMap(sp.TNat, sp.TAddress)), poolId = sp.TPair(sp.TAddress, sp.TNat), tokens = sp.TMap(sp.TNat, sp.TPair(sp.TAddress, sp.TOption(sp.TNat)))).layout(("assetManagers", ("poolId", "tokens"))))
    sp.verify(self.data.settings.paused == False, 'ONLY_UNPAUSED')
    sp.verify(self.data.isPoolRegistered.contains(params.poolId), 500)
    sp.verify(sp.sender == sp.fst(params.poolId), 501)
    sp.if self.data.poolsTokens.contains(params.poolId):
      sp.for i in sp.range(0, sp.len(params.tokens)):
        contains = sp.local("contains", False)
        sp.for e in self.data.poolsTokens[params.poolId].values():
          sp.if e == params.tokens[i]:
            contains.value = True
        sp.verify(contains.value == False)
        self.data.poolsTokens[params.poolId][sp.len(self.data.poolsTokens[params.poolId])] = params.tokens[i]
    sp.else:
      self.data.poolsTokens[params.poolId] = params.tokens
      self.data.poolsBalances[params.poolId] = sp.set_type_expr({}, sp.TMap(sp.TPair(sp.TAddress, sp.TOption(sp.TNat)), sp.TPair(sp.TNat, sp.TNat)))
    sp.emit(sp.record(poolId = params.poolId, tokens = params.tokens), tag = "TokensRegistered")

  @sp.entrypoint
  def run_lambda(self, params):
    sp.set_type(params, sp.TLambda(sp.TUnit, sp.TList(sp.TOperation), with_storage="read-write", tstorage=sp.TRecord(admin = sp.TAddress, isPoolRegistered = sp.TBigMap(sp.TPair(sp.TAddress, sp.TNat), sp.TUnit), metadata = sp.TBigMap(sp.TString, sp.TBytes), nextPoolNonce = sp.TNat, poolsBalances = sp.TBigMap(sp.TPair(sp.TAddress, sp.TNat), sp.TMap(sp.TPair(sp.TAddress, sp.TOption(sp.TNat)), sp.TPair(sp.TNat, sp.TNat))), poolsTokens = sp.TBigMap(sp.TPair(sp.TAddress, sp.TNat), sp.TMap(sp.TNat, sp.TPair(sp.TAddress, sp.TOption(sp.TNat)))), proposed_admin = sp.TOption(sp.TAddress), settings = sp.TRecord(paused = sp.TBool).layout("paused")).layout(((("admin", "isPoolRegistered"), ("metadata", "nextPoolNonce")), (("poolsBalances", "poolsTokens"), ("proposed_admin", "settings")))), with_operations=True))
    sp.verify(self.data.admin == sp.set_type_expr(sp.sender, sp.TAddress), 'ONLY_ADMIN')
    sp.for op in params(sp.unit):
      sp.operations().push(op)

  @sp.entrypoint
  def set_paused(self, params):
    sp.verify(self.data.admin == sp.set_type_expr(sp.sender, sp.TAddress), 'ONLY_ADMIN')
    self.data.settings.paused = params

  @sp.entrypoint
  def swap(self, params):
    sp.verify(self.data.settings.paused == False, 'ONLY_UNPAUSED')
    sp.verify(params.funds.sender == sp.source, 401)
    sp.verify(sp.now <= params.deadline, 508)
    sp.verify(params.singleSwap.amount > 0, 510)
    sp.verify(params.singleSwap.assetIn != params.singleSwap.assetOut, 509)
    compute_Swaps_325 = sp.local("compute_Swaps_325", sp.view("onSwap", sp.record(balanceTokenIn = sp.fst(self.data.poolsBalances.get(params.singleSwap.poolId, message = 500).get(params.singleSwap.assetIn, message = 521)) + sp.snd(self.data.poolsBalances.get(params.singleSwap.poolId, message = 500).get(params.singleSwap.assetIn, message = 521)), balanceTokenOut = sp.fst(self.data.poolsBalances.get(params.singleSwap.poolId, message = 500).get(params.singleSwap.assetOut, message = 521)) + sp.snd(self.data.poolsBalances.get(params.singleSwap.poolId, message = 500).get(params.singleSwap.assetOut, message = 521)), request = sp.record(amount = params.singleSwap.amount, kind = params.singleSwap.kind, tokenIn = params.singleSwap.assetIn, tokenOut = params.singleSwap.assetOut)), sp.fst(params.singleSwap.poolId), sp.TNat).open_some(message = 812))
    compute_Swaps_328 = sp.local("compute_Swaps_328", sp.eif(params.singleSwap.kind == 7, (params.singleSwap.amount, compute_Swaps_325.value), (compute_Swaps_325.value, params.singleSwap.amount)))
    match_pair_Swaps_328_fst, match_pair_Swaps_328_snd = sp.match_tuple(compute_Swaps_328.value, "match_pair_Swaps_328_fst", "match_pair_Swaps_328_snd")
    self.data.poolsBalances[params.singleSwap.poolId][params.singleSwap.assetIn] = (sp.fst(self.data.poolsBalances.get(params.singleSwap.poolId, message = 500).get(params.singleSwap.assetIn, message = 521)) + match_pair_Swaps_328_fst, sp.snd(self.data.poolsBalances.get(params.singleSwap.poolId, message = 500).get(params.singleSwap.assetIn, message = 521)))
    self.data.poolsBalances[params.singleSwap.poolId][params.singleSwap.assetOut] = (sp.as_nat(sp.fst(self.data.poolsBalances.get(params.singleSwap.poolId, message = 500).get(params.singleSwap.assetOut, message = 521)) - match_pair_Swaps_328_snd), sp.snd(self.data.poolsBalances.get(params.singleSwap.poolId, message = 500).get(params.singleSwap.assetOut, message = 521)))
    match_pair_Swaps_269_fst, match_pair_Swaps_269_snd = sp.match_tuple(sp.eif(params.singleSwap.kind == 7, (params.singleSwap.amount, compute_Swaps_325.value), (compute_Swaps_325.value, params.singleSwap.amount)), "match_pair_Swaps_269_fst", "match_pair_Swaps_269_snd")
    sp.emit(sp.record(amountIn = match_pair_Swaps_269_fst, amountOut = match_pair_Swaps_269_snd, poolId = params.singleSwap.poolId, tokenIn = (sp.fst(params.singleSwap.assetIn), sp.snd(params.singleSwap.assetIn)), tokenOut = (sp.fst(params.singleSwap.assetOut), sp.snd(params.singleSwap.assetOut))), tag = "Swap")
    sp.verify(sp.eif(params.singleSwap.kind == 7, match_pair_Swaps_269_snd >= params.limit, match_pair_Swaps_269_fst <= params.limit), 507)
    sp.if match_pair_Swaps_269_fst > 0:
      sp.verify(match_pair_Swaps_269_fst > 0, 'Zero_Transfer')
      sp.if sp.snd(params.singleSwap.assetIn) != sp.none:
        sp.transfer(sp.list([sp.record(from_ = params.funds.sender, txs = sp.list([sp.record(amount = match_pair_Swaps_269_fst, to_ = sp.self_address, token_id = sp.snd(params.singleSwap.assetIn).open_some())]))]), sp.tez(0), sp.contract(sp.TList(sp.TRecord(from_ = sp.TAddress, txs = sp.TList(sp.TRecord(amount = sp.TNat, to_ = sp.TAddress, token_id = sp.TNat).layout(("to_", ("token_id", "amount"))))).layout(("from_", "txs"))), sp.fst(params.singleSwap.assetIn), entrypoint='transfer').open_some())
      sp.else:
        sp.transfer(sp.record(from_ = params.funds.sender, to_ = sp.self_address, value = match_pair_Swaps_269_fst), sp.tez(0), sp.contract(sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value"))), sp.fst(params.singleSwap.assetIn), entrypoint='transfer').open_some())
    sp.if match_pair_Swaps_269_snd > 0:
      sp.verify(match_pair_Swaps_269_snd > 0, 'Zero_Transfer')
      sp.if sp.snd(params.singleSwap.assetOut) != sp.none:
        sp.transfer(sp.list([sp.record(from_ = sp.self_address, txs = sp.list([sp.record(amount = match_pair_Swaps_269_snd, to_ = params.funds.recipient, token_id = sp.snd(params.singleSwap.assetOut).open_some())]))]), sp.tez(0), sp.contract(sp.TList(sp.TRecord(from_ = sp.TAddress, txs = sp.TList(sp.TRecord(amount = sp.TNat, to_ = sp.TAddress, token_id = sp.TNat).layout(("to_", ("token_id", "amount"))))).layout(("from_", "txs"))), sp.fst(params.singleSwap.assetOut), entrypoint='transfer').open_some())
      sp.else:
        sp.transfer(sp.record(from_ = sp.self_address, to_ = params.funds.recipient, value = match_pair_Swaps_269_snd), sp.tez(0), sp.contract(sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value"))), sp.fst(params.singleSwap.assetOut), entrypoint='transfer').open_some())

  @sp.entrypoint
  def transfer_admin(self, params):
    sp.verify(self.data.admin == sp.set_type_expr(sp.sender, sp.TAddress), 'ONLY_ADMIN')
    self.data.proposed_admin = sp.some(params)

  @sp.private_lambda()
  def _castToInt(_x0):
    compute_PoolBalances_309 = sp.local("compute_PoolBalances_309", {})
    sp.for i in sp.range(0, sp.len(_x0.amounts)):
      sp.if _x0.positive:
        compute_PoolBalances_309.value[i] = sp.to_int(_x0.amounts[i])
      sp.else:
        compute_PoolBalances_309.value[i] = - sp.to_int(_x0.amounts[i])
    sp.result(compute_PoolBalances_309.value)

  @sp.private_lambda()
  def _validateTokensAndGetBalances(_x2):
    sp.verify(sp.len(_x2.expectedTokens) == sp.len(_x2.limits))
    compute_PoolTokens_168 = sp.local("compute_PoolTokens_168", {}, sp.TMap(sp.TNat, sp.TPair(sp.TAddress, sp.TOption(sp.TNat))))
    compute_PoolTokens_169 = sp.local("compute_PoolTokens_169", {}, sp.TMap(sp.TNat, sp.TPair(sp.TNat, sp.TNat)))
    sp.for i in sp.range(0, sp.len(self.data.poolsTokens[_x2.poolId])):
      compute_PoolTokens_168.value[i] = self.data.poolsTokens[_x2.poolId][i]
      compute_PoolTokens_169.value[i] = self.data.poolsBalances.get(_x2.poolId, default_value = {}).get(self.data.poolsTokens[_x2.poolId][i], default_value = (0, 0))
    sp.verify(sp.len(compute_PoolTokens_168.value) == sp.len(_x2.expectedTokens))
    sp.verify(sp.len(compute_PoolTokens_168.value) > 0, 527)
    sp.for i in sp.range(0, sp.len(compute_PoolTokens_168.value)):
      sp.verify(compute_PoolTokens_168.value[i] == _x2.expectedTokens[i], 520)
    sp.result(compute_PoolTokens_169.value)

sp.add_compilation_target("test", Contract())