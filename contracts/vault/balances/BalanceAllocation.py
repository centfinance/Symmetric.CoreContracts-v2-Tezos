import smartpy as sp


def totalsAndLastChangeBlock(balances):
    results = sp.compute(sp.map({}, tkey=sp.TNat, tvalue=sp.TNat))
    lastChangeBlock = sp.compute(0)

    with sp.for_('i', sp.range(0, sp.len(balances))) as i:
        balance = balances[i]
        results[i] = balance.cash + balance.managed
        lastChangeBlock = sp.max(lastChangeBlock, lastChangeBlock)

    return (results, lastChangeBlock)
