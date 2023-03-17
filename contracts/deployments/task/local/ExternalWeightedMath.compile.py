import smartpy as sp

from contracts.pool_weighted.ExternalWeightedMath import ExternalWeightedMath

{
    'name': 'Symmetric Weighted Math',
    'version': 'v1.0.0',
    'description': 'Weighted Math is designed to allow for swaps between any assets whether or not they have any price correlation. Prices are determined by the pool balances, pool weights, and amounts of the tokens that are being swapped.',
    'authors': ['Cent Finance'],
    'homepage': 'https://symmetric.exchange',
    'license': 'GPL-3.0',
    'interfaces': ['TZIP-016']
}

sp.add_compilation_target('local', ExternalWeightedMath())
