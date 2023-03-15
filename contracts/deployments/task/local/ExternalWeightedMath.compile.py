import smartpy as sp

from contracts.pool_weighted.ExternalWeightedMath import ExternalWeightedMath

sp.add_compilation_target('local', ExternalWeightedMath())
