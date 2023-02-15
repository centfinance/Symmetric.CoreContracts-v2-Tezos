import smartpy as sp


def list_contains(lst, elem):
    contains = sp.local("contains", False)
    with sp.for_('e', lst) as e:
        with sp.if_(e == elem):
            contains.value = True
    return contains.value
