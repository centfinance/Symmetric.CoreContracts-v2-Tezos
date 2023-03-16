import smartpy as sp

from contracts.pool_weighted.WeightedPool import WeightedPool

CONTRACT_STORAGE = sp.record(
    vault=sp.address('KT1N5Qpp5DaJzEgEXY1TW6Zne6Eehbxp83XF'),
    name='Symmetric Pool Token',
    symbol='SYMMLP',
    weightedMathLib='KT1SJtRC6xTfrrhx2ys1bkR3BSCrLNHrmHpy'
)

sp.add_compilation_target('local', WeightedPool(
    sp.address('KT1N5Qpp5DaJzEgEXY1TW6Zne6Eehbxp83XF'),
    'Symmetric Pool Token',
    'SYMMLP',
    sp.address('KT1SJtRC6xTfrrhx2ys1bkR3BSCrLNHrmHpy'))
)
