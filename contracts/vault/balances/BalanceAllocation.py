import smartpy as sp

def totals(balances):
    # helper for getting a map total balances
    results = sp.compute(sp.map({}, tkey=sp.TNat, tvalue=sp.TNat))

    with sp.for_('i', sp.range(0, sp.len(balances))) as i:
        balance = balances[i]
        results[i] = sp.fst(balance) + sp.snd(balance)

    return results


def toBalance(cash, managed):
    return sp.pair(cash, managed)
