import smartpy as sp

from contracts.pool_utils.BasePool import BasePool


class BaseWeightedPool(
    BasePool
):
    def __init__(
        self,
        vault,
        name,
        symbol,
        owner,
    ):
        BasePool.__init__(
            self,
            vault,
            name,
            symbol,
            owner,
        )
