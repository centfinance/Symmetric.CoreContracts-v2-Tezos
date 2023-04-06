import smartpy as sp

from contracts.pool_weighted.ExternalWeightedProtocolFees import ExternalWeightedProtocolFees


sp.add_compilation_target('local', ExternalWeightedProtocolFees())
