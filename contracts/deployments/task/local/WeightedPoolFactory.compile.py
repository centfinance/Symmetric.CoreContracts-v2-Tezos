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
    vault=sp.address('KT1NoUZuy55cRNwRGmJBTynMZgQUmU5gWSyv'),
    weightedMathLib=sp.address('KT1AtEf9dYqnojQaJWoHFEeMdZC3AWcwq5Hs'),
    weightedProtocolFeesLib=sp.address('KT1CwBKMkyivjqSs7MPmCn5k7UZnGDNPFfi5'),
    protocolFeeProvider=sp.address('KT1FaEfHMLoEeub55qT4P4g8ELtPggCgZwea'),
    metadata=CONTRACT_METADATA,
)

sp.add_compilation_target('local', WeightedPoolFactory(
    sp.address('tz1UGWQQ5YFkZqWgE3gqmPyuwy2R5VGpMM9B'),
    sp.address('KT1NoUZuy55cRNwRGmJBTynMZgQUmU5gWSyv'),
    sp.address('KT1AtEf9dYqnojQaJWoHFEeMdZC3AWcwq5Hs'),
    sp.address('KT1CwBKMkyivjqSs7MPmCn5k7UZnGDNPFfi5'),
    sp.address('KT1FaEfHMLoEeub55qT4P4g8ELtPggCgZwea'),
    CONTRACT_METADATA,
))
