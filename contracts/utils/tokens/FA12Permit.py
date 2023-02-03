import smartpy as sp


class FA12Permit:

    def __init__():
        pass

    @sp.entry_point
    def delete_permits(self, permit_keys):
        sp.set_type(permit_keys, sp.TList(sp.TPair(sp.TAddress, sp.TBytes)))
        effective_expiry = sp.local("effective_expiry", 0)
        with sp.for_('permit_key' in permit_keys) as permit_key:
            permit_exists = self.data.permits.contains(permit_key)
            sp.verify(permit_exists, sp.pair(
                "NO_PERMIT_TO_DELETE", permit_key))
            effective_expiry = self.getEffectiveExpiry(permit_key)
            permit_submission_timestamp = self.data.permits[permit_key]
            sp.verify(sp.as_nat(sp.now - permit_submission_timestamp) >= effective_expiry,
                      sp.pair("PERMIT_NOT_EXPIRED", permit_key))
            self.delete_permit(permit_key)

    def delete_permit(self, permit_key):
        sp.set_type(permit_key, sp.TPair(sp.TAddress, sp.TBytes))
        with sp.if_(self.data.permits.contains(permit_key)):
            del self.data.permits[permit_key]
        with sp.if_(self.data.permit_expiries.contains(permit_key)):
            del self.data.permit_expiries[permit_key]

    @ sp.sub_entry_point
    def transfer_presigned(self, params):
        sp.set_type(params, sp.TRecord(
            from_=sp.TAddress, to_=sp.TAddress, value=sp.TNat))
        params_hash = sp.blake2b(sp.pack(params))
        # unsigned = sp.blake2b(mi.operator("SELF; ADDRESS; CHAIN_ID; PAIR; PAIR; PACK", [sp.TPair(sp.TNat, sp.TBytes)], [sp.TBytes])(sp.pair(self.data.counter, params_hash)))
        permit_key = sp.pair(params.from_, params_hash)
        effective_expiry = sp.local("effective_expiry", 0)
        with sp.if_(self.data.permits.contains(permit_key)):
            permit_submission_timestamp = self.data.permits[permit_key]
            with sp.if_(self.data.permit_expiries.contains(permit_key) & self.data.permit_expiries[permit_key].is_some()):
                effective_expiry.value = self.data.permit_expiries[permit_key].open_some(
                )
            with sp.else_():
                with sp.if_(self.data.user_expiries.contains(params.from_) & self.data.user_expiries[params.from_].is_some()):
                    effective_expiry.value = self.data.user_expiries[params.from_].open_some(
                    )
                with sp.else_():
                    effective_expiry.value = self.data.default_expiry
            # Deleting permit regardless of whether or not its expired
            with sp.if_(sp.as_nat(sp.now - permit_submission_timestamp) >= effective_expiry.value):
                # Expired
                self.delete_permit(permit_key)
                sp.result(sp.bool(False))
            with sp.else_():
                self.delete_permit(permit_key)
                sp.result(sp.bool(True))
        with sp.else_():
            sp.result(sp.bool(False))

    @sp.entry_point
    def permit(self, params):
        sp.set_type(params, sp.TList(
            sp.TPair(sp.TKey, sp.TPair(sp.TSignature, sp.TBytes))))
        with sp.for_('permit' in params) as permit:
            params_hash = sp.snd(sp.snd(permit))
            unsigned = sp.pack(sp.pair(sp.pair(sp.chain_id, sp.self_address), sp.pair(
                self.data.counter, params_hash)))
            pk_address = sp.to_address(
                sp.implicit_account(sp.hash_key(sp.fst(permit))))
            permit_key = sp.pair(pk_address, params_hash)
            permit_exists = self.data.permits.contains(permit_key)
            effective_expiry = self.getEffectiveExpiry(
                sp.pair(pk_address, params_hash))
            permit_submission_timestamp = self.data.permits[permit_key]
            sp.verify(~ (permit_exists & (sp.as_nat(sp.now - permit_submission_timestamp) < effective_expiry)),
                      sp.pair("DUP_PERMIT", params_hash))
            sp.verify(sp.check_signature(sp.fst(permit), sp.fst(
                sp.snd(permit)), unsigned), sp.pair("MISSIGNED", unsigned))
            self.data.permits[sp.pair(pk_address, params_hash)] = sp.now
            self.data.counter = self.data.counter + 1

    @sp.sub_entry_point
    def getEffectiveExpiry(self, params):
        sp.set_type(params, sp.TPair(sp.TAddress, sp.TBytes))
        address = sp.fst(params)
        with sp.if_(self.data.permit_expiries.contains(params) & self.data.permit_expiries[params].is_some()):
            permit_expiry = self.data.permit_expiries[params].open_some()
            sp.result(permit_expiry)
        with sp.else_():
            with sp.if_(self.data.user_expiries.contains(address) & self.data.user_expiries[address].is_some()):
                user_expiry = self.data.user_expiries[address].open_some()
                sp.result(user_expiry)
            with sp.else_():
                sp.result(self.data.default_expiry)

    @sp.entry_point
    def setExpiry(self, params):
        sp.set_type(params, sp.TRecord(address=sp.TAddress, seconds=sp.TNat, permit=sp.TOption(
            sp.TBytes))).layout(("address", ("seconds", "permit")))
        sp.verify(params.seconds <= self.data.max_expiry,
                  "MAX_SECONDS_EXCEEDED")
        sp.verify_equal(params.address, sp.sender, message="NOT_AUTHORIZED")
        with sp.if_(params.permit.is_some()):
            some_permit = params.permit.open_some()
            sp.verify(self.data.permits.contains(
                sp.pair(params.address, some_permit)), "PERMIT_NONEXISTENT")
            permit_submission_timestamp = self.data.permits[sp.pair(
                params.address, some_permit)]
            with sp.if_(self.data.permit_expiries.contains(sp.pair(params.address, some_permit)) & self.data.permit_expiries[sp.pair(params.address, some_permit)].is_some()):
                permit_expiry = self.data.permit_expiries[sp.pair(
                    params.address, some_permit)].open_some()
                sp.verify(sp.as_nat(sp.now - permit_submission_timestamp)
                          < permit_expiry, "PERMIT_REVOKED")
            with sp.else_():
                with sp.if_(self.data.user_expiries.contains(params.address) & self.data.user_expiries[params.address].is_some()):
                    user_expiry = self.data.user_expiries[params.address].open_some(
                    )
                    sp.verify(sp.as_nat(sp.now - permit_submission_timestamp)
                              < user_expiry, "PERMIT_REVOKED")
                with sp.else_():
                    sp.verify(sp.as_nat(sp.now - permit_submission_timestamp)
                              < self.data.default_expiry, "PERMIT_REVOKED")
            self.data.permit_expiries[sp.pair(
                params.address, some_permit)] = sp.some(params.seconds)
            self.data.user_expiries[params.address] = sp.some(params.seconds)

    @sp.onchain_view()
    def getCounter(self):
        sp.result(self.data.counter)

    @sp.onchain_view()
    def getDefaultExpiry(self):
        sp.result(self.data.default_expiry)
