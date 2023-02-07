import smartpy as sp


class WeightedPool(
    sp.contract,
):

    def __init__(self, params):
        self.init(params)

    @sp.entry_point(private=True)
    def dummy_entry_point(self):
        pass
