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
    admin=sp.address('tz1UGWQQ5YFkZqWgE3gqmPyuwy2R5VGpMM9B'),
    vault=sp.address('KT1DSsMYr3n7C1ecYSgZimtFkDXdEQbxULFw'),
    weightedMathLib=sp.address('KT1TSNcEvQhX5wQyThfvVXzRaCbno5bkkUPs'),
    weightedProtocolFeesLib=sp.address('KT1VRdB2qWdGoj2ansGAsyDAFwVyerEAHGUg'),
    protocolFeeProvider=sp.address('KT1Tj18uGzc2HL3nNpFQaEPe7awMM88M3R7V'),
    metadata=CONTRACT_METADATA,
)

sp.add_compilation_target('local', WeightedPoolFactory(
    sp.address('tz1UGWQQ5YFkZqWgE3gqmPyuwy2R5VGpMM9B'),
    sp.address('KT1DSsMYr3n7C1ecYSgZimtFkDXdEQbxULFw'),
    sp.address('KT1TSNcEvQhX5wQyThfvVXzRaCbno5bkkUPs'),
    sp.address('KT1VRdB2qWdGoj2ansGAsyDAFwVyerEAHGUg'),
    sp.address('KT1Tj18uGzc2HL3nNpFQaEPe7awMM88M3R7V'),
    (sp.nat(400000000000000000), sp.nat(400000000000000000)),
    CONTRACT_METADATA,
))
