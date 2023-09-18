import smartpy as sp

class Contract(sp.Contract):
  def __init__(self):
    self.init_type(sp.TRecord(admin = sp.TAddress, balances = sp.TBigMap(sp.TAddress, sp.TRecord(approvals = sp.TMap(sp.TAddress, sp.TNat), balance = sp.TNat).layout(("approvals", "balance"))), entries = sp.TBigMap(sp.TIntOrNat, sp.TNat), exemptFromYieldFees = sp.TBool, feeCache = sp.TPair(sp.TNat, sp.TNat), fixedPoint = sp.TBigMap(sp.TNat, sp.TLambda(sp.TPair(sp.TNat, sp.TNat), sp.TNat)), getTokenValue = sp.TLambda(sp.TTuple(sp.TPair(sp.TAddress, sp.TOption(sp.TNat)), sp.TMap(sp.TNat, sp.TPair(sp.TAddress, sp.TOption(sp.TNat))), sp.TMap(sp.TNat, sp.TNat)), sp.TNat), initialized = sp.TBool, metadata = sp.TBigMap(sp.TString, sp.TBytes), normalizedWeights = sp.TMap(sp.TNat, sp.TNat), poolId = sp.TOption(sp.TPair(sp.TAddress, sp.TNat)), proposed_admin = sp.TOption(sp.TAddress), protocolFeesCollector = sp.TAddress, rateProviders = sp.TOption(sp.TMap(sp.TNat, sp.TOption(sp.TAddress))), recoveryMode = sp.TBool, scalingFactors = sp.TMap(sp.TNat, sp.TNat), scaling_helpers = sp.TBigMap(sp.TIntOrNat, sp.TLambda(sp.TTuple(sp.TMap(sp.TNat, sp.TNat), sp.TMap(sp.TNat, sp.TNat), sp.TLambda(sp.TPair(sp.TNat, sp.TNat), sp.TNat)), sp.TMap(sp.TNat, sp.TNat))), settings = sp.TRecord(paused = sp.TBool).layout("paused"), token_metadata = sp.TBigMap(sp.TNat, sp.TRecord(token_id = sp.TNat, token_info = sp.TMap(sp.TString, sp.TBytes)).layout(("token_id", "token_info"))), tokens = sp.TMap(sp.TNat, sp.TPair(sp.TAddress, sp.TOption(sp.TNat))), totalSupply = sp.TNat, vault = sp.TAddress, weightedMathLib = sp.TAddress, weightedProtocolFeesLib = sp.TAddress).layout((((("admin", ("balances", "entries")), ("exemptFromYieldFees", ("feeCache", "fixedPoint"))), (("getTokenValue", ("initialized", "metadata")), ("normalizedWeights", ("poolId", "proposed_admin")))), ((("protocolFeesCollector", ("rateProviders", "recoveryMode")), ("scalingFactors", ("scaling_helpers", "settings"))), (("token_metadata", ("tokens", "totalSupply")), ("vault", ("weightedMathLib", "weightedProtocolFeesLib")))))))
    self.init(admin = sp.address('KT1N5Qpp5DaJzEgEXY1TW6Zne6Eehbxp83XF'),
              balances = {},
              entries = {11 : 0, 12 : 0, 13 : 1500000000000000},
              exemptFromYieldFees = True,
              feeCache = (0, 0),
              fixedPoint = {20 : sp.build_lambda(lambda _x2: (sp.fst(_x2) * sp.snd(_x2)) // 1000000000000000000), 21 : sp.build_lambda(lambda _x4: sp.as_nat(sp.fst(sp.ediv((sp.fst(_x4) * sp.snd(_x4)) - 1, 1000000000000000000).open_some()) + 1)), 22 : lambda, 23 : lambda},
              getTokenValue = lambda,
              initialized = False,
              metadata = {'' : sp.bytes('0x3c697066733a2f2f2e2e2e2e3e')},
              normalizedWeights = {},
              poolId = sp.none,
              proposed_admin = sp.none,
              protocolFeesCollector = sp.address('KT1N5Qpp5DaJzEgEXY1TW6Zne6Eehbxp83XF'),
              rateProviders = sp.none,
              recoveryMode = False,
              scalingFactors = {},
              scaling_helpers = {0 : lambda},
              settings = sp.record(paused = False),
              token_metadata = {0 : sp.record(token_id = 0, token_info = {'decimals' : sp.bytes('0x3138'), 'name' : sp.bytes('0x53796d6d657472696320576569676874656420506f6f6c'), 'symbol' : sp.bytes('0x53594d4d4c50'), 'thumbnailUri' : sp.bytes('0x697066733a2f2f2e2e2e2e2e2e')})},
              tokens = {},
              totalSupply = 0,
              vault = sp.address('KT1N5Qpp5DaJzEgEXY1TW6Zne6Eehbxp83XF'),
              weightedMathLib = sp.address('KT1SJtRC6xTfrrhx2ys1bkR3BSCrLNHrmHpy'),
              weightedProtocolFeesLib = sp.address('KT1SJtRC6xTfrrhx2ys1bkR3BSCrLNHrmHpy'))

  @sp.entrypoint
  def accept_admin(self, params):
    sp.verify(sp.some(sp.sender) == self.data.proposed_admin, 'NOT_PROPOSED_ADMIN')
    self.data.admin = sp.sender
    self.data.proposed_admin = sp.none

  @sp.entrypoint
  def afterExitPool(self, params):
    sp.verify(self.data.settings.paused == False, 'ONLY_UNPAUSED')
    sp.if params.recoveryModeExit:
      sp.verify(self.data.recoveryMode == True, 438)
      sp.set_type(sp.record(address = params.sender, value = params.sptAmountIn), sp.TRecord(address = sp.TAddress, value = sp.TNat).layout(("address", "value")))
      sp.verify(self.data.balances[params.sender].balance >= params.sptAmountIn)
      self.data.balances[params.sender].balance = sp.as_nat(self.data.balances[params.sender].balance - params.sptAmountIn)
      self.data.totalSupply = sp.as_nat(self.data.totalSupply - params.sptAmountIn)
    sp.else:
      compute_BasePool_357 = sp.local("compute_BasePool_357", self.data.scaling_helpers[0]((params.balances, self.data.scalingFactors, self.data.fixedPoint[20])))
      compute_BasePool_360 = sp.local("compute_BasePool_360", self.data.scaling_helpers[0]((params.amountsOut, self.data.scalingFactors, self.data.fixedPoint[20])))
      compute_BaseWeightedPool_375 = sp.local("compute_BaseWeightedPool_375", self.data.normalizedWeights)
      match_pair_WeightedPoolProtocolFees_55_fst, match_pair_WeightedPoolProtocolFees_55_snd = sp.match_tuple(self.data.feeCache, "match_pair_WeightedPoolProtocolFees_55_fst", "match_pair_WeightedPoolProtocolFees_55_snd")
      compute_WeightedPoolProtocolFees_57 = sp.local("compute_WeightedPoolProtocolFees_57", self.data.entries)
      compute_WeightedPoolProtocolFees_64 = sp.local("compute_WeightedPoolProtocolFees_64", self.data.rateProviders)
      sp.set_type(sp.record(athRateProduct = compute_WeightedPoolProtocolFees_57.value[11], exemptFromYieldFees = self.data.exemptFromYieldFees, normalizedWeights = compute_BaseWeightedPool_375.value, postJoinExitInvariant = compute_WeightedPoolProtocolFees_57.value[12], preJoinExitInvariant = params.invariant, preJoinExitSupply = self.data.totalSupply, rateProviders = compute_WeightedPoolProtocolFees_64.value, swapFee = match_pair_WeightedPoolProtocolFees_55_fst, yieldFee = match_pair_WeightedPoolProtocolFees_55_snd), sp.TRecord(athRateProduct = sp.TNat, exemptFromYieldFees = sp.TBool, normalizedWeights = sp.TMap(sp.TNat, sp.TNat), postJoinExitInvariant = sp.TNat, preJoinExitInvariant = sp.TNat, preJoinExitSupply = sp.TNat, rateProviders = sp.TOption(sp.TMap(sp.TNat, sp.TOption(sp.TAddress))), swapFee = sp.TNat, yieldFee = sp.TNat).layout(((("athRateProduct", "exemptFromYieldFees"), ("normalizedWeights", "postJoinExitInvariant")), (("preJoinExitInvariant", "preJoinExitSupply"), ("rateProviders", ("swapFee", "yieldFee"))))))
      compute_ExternalWeightedProtocolFees_48 = sp.local("compute_ExternalWeightedProtocolFees_48", sp.view("getPreJoinExitProtocolFees", sp.record(athRateProduct = compute_WeightedPoolProtocolFees_57.value[11], exemptFromYieldFees = self.data.exemptFromYieldFees, normalizedWeights = compute_BaseWeightedPool_375.value, postJoinExitInvariant = compute_WeightedPoolProtocolFees_57.value[12], preJoinExitInvariant = params.invariant, preJoinExitSupply = self.data.totalSupply, rateProviders = compute_WeightedPoolProtocolFees_64.value, swapFee = match_pair_WeightedPoolProtocolFees_55_fst, yieldFee = match_pair_WeightedPoolProtocolFees_55_snd), self.data.weightedProtocolFeesLib, sp.TPair(sp.TNat, sp.TNat)).open_some(message = 807))
      match_pair_WeightedPool_299_fst, match_pair_WeightedPool_299_snd = sp.match_tuple((sp.fst(compute_ExternalWeightedProtocolFees_48.value), sp.snd(compute_ExternalWeightedProtocolFees_48.value)), "match_pair_WeightedPool_299_fst", "match_pair_WeightedPool_299_snd")
      sp.if match_pair_WeightedPool_299_snd > 0:
        compute_WeightedPool_303 = sp.local("compute_WeightedPool_303", match_pair_WeightedPool_299_snd)
        self.data.entries[11] = compute_WeightedPool_303.value
      compute_WeightedPool_305 = sp.local("compute_WeightedPool_305", match_pair_WeightedPool_299_fst)
      sp.if compute_WeightedPool_305.value > 0:
        sp.set_type(sp.record(address = self.data.protocolFeesCollector, value = compute_WeightedPool_305.value), sp.TRecord(address = sp.TAddress, value = sp.TNat).layout(("address", "value")))
        sp.if ~ (self.data.balances.contains(self.data.protocolFeesCollector)):
          self.data.balances[self.data.protocolFeesCollector] = sp.record(approvals = {}, balance = 0)
        self.data.balances[self.data.protocolFeesCollector].balance += compute_WeightedPool_305.value
        self.data.totalSupply += compute_WeightedPool_305.value
      sp.set_type(sp.record(balanceDeltas = compute_BasePool_360.value, normalizedWeights = compute_BaseWeightedPool_375.value, postJoinExitSupply = sp.as_nat((self.data.totalSupply + match_pair_WeightedPool_299_fst) - params.sptAmountIn), preBalances = compute_BasePool_357.value, preJoinExitInvariant = params.invariant, preJoinExitSupply = self.data.totalSupply + match_pair_WeightedPool_299_fst, swapFee = sp.fst(self.data.feeCache)), sp.TRecord(balanceDeltas = sp.TMap(sp.TNat, sp.TNat), normalizedWeights = sp.TMap(sp.TNat, sp.TNat), postJoinExitSupply = sp.TNat, preBalances = sp.TMap(sp.TNat, sp.TNat), preJoinExitInvariant = sp.TNat, preJoinExitSupply = sp.TNat, swapFee = sp.TNat).layout((("balanceDeltas", ("normalizedWeights", "postJoinExitSupply")), (("preBalances", "preJoinExitInvariant"), ("preJoinExitSupply", "swapFee")))))
      compute_ExternalWeightedProtocolFees_54 = sp.local("compute_ExternalWeightedProtocolFees_54", sp.view("getPostJoinExitProtocolFees", sp.record(balanceDeltas = compute_BasePool_360.value, normalizedWeights = compute_BaseWeightedPool_375.value, postJoinExitSupply = sp.as_nat((self.data.totalSupply + match_pair_WeightedPool_299_fst) - params.sptAmountIn), preBalances = compute_BasePool_357.value, preJoinExitInvariant = params.invariant, preJoinExitSupply = self.data.totalSupply + match_pair_WeightedPool_299_fst, swapFee = sp.fst(self.data.feeCache)), self.data.weightedProtocolFeesLib, sp.TPair(sp.TNat, sp.TNat)).open_some(message = 808))
      self.data.entries[12] = sp.snd(compute_ExternalWeightedProtocolFees_54.value)
      compute_WeightedPool_327 = sp.local("compute_WeightedPool_327", sp.fst(compute_ExternalWeightedProtocolFees_54.value))
      sp.if compute_WeightedPool_327.value > 0:
        sp.set_type(sp.record(address = self.data.protocolFeesCollector, value = compute_WeightedPool_327.value), sp.TRecord(address = sp.TAddress, value = sp.TNat).layout(("address", "value")))
        sp.if ~ (self.data.balances.contains(self.data.protocolFeesCollector)):
          self.data.balances[self.data.protocolFeesCollector] = sp.record(approvals = {}, balance = 0)
        self.data.balances[self.data.protocolFeesCollector].balance += compute_WeightedPool_327.value
        self.data.totalSupply += compute_WeightedPool_327.value
      sp.set_type(sp.record(address = params.sender, value = params.sptAmountIn), sp.TRecord(address = sp.TAddress, value = sp.TNat).layout(("address", "value")))
      sp.verify(self.data.balances[params.sender].balance >= params.sptAmountIn)
      self.data.balances[params.sender].balance = sp.as_nat(self.data.balances[params.sender].balance - params.sptAmountIn)
      self.data.totalSupply = sp.as_nat(self.data.totalSupply - params.sptAmountIn)

  @sp.entrypoint
  def afterJoinPool(self, params):
    sp.verify(self.data.settings.paused == False, 'ONLY_UNPAUSED')
    sp.if self.data.totalSupply == 0:
      sp.if self.data.exemptFromYieldFees == False:
        sp.set_type(sp.record(normalizedWeights = self.data.normalizedWeights, rateProviders = self.data.rateProviders.open_some()), sp.TRecord(normalizedWeights = sp.TMap(sp.TNat, sp.TNat), rateProviders = sp.TMap(sp.TNat, sp.TOption(sp.TAddress))).layout(("normalizedWeights", "rateProviders")))
        compute_ExternalWeightedProtocolFees_60 = sp.local("compute_ExternalWeightedProtocolFees_60", sp.view("getRateProduct", sp.record(normalizedWeights = self.data.normalizedWeights, rateProviders = self.data.rateProviders.open_some()), self.data.weightedProtocolFeesLib, sp.TNat).open_some(message = 809))
        self.data.entries[11] = compute_ExternalWeightedProtocolFees_60.value
      self.data.entries[12] = params.invariant
      sp.verify(params.sptAmountOut >= 1000000, 204)
      sp.set_type(sp.record(address = sp.address('tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU'), value = 1000000), sp.TRecord(address = sp.TAddress, value = sp.TNat).layout(("address", "value")))
      sp.if ~ (self.data.balances.contains(sp.address('tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU'))):
        self.data.balances[sp.address('tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU')] = sp.record(approvals = {}, balance = 0)
      self.data.balances[sp.address('tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU')].balance += 1000000
      self.data.totalSupply += 1000000
      sp.set_type(sp.record(address = params.recipient, value = sp.as_nat(params.sptAmountOut - 1000000)), sp.TRecord(address = sp.TAddress, value = sp.TNat).layout(("address", "value")))
      sp.if ~ (self.data.balances.contains(params.recipient)):
        self.data.balances[params.recipient] = sp.record(approvals = {}, balance = 0)
      self.data.balances[params.recipient].balance += sp.as_nat(params.sptAmountOut - 1000000)
      self.data.totalSupply += sp.as_nat(params.sptAmountOut - 1000000)
    sp.else:
      compute_BasePool_307 = sp.local("compute_BasePool_307", self.data.scaling_helpers[0]((params.balances, self.data.scalingFactors, self.data.fixedPoint[20])))
      compute_BasePool_310 = sp.local("compute_BasePool_310", self.data.scaling_helpers[0]((params.amountsIn, self.data.scalingFactors, self.data.fixedPoint[20])))
      compute_BaseWeightedPool_227 = sp.local("compute_BaseWeightedPool_227", self.data.normalizedWeights)
      match_pair_WeightedPoolProtocolFees_55_fst, match_pair_WeightedPoolProtocolFees_55_snd = sp.match_tuple(self.data.feeCache, "match_pair_WeightedPoolProtocolFees_55_fst", "match_pair_WeightedPoolProtocolFees_55_snd")
      compute_WeightedPoolProtocolFees_57 = sp.local("compute_WeightedPoolProtocolFees_57", self.data.entries)
      compute_WeightedPoolProtocolFees_64 = sp.local("compute_WeightedPoolProtocolFees_64", self.data.rateProviders)
      sp.set_type(sp.record(athRateProduct = compute_WeightedPoolProtocolFees_57.value[11], exemptFromYieldFees = self.data.exemptFromYieldFees, normalizedWeights = compute_BaseWeightedPool_227.value, postJoinExitInvariant = compute_WeightedPoolProtocolFees_57.value[12], preJoinExitInvariant = params.invariant, preJoinExitSupply = self.data.totalSupply, rateProviders = compute_WeightedPoolProtocolFees_64.value, swapFee = match_pair_WeightedPoolProtocolFees_55_fst, yieldFee = match_pair_WeightedPoolProtocolFees_55_snd), sp.TRecord(athRateProduct = sp.TNat, exemptFromYieldFees = sp.TBool, normalizedWeights = sp.TMap(sp.TNat, sp.TNat), postJoinExitInvariant = sp.TNat, preJoinExitInvariant = sp.TNat, preJoinExitSupply = sp.TNat, rateProviders = sp.TOption(sp.TMap(sp.TNat, sp.TOption(sp.TAddress))), swapFee = sp.TNat, yieldFee = sp.TNat).layout(((("athRateProduct", "exemptFromYieldFees"), ("normalizedWeights", "postJoinExitInvariant")), (("preJoinExitInvariant", "preJoinExitSupply"), ("rateProviders", ("swapFee", "yieldFee"))))))
      compute_ExternalWeightedProtocolFees_48 = sp.local("compute_ExternalWeightedProtocolFees_48", sp.view("getPreJoinExitProtocolFees", sp.record(athRateProduct = compute_WeightedPoolProtocolFees_57.value[11], exemptFromYieldFees = self.data.exemptFromYieldFees, normalizedWeights = compute_BaseWeightedPool_227.value, postJoinExitInvariant = compute_WeightedPoolProtocolFees_57.value[12], preJoinExitInvariant = params.invariant, preJoinExitSupply = self.data.totalSupply, rateProviders = compute_WeightedPoolProtocolFees_64.value, swapFee = match_pair_WeightedPoolProtocolFees_55_fst, yieldFee = match_pair_WeightedPoolProtocolFees_55_snd), self.data.weightedProtocolFeesLib, sp.TPair(sp.TNat, sp.TNat)).open_some(message = 807))
      match_pair_WeightedPool_299_fst, match_pair_WeightedPool_299_snd = sp.match_tuple((sp.fst(compute_ExternalWeightedProtocolFees_48.value), sp.snd(compute_ExternalWeightedProtocolFees_48.value)), "match_pair_WeightedPool_299_fst", "match_pair_WeightedPool_299_snd")
      sp.if match_pair_WeightedPool_299_snd > 0:
        compute_WeightedPool_303 = sp.local("compute_WeightedPool_303", match_pair_WeightedPool_299_snd)
        self.data.entries[11] = compute_WeightedPool_303.value
      compute_WeightedPool_305 = sp.local("compute_WeightedPool_305", match_pair_WeightedPool_299_fst)
      sp.if compute_WeightedPool_305.value > 0:
        sp.set_type(sp.record(address = self.data.protocolFeesCollector, value = compute_WeightedPool_305.value), sp.TRecord(address = sp.TAddress, value = sp.TNat).layout(("address", "value")))
        sp.if ~ (self.data.balances.contains(self.data.protocolFeesCollector)):
          self.data.balances[self.data.protocolFeesCollector] = sp.record(approvals = {}, balance = 0)
        self.data.balances[self.data.protocolFeesCollector].balance += compute_WeightedPool_305.value
        self.data.totalSupply += compute_WeightedPool_305.value
      sp.set_type(sp.record(balanceDeltas = compute_BasePool_310.value, normalizedWeights = compute_BaseWeightedPool_227.value, postJoinExitSupply = (self.data.totalSupply + match_pair_WeightedPool_299_fst) + params.sptAmountOut, preBalances = compute_BasePool_307.value, preJoinExitInvariant = params.invariant, preJoinExitSupply = self.data.totalSupply + match_pair_WeightedPool_299_fst, swapFee = sp.fst(self.data.feeCache)), sp.TRecord(balanceDeltas = sp.TMap(sp.TNat, sp.TNat), normalizedWeights = sp.TMap(sp.TNat, sp.TNat), postJoinExitSupply = sp.TNat, preBalances = sp.TMap(sp.TNat, sp.TNat), preJoinExitInvariant = sp.TNat, preJoinExitSupply = sp.TNat, swapFee = sp.TNat).layout((("balanceDeltas", ("normalizedWeights", "postJoinExitSupply")), (("preBalances", "preJoinExitInvariant"), ("preJoinExitSupply", "swapFee")))))
      compute_ExternalWeightedProtocolFees_54 = sp.local("compute_ExternalWeightedProtocolFees_54", sp.view("getPostJoinExitProtocolFees", sp.record(balanceDeltas = compute_BasePool_310.value, normalizedWeights = compute_BaseWeightedPool_227.value, postJoinExitSupply = (self.data.totalSupply + match_pair_WeightedPool_299_fst) + params.sptAmountOut, preBalances = compute_BasePool_307.value, preJoinExitInvariant = params.invariant, preJoinExitSupply = self.data.totalSupply + match_pair_WeightedPool_299_fst, swapFee = sp.fst(self.data.feeCache)), self.data.weightedProtocolFeesLib, sp.TPair(sp.TNat, sp.TNat)).open_some(message = 808))
      self.data.entries[12] = sp.snd(compute_ExternalWeightedProtocolFees_54.value)
      compute_WeightedPool_327 = sp.local("compute_WeightedPool_327", sp.fst(compute_ExternalWeightedProtocolFees_54.value))
      sp.if compute_WeightedPool_327.value > 0:
        sp.set_type(sp.record(address = self.data.protocolFeesCollector, value = compute_WeightedPool_327.value), sp.TRecord(address = sp.TAddress, value = sp.TNat).layout(("address", "value")))
        sp.if ~ (self.data.balances.contains(self.data.protocolFeesCollector)):
          self.data.balances[self.data.protocolFeesCollector] = sp.record(approvals = {}, balance = 0)
        self.data.balances[self.data.protocolFeesCollector].balance += compute_WeightedPool_327.value
        self.data.totalSupply += compute_WeightedPool_327.value
      sp.set_type(sp.record(address = params.recipient, value = params.sptAmountOut), sp.TRecord(address = sp.TAddress, value = sp.TNat).layout(("address", "value")))
      sp.if ~ (self.data.balances.contains(params.recipient)):
        self.data.balances[params.recipient] = sp.record(approvals = {}, balance = 0)
      self.data.balances[params.recipient].balance += params.sptAmountOut
      self.data.totalSupply += params.sptAmountOut

  @sp.entrypoint
  def approve(self, params):
    sp.verify(sp.amount == sp.tez(0), 'FA1.2_TezSentToEntrypoint')
    sp.set_type(params, sp.TRecord(spender = sp.TAddress, value = sp.TNat).layout(("spender", "value")))
    sp.if ~ (self.data.balances.contains(sp.sender)):
      self.data.balances[sp.sender] = sp.record(approvals = {}, balance = 0)
    sp.verify((self.data.balances[sp.sender].approvals.get(params.spender, default_value = 0) == 0) | (params.value == 0), 'FA1.2_UnsafeAllowanceChange')
    self.data.balances[sp.sender].approvals[params.spender] = params.value

  @sp.entrypoint
  def disableRecoveryMode(self):
    sp.verify(self.data.admin == sp.set_type_expr(sp.sender, sp.TAddress), 'ONLY_ADMIN')
    sp.verify(self.data.recoveryMode == True, 438)
    self.data.recoveryMode = False
    sp.if True:
      compute_BaseWeightedPool_49 = sp.local("compute_BaseWeightedPool_49", sp.view("getPoolTokens", self.data.poolId.open_some(), self.data.vault, sp.TPair(sp.TMap(sp.TNat, sp.TPair(sp.TAddress, sp.TOption(sp.TNat))), sp.TMap(sp.TNat, sp.TNat))).open_some(message = 813))
      compute_BaseWeightedPool_54 = sp.local("compute_BaseWeightedPool_54", self.data.scaling_helpers[0]((sp.snd(compute_BaseWeightedPool_49.value), self.data.scalingFactors, self.data.fixedPoint[20])))
      sp.set_type(sp.record(balances = compute_BaseWeightedPool_54.value, normalizedWeights = self.data.normalizedWeights), sp.TRecord(balances = sp.TMap(sp.TNat, sp.TNat), normalizedWeights = sp.TMap(sp.TNat, sp.TNat)).layout(("balances", "normalizedWeights")))
      compute_ExternalWeightedMath_93 = sp.local("compute_ExternalWeightedMath_93", sp.view("calculateInvariant", sp.record(balances = compute_BaseWeightedPool_54.value, normalizedWeights = self.data.normalizedWeights), self.data.weightedMathLib, sp.TNat).open_some(message = 802))
      self.data.entries[12] = compute_ExternalWeightedMath_93.value
      sp.if self.data.exemptFromYieldFees == False:
        sp.set_type(sp.record(normalizedWeights = self.data.normalizedWeights, rateProviders = self.data.rateProviders.open_some()), sp.TRecord(normalizedWeights = sp.TMap(sp.TNat, sp.TNat), rateProviders = sp.TMap(sp.TNat, sp.TOption(sp.TAddress))).layout(("normalizedWeights", "rateProviders")))
        compute_ExternalWeightedProtocolFees_60 = sp.local("compute_ExternalWeightedProtocolFees_60", sp.view("getRateProduct", sp.record(normalizedWeights = self.data.normalizedWeights, rateProviders = self.data.rateProviders.open_some()), self.data.weightedProtocolFeesLib, sp.TNat).open_some(message = 809))
        sp.if compute_ExternalWeightedProtocolFees_60.value > self.data.entries[11]:
          self.data.entries[11] = compute_ExternalWeightedProtocolFees_60.value
    sp.emit(False, tag = "RecoveryModeStateChanged")

  @sp.entrypoint
  def enableRecoveryMode(self):
    sp.verify(self.data.admin == sp.set_type_expr(sp.sender, sp.TAddress), 'ONLY_ADMIN')
    sp.verify(self.data.recoveryMode == False, 437)
    self.data.recoveryMode = True
    sp.if False:
      compute_BaseWeightedPool_49 = sp.local("compute_BaseWeightedPool_49", sp.view("getPoolTokens", self.data.poolId.open_some(), self.data.vault, sp.TPair(sp.TMap(sp.TNat, sp.TPair(sp.TAddress, sp.TOption(sp.TNat))), sp.TMap(sp.TNat, sp.TNat))).open_some(message = 813))
      compute_BaseWeightedPool_54 = sp.local("compute_BaseWeightedPool_54", self.data.scaling_helpers[0]((sp.snd(compute_BaseWeightedPool_49.value), self.data.scalingFactors, self.data.fixedPoint[20])))
      sp.set_type(sp.record(balances = compute_BaseWeightedPool_54.value, normalizedWeights = self.data.normalizedWeights), sp.TRecord(balances = sp.TMap(sp.TNat, sp.TNat), normalizedWeights = sp.TMap(sp.TNat, sp.TNat)).layout(("balances", "normalizedWeights")))
      compute_ExternalWeightedMath_93 = sp.local("compute_ExternalWeightedMath_93", sp.view("calculateInvariant", sp.record(balances = compute_BaseWeightedPool_54.value, normalizedWeights = self.data.normalizedWeights), self.data.weightedMathLib, sp.TNat).open_some(message = 802))
      self.data.entries[12] = compute_ExternalWeightedMath_93.value
      sp.if self.data.exemptFromYieldFees == False:
        sp.set_type(sp.record(normalizedWeights = self.data.normalizedWeights, rateProviders = self.data.rateProviders.open_some()), sp.TRecord(normalizedWeights = sp.TMap(sp.TNat, sp.TNat), rateProviders = sp.TMap(sp.TNat, sp.TOption(sp.TAddress))).layout(("normalizedWeights", "rateProviders")))
        compute_ExternalWeightedProtocolFees_60 = sp.local("compute_ExternalWeightedProtocolFees_60", sp.view("getRateProduct", sp.record(normalizedWeights = self.data.normalizedWeights, rateProviders = self.data.rateProviders.open_some()), self.data.weightedProtocolFeesLib, sp.TNat).open_some(message = 809))
        sp.if compute_ExternalWeightedProtocolFees_60.value > self.data.entries[11]:
          self.data.entries[11] = compute_ExternalWeightedProtocolFees_60.value
    sp.emit(True, tag = "RecoveryModeStateChanged")

  @sp.entrypoint
  def initializePool(self):
    sp.verify(self.data.initialized == False)
    compute_PoolRegistrationLib_44 = sp.local("compute_PoolRegistrationLib_44", sp.view("getNextPoolNonce", sp.unit, self.data.vault, sp.TNat).open_some(message = 814))
    sp.transfer(sp.unit, sp.tez(0), sp.contract(sp.TUnit, self.data.vault, entrypoint='registerPool').open_some(message = 'registerPoolFail'))
    sp.transfer(sp.record(assetManagers = sp.none, poolId = (sp.self_address, compute_PoolRegistrationLib_44.value), tokens = self.data.tokens), sp.tez(0), sp.contract(sp.TRecord(assetManagers = sp.TOption(sp.TMap(sp.TNat, sp.TAddress)), poolId = sp.TPair(sp.TAddress, sp.TNat), tokens = sp.TMap(sp.TNat, sp.TPair(sp.TAddress, sp.TOption(sp.TNat)))).layout(("assetManagers", ("poolId", "tokens"))), self.data.vault, entrypoint='registerTokens').open_some(message = 'registerTokensFail'))
    self.data.poolId = sp.some((sp.self_address, compute_PoolRegistrationLib_44.value))
    self.data.initialized = True

  @sp.entrypoint
  def run_lambda(self, params):
    sp.set_type(params, sp.TLambda(sp.TUnit, sp.TList(sp.TOperation), with_storage="read-write", tstorage=sp.TRecord(admin = sp.TAddress, balances = sp.TBigMap(sp.TAddress, sp.TRecord(approvals = sp.TMap(sp.TAddress, sp.TNat), balance = sp.TNat).layout(("approvals", "balance"))), entries = sp.TBigMap(sp.TIntOrNat, sp.TNat), exemptFromYieldFees = sp.TBool, feeCache = sp.TPair(sp.TNat, sp.TNat), fixedPoint = sp.TBigMap(sp.TNat, sp.TLambda(sp.TPair(sp.TNat, sp.TNat), sp.TNat)), getTokenValue = sp.TLambda(sp.TTuple(sp.TPair(sp.TAddress, sp.TOption(sp.TNat)), sp.TMap(sp.TNat, sp.TPair(sp.TAddress, sp.TOption(sp.TNat))), sp.TMap(sp.TNat, sp.TNat)), sp.TNat), initialized = sp.TBool, metadata = sp.TBigMap(sp.TString, sp.TBytes), normalizedWeights = sp.TMap(sp.TNat, sp.TNat), poolId = sp.TOption(sp.TPair(sp.TAddress, sp.TNat)), proposed_admin = sp.TOption(sp.TAddress), protocolFeesCollector = sp.TAddress, rateProviders = sp.TOption(sp.TMap(sp.TNat, sp.TOption(sp.TAddress))), recoveryMode = sp.TBool, scalingFactors = sp.TMap(sp.TNat, sp.TNat), scaling_helpers = sp.TBigMap(sp.TIntOrNat, sp.TLambda(sp.TTuple(sp.TMap(sp.TNat, sp.TNat), sp.TMap(sp.TNat, sp.TNat), sp.TLambda(sp.TPair(sp.TNat, sp.TNat), sp.TNat)), sp.TMap(sp.TNat, sp.TNat))), settings = sp.TRecord(paused = sp.TBool).layout("paused"), token_metadata = sp.TBigMap(sp.TNat, sp.TRecord(token_id = sp.TNat, token_info = sp.TMap(sp.TString, sp.TBytes)).layout(("token_id", "token_info"))), tokens = sp.TMap(sp.TNat, sp.TPair(sp.TAddress, sp.TOption(sp.TNat))), totalSupply = sp.TNat, vault = sp.TAddress, weightedMathLib = sp.TAddress, weightedProtocolFeesLib = sp.TAddress).layout((((("admin", ("balances", "entries")), ("exemptFromYieldFees", ("feeCache", "fixedPoint"))), (("getTokenValue", ("initialized", "metadata")), ("normalizedWeights", ("poolId", "proposed_admin")))), ((("protocolFeesCollector", ("rateProviders", "recoveryMode")), ("scalingFactors", ("scaling_helpers", "settings"))), (("token_metadata", ("tokens", "totalSupply")), ("vault", ("weightedMathLib", "weightedProtocolFeesLib")))))), with_operations=True))
    sp.verify(self.data.admin == sp.set_type_expr(sp.sender, sp.TAddress), 'ONLY_ADMIN')
    sp.for op in params(sp.unit):
      sp.operations().push(op)

  @sp.entrypoint
  def setSwapFeePercentage(self, params):
    sp.verify(self.data.settings.paused == False, 'ONLY_UNPAUSED')
    sp.verify(self.data.admin == sp.set_type_expr(sp.sender, sp.TAddress), 'ONLY_ADMIN')
    sp.verify(params >= 1000000000000, 203)
    sp.verify(params <= 100000000000000000, 202)
    self.data.entries[13] = params
    sp.emit(params, tag = "SwapFeePercentageChanged")

  @sp.entrypoint
  def set_paused(self, params):
    sp.verify(self.data.admin == sp.set_type_expr(sp.sender, sp.TAddress), 'ONLY_ADMIN')
    self.data.settings.paused = params

  @sp.entrypoint
  def transfer(self, params):
    sp.set_type(params, sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value"))))
    result = sp.local("result", False)
    sp.if sp.sender == self.data.vault:
      result.value = True
    sp.else:
      result.value = self.data.balances[params.from_].approvals.get(sp.sender, default_value = 0) >= params.value
    sp.verify((params.from_ == sp.sender) | result.value, 'FA1.2_NotEnoughAllowance')
    sp.verify(sp.amount == sp.tez(0), 'FA1.2_TezSentToEntrypoint')
    sp.if ~ (self.data.balances.contains(params.from_)):
      self.data.balances[params.from_] = sp.record(approvals = {}, balance = 0)
    sp.if ~ (self.data.balances.contains(params.to_)):
      self.data.balances[params.to_] = sp.record(approvals = {}, balance = 0)
    sp.verify(self.data.balances[params.from_].balance >= params.value, 'FA1.2_NotEnoughBalance')
    self.data.balances[params.from_].balance = sp.as_nat(self.data.balances[params.from_].balance - params.value)
    self.data.balances[params.to_].balance += params.value
    sp.if params.from_ != sp.sender:
      self.data.balances[params.from_].approvals[sp.sender] = sp.as_nat(self.data.balances[params.from_].approvals[sp.sender] - params.value)

  @sp.entrypoint
  def transfer_admin(self, params):
    sp.verify(self.data.admin == sp.set_type_expr(sp.sender, sp.TAddress), 'ONLY_ADMIN')
    self.data.proposed_admin = sp.some(params)

  @sp.entrypoint
  def updateProtocolFeePercentageCache(self):
    sp.verify(self.data.settings.paused == False, 'ONLY_UNPAUSED')
    compute_WeightedPool_365 = sp.local("compute_WeightedPool_365", self.data.totalSupply)
    compute_BaseWeightedPool_49 = sp.local("compute_BaseWeightedPool_49", sp.view("getPoolTokens", self.data.poolId.open_some(), self.data.vault, sp.TPair(sp.TMap(sp.TNat, sp.TPair(sp.TAddress, sp.TOption(sp.TNat))), sp.TMap(sp.TNat, sp.TNat))).open_some(message = 813))
    compute_BaseWeightedPool_54 = sp.local("compute_BaseWeightedPool_54", self.data.scaling_helpers[0]((sp.snd(compute_BaseWeightedPool_49.value), self.data.scalingFactors, self.data.fixedPoint[20])))
    sp.set_type(sp.record(balances = compute_BaseWeightedPool_54.value, normalizedWeights = self.data.normalizedWeights), sp.TRecord(balances = sp.TMap(sp.TNat, sp.TNat), normalizedWeights = sp.TMap(sp.TNat, sp.TNat)).layout(("balances", "normalizedWeights")))
    compute_ExternalWeightedMath_93 = sp.local("compute_ExternalWeightedMath_93", sp.view("calculateInvariant", sp.record(balances = compute_BaseWeightedPool_54.value, normalizedWeights = self.data.normalizedWeights), self.data.weightedMathLib, sp.TNat).open_some(message = 802))
    compute_WeightedPool_371 = sp.local("compute_WeightedPool_371", self.data.scalingFactors)
    match_pair_WeightedPoolProtocolFees_55_fst, match_pair_WeightedPoolProtocolFees_55_snd = sp.match_tuple(self.data.feeCache, "match_pair_WeightedPoolProtocolFees_55_fst", "match_pair_WeightedPoolProtocolFees_55_snd")
    compute_WeightedPoolProtocolFees_57 = sp.local("compute_WeightedPoolProtocolFees_57", self.data.entries)
    compute_WeightedPoolProtocolFees_64 = sp.local("compute_WeightedPoolProtocolFees_64", self.data.rateProviders)
    sp.set_type(sp.record(athRateProduct = compute_WeightedPoolProtocolFees_57.value[11], exemptFromYieldFees = self.data.exemptFromYieldFees, normalizedWeights = compute_WeightedPool_371.value, postJoinExitInvariant = compute_WeightedPoolProtocolFees_57.value[12], preJoinExitInvariant = compute_ExternalWeightedMath_93.value, preJoinExitSupply = compute_WeightedPool_365.value, rateProviders = compute_WeightedPoolProtocolFees_64.value, swapFee = match_pair_WeightedPoolProtocolFees_55_fst, yieldFee = match_pair_WeightedPoolProtocolFees_55_snd), sp.TRecord(athRateProduct = sp.TNat, exemptFromYieldFees = sp.TBool, normalizedWeights = sp.TMap(sp.TNat, sp.TNat), postJoinExitInvariant = sp.TNat, preJoinExitInvariant = sp.TNat, preJoinExitSupply = sp.TNat, rateProviders = sp.TOption(sp.TMap(sp.TNat, sp.TOption(sp.TAddress))), swapFee = sp.TNat, yieldFee = sp.TNat).layout(((("athRateProduct", "exemptFromYieldFees"), ("normalizedWeights", "postJoinExitInvariant")), (("preJoinExitInvariant", "preJoinExitSupply"), ("rateProviders", ("swapFee", "yieldFee"))))))
    compute_ExternalWeightedProtocolFees_48 = sp.local("compute_ExternalWeightedProtocolFees_48", sp.view("getPreJoinExitProtocolFees", sp.record(athRateProduct = compute_WeightedPoolProtocolFees_57.value[11], exemptFromYieldFees = self.data.exemptFromYieldFees, normalizedWeights = compute_WeightedPool_371.value, postJoinExitInvariant = compute_WeightedPoolProtocolFees_57.value[12], preJoinExitInvariant = compute_ExternalWeightedMath_93.value, preJoinExitSupply = compute_WeightedPool_365.value, rateProviders = compute_WeightedPoolProtocolFees_64.value, swapFee = match_pair_WeightedPoolProtocolFees_55_fst, yieldFee = match_pair_WeightedPoolProtocolFees_55_snd), self.data.weightedProtocolFeesLib, sp.TPair(sp.TNat, sp.TNat)).open_some(message = 807))
    sp.if sp.fst(compute_ExternalWeightedProtocolFees_48.value) > 0:
      sp.set_type(sp.record(address = self.data.protocolFeesCollector, value = sp.fst(compute_ExternalWeightedProtocolFees_48.value)), sp.TRecord(address = sp.TAddress, value = sp.TNat).layout(("address", "value")))
      sp.if ~ (self.data.balances.contains(self.data.protocolFeesCollector)):
        self.data.balances[self.data.protocolFeesCollector] = sp.record(approvals = {}, balance = 0)
      self.data.balances[self.data.protocolFeesCollector].balance += sp.fst(compute_ExternalWeightedProtocolFees_48.value)
      self.data.totalSupply += sp.fst(compute_ExternalWeightedProtocolFees_48.value)
    self.data.entries[12] = compute_ExternalWeightedMath_93.value
    sp.if self.data.entries[11] > 0:
      self.data.entries[11] = sp.snd(compute_ExternalWeightedProtocolFees_48.value)
    compute_ProtocolFeesCollector_23 = sp.local("compute_ProtocolFeesCollector_23", sp.view("getSwapFeePercentage", sp.unit, self.data.protocolFeesCollector, sp.TNat).open_some(message = 816))
    compute_ProtocolFeesCollector_26 = sp.local("compute_ProtocolFeesCollector_26", sp.view("getYieldFeePercentage", sp.unit, self.data.protocolFeesCollector, sp.TNat).open_some(message = 817))
    self.data.feeCache = (compute_ProtocolFeesCollector_23.value, compute_ProtocolFeesCollector_26.value)

  @sp.private_lambda()
  def onlyVault(_x0):
    sp.verify(sp.sender == self.data.vault)
    sp.verify(_x0 == self.data.poolId)

sp.add_compilation_target("test", Contract())