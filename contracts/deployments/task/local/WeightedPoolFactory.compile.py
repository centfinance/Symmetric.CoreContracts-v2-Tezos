import smartpy as sp

from contracts.pool_weighted.WeightedPoolFactory import WeightedPoolFactory

metdata = {
    'name': 'Symmetric Weighted Pool Factory',
    'version': 'v1.0.0',
    'description': 'Symmetric Weighted Pool Factory. Used for creating liquidity pools that swap tokens by enforcing a Constant Weighted Product invariant.',
    'authors': ['Cent Finance'],
    'homepage': 'https://symmetric.exchange',
    'license': 'GPL-3.0',
    'interfaces': ['TZIP-016']
}
CONTRACT_METADATA = {
    "": "https://raw.githubusercontent.com/centfinance/Symmetric.CoreContracts-v2-Tezos/main/metadata/testnet/WeightedPoolFactory.json",
}

CONTRACT_STORAGE = sp.record(
    vault=sp.address('KT1XV3C2twmrgVaHv2jNtUpymQZ39C6mM7Kp'),
    weightedMathlib=sp.address('KT1XrNpj8TBdpfMmjF2wod6yZisAzm6c3TCY'),
    protocolFeeProvider=sp.address('KT1VqarPDicMFn1ejmQqqshUkUXTCTXwmkCN'),
)

sp.add_compilation_target('local', WeightedPoolFactory(
    sp.address('KT1XV3C2twmrgVaHv2jNtUpymQZ39C6mM7Kp'),
    sp.address('KT1XrNpj8TBdpfMmjF2wod6yZisAzm6c3TCY'),
    sp.address('KT1SJtRC6xTfrrhx2ys1bkR3BSCrLNHrmHpy'),
    CONTRACT_METADATA,
))
