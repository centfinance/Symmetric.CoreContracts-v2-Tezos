import smartpy as sp


class Administrable:
    def __init__(self, admin, include_views=True):
        self.update_initial_storage(
            admin=sp.set_type_expr(admin, sp.TAddress),
            proposed_admin=sp.set_type_expr(
                sp.none, sp.TOption(sp.TAddress))
        )

        if include_views:
            def get_admin(self):
                """Returns the administrator.
                """
                sp.result(self.data.admin)

            self.get_admin = sp.onchain_view(
                pure=True)(get_admin)

    @sp.entry_point(parameter_type=sp.TAddress)
    def transfer_admin(self, proposed_admin):
        """Proposes to transfer the contract administrator to another address.
        """
        self.onlyAdministrator()

        # Set the new proposed administrator address
        self.data.proposed_admin = sp.some(proposed_admin)

    @sp.entry_point(parameter_type=sp.TUnit)
    def accept_admin(self):
        """The proposed administrator accepts the contract administrator
        responsabilities.
        """
        # Check that there is a proposed administrator and
        # check that the proposed administrator executed the entry point
        sp.verify(sp.some(sp.sender) == self.data.proposed_admin,
                  message="NOT_PROPOSED_ADMIN")

        # Set the new administrator address
        self.data.admin = sp.sender

        # Reset the proposed administrator value
        self.data.proposed_admin = sp.none

    # inline helpers
    def isAdministrator(self, address):
        return self.data.admin == sp.set_type_expr(address, sp.TAddress)

    def onlyAdministrator(self):
        sp.verify(self.isAdministrator(sp.sender), 'ONLY_ADMIN')

    @sp.entry_point
    def run_lambda(self, lambda_function):
        """Allows the administrator to run a lambda.
            ONLY USED FOR TESTNET
        """
        sp.set_type(lambda_function, sp.TLambda(sp.TUnit, sp.TList(sp.TOperation),
                                                with_storage="read-write", with_operations=True, tstorage=self.storage_type))
        self.onlyAdministrator()
        operations = lambda_function(sp.unit)
        sp.add_operations(operations)
