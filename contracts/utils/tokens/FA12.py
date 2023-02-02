# Fungible Assets - FA12
# Inspired by https://gitlab.com/tzip/tzip/blob/master/A/FA1.2.md

import smartpy as sp


class FA12_Error:
    def make(s):
        return "FA1.2_" + s

    NotAdmin = make("NotAdmin")
    NotEnoughBalance = make("NotEnoughBalance")
    UnsafeAllowanceChange = make("UnsafeAllowanceChange")
    NotEnoughAllowance = make("NotEnoughAllowance")
    MaxSupplyMinted = make("MaxSupplyMinted")
    TezSentToEntrypoint = make("TezSentToEntrypoint")


class FA12_common:
    def normalize_metadata(self, metadata):
        meta = {}
        for key in metadata:
            meta[key] = sp.utils.bytes_of_string(metadata[key])

        return meta


class FA12_core(sp.Contract, FA12_common):
    def __init__(self, **extra_storage):
        self.init(
            balances=sp.big_map(
                tvalue=sp.TRecord(approvals=sp.TMap(
                    sp.TAddress, sp.TNat), balance=sp.TNat),
            ),
            totalSupply=0,
            **extra_storage,
        )

    @sp.entry_point
    def transfer(self, params):
        sp.set_type(
            params,
            sp.TRecord(from_=sp.TAddress, to_=sp.TAddress, value=sp.TNat).layout(
                ("from_ as from", ("to_ as to", "value"))
            ),
        )
        sp.verify(
            (params.from_ == sp.sender)
            | self.is_allowed(params.from_, sp.sender, params.value),
            FA12_Error.NotEnoughAllowance,
        )

        # Reject tez
        sp.verify(sp.amount == sp.tez(0), FA12_Error.TezSentToEntrypoint)

        self.addAddressIfNecessary(params.from_)
        self.addAddressIfNecessary(params.to_)
        sp.verify(self.data.balances[params.from_].balance >=
                  params.value, FA12_Error.NotEnoughBalance)
        self.data.balances[params.from_].balance = sp.as_nat(
            self.data.balances[params.from_].balance - params.value)
        self.data.balances[params.to_].balance += params.value

        with sp.if_(params.from_ != sp.sender):
            self.data.balances[params.from_].approvals[sp.sender] = sp.as_nat(
                self.data.balances[params.from_].approvals[sp.sender] -
                params.value
            )

    @sp.entry_point
    def approve(self, params):
        sp.verify(sp.amount == sp.tez(0), FA12_Error.TezSentToEntrypoint)
        sp.set_type(params, sp.TRecord(spender=sp.TAddress,
                    value=sp.TNat).layout(("spender", "value")))
        self.addAddressIfNecessary(sp.sender)
        alreadyApproved = self.data.balances[sp.sender].approvals.get(
            params.spender, 0)
        sp.verify((alreadyApproved == 0) | (params.value == 0),
                  FA12_Error.UnsafeAllowanceChange)
        self.data.balances[sp.sender].approvals[params.spender] = params.value

    def addAddressIfNecessary(self, address):
        with sp.if_(~ self.data.balances.contains(address)):
            self.data.balances[address] = sp.record(balance=0, approvals={})

    def is_allowed(self, owner, spender, value):
        return (self.data.balances[owner].approvals.get(spender, 0) >= value)

    @sp.onchain_view()
    def getBalance(self, params):
        sp.set_type(params, sp.TAddress)
        with sp.if_(self.data.balances.contains(params)):
            sp.result(self.data.balances[params].balance)
        with sp.else_():
            sp.result(sp.nat(0))

    @sp.onchain_view()
    def getAllowance(self, params):
        sp.set_type(params, sp.TRecord(owner=sp.TAddress, spender=sp.TAddress))
        with sp.if_(self.data.balances.contains(params.owner)):
            sp.result(self.data.balances[params.owner].approvals.get(
                params.spender, 0))
        with sp.else_():
            sp.result(sp.nat(0))

    @sp.onchain_view()
    def getTotalSupply(self):
        sp.result(self.data.totalSupply)

    # this is not part of the standard but can be supported through inheritance.
    def is_paused(self):
        return sp.bool(False)

    # this is not part of the standard but can be supported through inheritance.
    def is_administrator(self, sender):
        return sp.bool(False)

    # this is not part of the standard but can be supported through inheritance.
    def _mint(self, params):
        sp.set_type(params, sp.TRecord(address=sp.TAddress, value=sp.TNat))
        self.addAddressIfNecessary(params.address)
        self.data.balances[params.address].balance += params.value
        self.data.totalSupply += params.value

    # this is not part of the standard but can be supported through inheritance.
    def _burn(self, params):
        sp.set_type(params, sp.TRecord(address=sp.TAddress, value=sp.TNat))
        sp.verify(self.data.balances[params.address].balance >= params.value)
        self.data.balances[params.address].balance = sp.as_nat(
            self.data.balances[params.address].balance - params.value)
        self.data.totalSupply = sp.as_nat(self.data.totalSupply - params.value)


class FA12_token_metadata(FA12_core):
    def set_token_metadata(self, metadata):
        self.update_initial_storage(
            token_metadata=sp.big_map(
                {0: sp.record(
                    token_id=0, token_info=self.normalize_metadata(metadata))},
                tkey=sp.TNat,
                tvalue=sp.TRecord(token_id=sp.TNat,
                                  token_info=sp.TMap(sp.TString, sp.TBytes)),
            )
        )


class FA12_contract_metadata(FA12_core):
    def set_contract_metadata(self, metadata):
        self.update_initial_storage(metadata=sp.big_map(
            self.normalize_metadata(metadata)))
