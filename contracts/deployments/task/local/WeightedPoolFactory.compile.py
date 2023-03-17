import smartpy as sp

from contracts.pool_weighted.WeightedPoolFactory import WeightedPoolFactory

CONTRACT_STORAGE = sp.record(
    vault=sp.address('KT1SVwK8Uu4AgSpBrEqrSQczJeRQCCTXSXw7'),
    weightedMathlib=sp.address('KT1XrNpj8TBdpfMmjF2wod6yZisAzm6c3TCY'),
    protocolFeeProvider=sp.address('KT1VqarPDicMFn1ejmQqqshUkUXTCTXwmkCN'),
)

sp.add_compilation_target('local', WeightedPoolFactory(
    sp.address('KT1SVwK8Uu4AgSpBrEqrSQczJeRQCCTXSXw7'),
    sp.address('KT1XrNpj8TBdpfMmjF2wod6yZisAzm6c3TCY'),
    sp.address('KT1SJtRC6xTfrrhx2ys1bkR3BSCrLNHrmHpy'),
))
