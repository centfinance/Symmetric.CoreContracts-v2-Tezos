import smartpy as sp

from contracts.pool_weighted.WeightedPoolFactory import WeightedPoolFactory

CONTRACT_STORAGE = sp.record(
    vault=sp.address('KT1N5Qpp5DaJzEgEXY1TW6Zne6Eehbxp83XF'),
    protocolFeeProvider=sp.address('KT1VqarPDicMFn1ejmQqqshUkUXTCTXwmkCN'),
)

sp.add_compilation_target('local', WeightedPoolFactory(CONTRACT_STORAGE))
