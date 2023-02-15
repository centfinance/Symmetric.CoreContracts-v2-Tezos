import smartpy as sp


class Types:
    TOKEN = sp.TRecord(
        address=sp.TAddress,
        id=sp.TNat
    )

    ENTRY = sp.TRecord(
        key=TOKEN,
        vaulue=sp.TBytes
    )

    ENUMERABLE_MAP = sp.TRecord(
        length=sp.TNat,
        entries=sp.Tmap(sp.TNat, sp.TAddress),
        indexes=sp.TMap(TOKEN, sp.TNat)
    )
