import smartpy as sp

from contracts.vault.ProtocolFeesCollector import ProtocolFeesCollector

sp.add_compilation_target('local', ProtocolFeesCollector(
    sp.address('KT1XV3C2twmrgVaHv2jNtUpymQZ39C6mM7Kp'),
    sp.address('tz1UGWQQ5YFkZqWgE3gqmPyuwy2R5VGpMM9B'),
))
