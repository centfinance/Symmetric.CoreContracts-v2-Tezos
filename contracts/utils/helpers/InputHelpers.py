import smartpy as sp

import contracts.interfaces.SymmetricErrors as Errors


def ensureInputLengthMatch(a, b):
    sp.verify(a == b, Errors.INPUT_LENGTH_MISMATCH)


def ensureInputLengthMatch(a, b, c):
    sp.verify(((a == b) & (b == c)), Errors.INPUT_LENGTH_MISMATCH)


def ensureListIsSorted(list):
    with sp.if_(sp.len(list) < 2):
        pass

    previous = sp.local('previous', list[0])
    with sp.for_('x' in list) as x:
        sp.verify(previous < x, Errors.UNSORTED_ARRAY)
        previous.value = x
