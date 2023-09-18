import smartpy as sp

tstorage = sp.TRecord(admin = sp.TAddress, feeCache = sp.TPair(sp.TNat, sp.TNat), isPoolFromFactory = sp.TBigMap(sp.TAddress, sp.TUnit), lastPool = sp.TAddress, metadata = sp.TBigMap(sp.TString, sp.TBytes), protocolFeeProvider = sp.TAddress, vault = sp.TAddress, weightedMathLib = sp.TAddress, weightedProtocolFeesLib = sp.TAddress).layout(((("admin", "feeCache"), ("isPoolFromFactory", "lastPool")), (("metadata", "protocolFeeProvider"), ("vault", ("weightedMathLib", "weightedProtocolFeesLib")))))
tparameter = sp.TVariant(create = sp.TRecord(metadata = sp.TBytes, normalizedWeights = sp.TMap(sp.TNat, sp.TNat), rateProviders = sp.TOption(sp.TMap(sp.TNat, sp.TOption(sp.TAddress))), swapFeePercentage = sp.TNat, tokenDecimals = sp.TMap(sp.TNat, sp.TNat), token_metadata = sp.TMap(sp.TString, sp.TBytes), tokens = sp.TMap(sp.TNat, sp.TPair(sp.TAddress, sp.TOption(sp.TNat)))).layout((("metadata", ("normalizedWeights", "rateProviders")), (("swapFeePercentage", "tokenDecimals"), ("token_metadata", "tokens")))), initialize = sp.TUnit).layout(("create", "initialize"))
tprivates = { }
tviews = { }
