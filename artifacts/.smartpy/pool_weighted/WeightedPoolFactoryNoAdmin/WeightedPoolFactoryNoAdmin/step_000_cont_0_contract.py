import smartpy as sp

class Contract(sp.Contract):
  def __init__(self):
    self.init_type(sp.TRecord(admin = sp.TAddress, feeCache = sp.TPair(sp.TNat, sp.TNat), isPoolFromFactory = sp.TBigMap(sp.TAddress, sp.TUnit), lastPool = sp.TAddress, metadata = sp.TBigMap(sp.TString, sp.TBytes), protocolFeeProvider = sp.TAddress, vault = sp.TAddress, weightedMathLib = sp.TAddress, weightedProtocolFeesLib = sp.TAddress).layout(((("admin", "feeCache"), ("isPoolFromFactory", "lastPool")), (("metadata", "protocolFeeProvider"), ("vault", ("weightedMathLib", "weightedProtocolFeesLib"))))))
    self.init(admin = sp.address('tz1UGWQQ5YFkZqWgE3gqmPyuwy2R5VGpMM9B'),
              feeCache = (400000000000000000, 400000000000000000),
              isPoolFromFactory = {},
              lastPool = sp.address('KT1H2SaqZyCmmHxbsTfwx12YeUzugzj8eN2t'),
              metadata = {'' : sp.bytes('0x68747470733a2f2f7261772e67697468756275736572636f6e74656e742e636f6d2f63656e7466696e616e63652f53796d6d65747269632e436f7265436f6e7472616374732d76322d54657a6f732f6d61696e2f6d657461646174612f746573746e65742f5765696768746564506f6f6c466163746f72792e6a736f6e')},
              protocolFeeProvider = sp.address('KT1AadsFF9ogbKySycWQm5i5avTAgcVwpY3e'),
              vault = sp.address('KT1L6L7n9cq7ExJFDD45PkpPACedufffKRbP'),
              weightedMathLib = sp.address('KT19aJTzRK1SC131ZQa7Lr6kDfC4KPm9Kjry'),
              weightedProtocolFeesLib = sp.address('KT195jeqmRvGR25GTvoecXg25nCdCZubWT6N'))

  @sp.entrypoint
  def create(self, params):
    sp.verify(sp.len(params.tokens) >= 2, 200)
    sp.verify(sp.len(params.tokens) <= 8, 201)
    sp.verify((sp.len(params.tokens) == sp.len(params.normalizedWeights)) & (sp.len(params.tokens) == sp.len(params.tokenDecimals)))
    normalizedSum = sp.local("normalizedSum", 0)
    sp.for i in sp.range(0, sp.len(params.tokens)):
      sp.verify(params.normalizedWeights[i] >= 10000000000000000, 302)
      normalizedSum.value += params.normalizedWeights[i]
    sp.verify(normalizedSum.value == 1000000000000000000, 308)
    compute_WeightedPoolFactoryNoAdmin_131 = sp.local("compute_WeightedPoolFactoryNoAdmin_131", {}, sp.TMap(sp.TNat, sp.TNat))
    sp.for i in sp.range(0, sp.len(params.tokens)):
      sp.set_type(params.tokenDecimals[i], sp.TNat)
      match_pair_WeightedPoolFactoryNoAdmin_216_fst, match_pair_WeightedPoolFactoryNoAdmin_216_snd = sp.match_tuple((10, sp.as_nat(18 - params.tokenDecimals[i])), "match_pair_WeightedPoolFactoryNoAdmin_216_fst", "match_pair_WeightedPoolFactoryNoAdmin_216_snd")
      powResult = sp.local("powResult", 1)
      base = sp.local("base", match_pair_WeightedPoolFactoryNoAdmin_216_fst)
      exponent = sp.local("exponent", match_pair_WeightedPoolFactoryNoAdmin_216_snd)
      sp.while exponent.value != 0:
        sp.if (exponent.value % 2) != 0:
          powResult.value *= base.value
        exponent.value = exponent.value >> 1
        base.value *= base.value
      compute_WeightedPoolFactoryNoAdmin_131.value[i] = 1000000000000000000 * powResult.value
    exemptFromYieldFees = sp.local("exemptFromYieldFees", True)
    sp.if params.rateProviders.is_some():
      sp.verify(sp.len(params.tokens) == sp.len(params.rateProviders.open_some()))
      exempt = sp.local("exempt", True)
      sp.for i in sp.range(0, sp.len(params.rateProviders.open_some())):
        sp.if params.rateProviders.open_some()[i] != sp.none:
          exempt.value = False
      exemptFromYieldFees.value = exempt.value
    sp.verify(params.swapFeePercentage >= 1000000000000, 203)
    sp.verify(params.swapFeePercentage <= 100000000000000000, 202)
    def f_x0(_x0):
      sp.set_type(_x0, sp.TTuple(sp.TPair(sp.TAddress, sp.TOption(sp.TNat)), sp.TMap(sp.TNat, sp.TPair(sp.TAddress, sp.TOption(sp.TNat))), sp.TMap(sp.TNat, sp.TNat)))
      token, tokens, entries = sp.match_tuple(_x0, "token", "tokens", "entries")
      entry = sp.local("entry", 0)
      sp.for i in sp.range(0, sp.len(entries)):
        sp.if tokens[i] == token:
          entry.value = entries[i]
      sp.if entry.value == 0:
        sp.failwith(309)
      sp.result(entry.value)
    compute_WeightedPoolFactoryNoAdmin_179 = sp.local("compute_WeightedPoolFactoryNoAdmin_179", sp.build_lambda(f_x0))
    def f_x8(_x8):
      sp.verify(sp.snd(_x8) != 0)
      sp.result((sp.fst(_x8) * 1000000000000000000) // sp.snd(_x8))
    def f_x10(_x10):
      sp.verify(sp.snd(_x10) != 0)
      sp.result(sp.as_nat(((sp.fst(_x10) * 1000000000000000000) + sp.snd(_x10)) - 1) // sp.snd(_x10))
    def f_x2(_x2):
      sp.set_type(_x2, sp.TTuple(sp.TPair(sp.TAddress, sp.TOption(sp.TNat)), sp.TMap(sp.TNat, sp.TPair(sp.TAddress, sp.TOption(sp.TNat))), sp.TMap(sp.TNat, sp.TNat)))
      token, tokens, entries = sp.match_tuple(_x2, "token", "tokens", "entries")
      entry = sp.local("entry", 0)
      sp.for i in sp.range(0, sp.len(entries)):
        sp.if tokens[i] == token:
          entry.value = entries[i]
      sp.if entry.value == 0:
        sp.failwith(309)
      sp.result(entry.value)
    def f_x12(_x12):
      sp.set_type(_x12, sp.TTuple(sp.TMap(sp.TNat, sp.TNat), sp.TMap(sp.TNat, sp.TNat), sp.TLambda(sp.TPair(sp.TNat, sp.TNat), sp.TNat)))
      amounts, scaling_factors, scale_func = sp.match_tuple(_x12, "amounts", "scaling_factors", "scale_func")
      compute_ScalingHelpers_47 = sp.local("compute_ScalingHelpers_47", {}, sp.TMap(sp.TNat, sp.TNat))
      sp.for i in sp.range(0, sp.len(amounts)):
        compute_ScalingHelpers_47.value[i] = scale_func((amounts[i], scaling_factors[i]))
      sp.result(compute_ScalingHelpers_47.value)
    def f_x2(_x2):
      sp.verify(sp.sender == self.data.vault)
      sp.verify(_x2 == self.data.poolId)
    def f_x18(_x18):
      sp.verify(sp.snd(_x18) != 0)
      sp.result((sp.fst(_x18) * 1000000000000000000) // sp.snd(_x18))
    def f_x20(_x20):
      sp.verify(sp.snd(_x20) != 0)
      sp.result(sp.as_nat(((sp.fst(_x20) * 1000000000000000000) + sp.snd(_x20)) - 1) // sp.snd(_x20))
    def f_x22(_x22):
      sp.set_type(_x22, sp.TTuple(sp.TMap(sp.TNat, sp.TNat), sp.TMap(sp.TNat, sp.TNat), sp.TLambda(sp.TPair(sp.TNat, sp.TNat), sp.TNat)))
      amounts, scaling_factors, scale_func = sp.match_tuple(_x22, "amounts", "scaling_factors", "scale_func")
      compute_ScalingHelpers_47 = sp.local("compute_ScalingHelpers_47", {}, sp.TMap(sp.TNat, sp.TNat))
      sp.for i in sp.range(0, sp.len(amounts)):
        compute_ScalingHelpers_47.value[i] = scale_func((amounts[i], scaling_factors[i]))
      sp.result(compute_ScalingHelpers_47.value)
    create_contract_BasePoolFactoryNoAdmin_24 = sp.local("create_contract_BasePoolFactoryNoAdmin_24", create contract ...)
    sp.operations().push(create_contract_BasePoolFactoryNoAdmin_24.value.operation)
    self.data.lastPool = create_contract_BasePoolFactoryNoAdmin_24.value.address
    self.data.isPoolFromFactory[create_contract_BasePoolFactoryNoAdmin_24.value.address] = sp.unit
    sp.emit(create_contract_BasePoolFactoryNoAdmin_24.value.address, tag = "PoolCreated")

  @sp.entrypoint
  def initialize(self):
    sp.transfer(sp.unit, sp.tez(0), sp.contract(sp.TUnit, self.data.lastPool, entrypoint='initializePool').open_some(message = 'INITIALIZE_FAIL'))

sp.add_compilation_target("test", Contract())