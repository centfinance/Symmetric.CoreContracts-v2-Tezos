import smartpy as sp

import contracts.pool_utils.SymmetricPoolToken as SymmetricPoolToken


class MockSymmetricPoolToken(SymmetricPoolToken):
    def __init__(self, name, symbol, vault):
        SymmetricPoolToken.__init__(self, name, symbol, vault)

    def mint(self, recipient, amount):
        self._mintPooltokens(self, recipient, amount)

    def burn(self, sender, amount):
        self._burnPoolTokens(self, sender, amount)


class Viewer(sp.Contract):
    def __init__(self, t):
        self.init(last=sp.none)
        self.init_type(sp.TRecord(last=sp.TOption(t)))

    @sp.entry_point
    def target(self, params):
        self.data.last = sp.some(params)


@sp.add_test(name="Default Smartpy test suite")
def test():
    sc = sp.test_scenario()
    sc.h1("FA1.2 template - Fungible assets")

    sc.table_of_contents()

    # sp.test_account generates ED25519 key-pairs deterministically:
    admin = sp.test_account("Administrator")
    alice = sp.test_account("Alice")
    bob = sp.test_account("Robert")

    # Let's display the accounts:
    sc.h1("Accounts")
    sc.show([admin, alice, bob])
    sc.h1("Contract")
    c1 = MockSymmetricPoolToken(admin.address)

    sc.h1("Entry points")
    sc += c1
    sc += c1.mint(address=alice.address, value=3).run(sender=admin)
    sc += c1.mint(address=alice.address, value=3).run(sender=admin)
    sc.h2("Alice transfers to Bob")
    sc += c1.transfer(from_=alice.address,
                      to_=bob.address, value=4).run(sender=alice)
    sc.verify(c1.data.balances[alice.address].balance == 14)
    sc.h2("Bob tries to transfer from Alice but he doesn't have her approval")
    sc += c1.transfer(from_=alice.address, to_=bob.address,
                      value=4).run(sender=bob, valid=False)
    sc += c1.approve(spender=bob.address, value=5).run(sender=alice)
    sc += c1.transfer(from_=alice.address,
                      to_=bob.address, value=4).run(sender=bob)
    sc.h2("Bob tries to over-transfer from Alice")
    sc += c1.transfer(from_=alice.address, to_=bob.address,
                      value=4).run(sender=bob, valid=False)
    sc.verify(c1.data.balances[alice.address].balance == 10)
    sc += c1.transfer(from_=alice.address,
                      to_=bob.address, value=1).run(sender=alice)
    sc.h2("Admin makes the alice the new administrator")
    sc += c1.setAdministrator(alice.address).run(sender=admin)
    sc.h2("Bob tries to change the admin")
    sc += c1.setAdministrator(
        bob.address).run(sender=bob, valid=False)

    sc.verify(c1.data.totalSupply == 18)
    sc.verify(c1.data.administrator == alice.address)
    sc.verify(c1.data.balances[alice.address].balance == 9)
    sc.verify(c1.data.balances[bob.address].balance == 9)

    sc.h1("Views")
    sc.h2("Balance")
    view_balance = Viewer(sp.TNat)
    sc += view_balance
    sc += c1.getBalance(
        (alice.address, view_balance.typed.target),
    )
    sc.verify_equal(view_balance.data.last, sp.some(9))

    sc.h2("Total Supply")
    view_totalSupply = Viewer(sp.TNat)
    sc += view_totalSupply
    sc += c1.getTotalSupply(
        (sp.unit, view_totalSupply.typed.target),
    )
    sc.verify_equal(view_totalSupply.data.last, sp.some(18))

    sc.h2("Allowance")
    view_allowance = Viewer(sp.TNat)
    sc += view_allowance
    sc += c1.getAllowance(
        (sp.record(owner=alice.address, spender=bob.address),
         view_allowance.typed.target),
    )
    sc.verify_equal(view_allowance.data.last, sp.some(1))

    ######################
    # CHANGED entrypoints
    ######################


@ sp.add_test(name="CHANGED entrypoints work correctly")
def test():
    sc = sp.test_scenorio()

    token = FA12(Addresses.ADMIN)

    sc += token

    # Add mint admins
    sc += token.addMintAdmin(
        Addresses.CONTRACT).run(sender=Addresses.ADMIN)

    # Mint admin mints 90_000_000 tokens
    sc += token.mint(address=Addresses.ALICE,
                     value=900_000_000 * DECIMALS).run(sender=Addresses.CONTRACT)

    # Mint admin mints 20_000_000 tokens (overshoots max supply, so value gets adjusted), txn fails
    sc += token.mint(address=Addresses.ALICE, value=200_000_000 * DECIMALS).run(
        sender=Addresses.CONTRACT,
        valid=False,
        exception=FA12_Error.MaxSupplyMinted,
    )

    # Remove mint admin
    sc += token.removeMintAdmin(
        Addresses.CONTRACT).run(sender=Addresses.ADMIN)

    # Removed mint admin tries to mint, txn fails
    sc += token.mint(address=Addresses.ALICE, value=10_000_000 * DECIMALS).run(
        sender=Addresses.CONTRACT,
        valid=False,
        exception=FA12_Error.NotAdmin,
    )

    sp.add_compilation_target("ply_fa12", FA12())
