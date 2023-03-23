
from decimal import ROUND_DOWN, Context, Decimal, localcontext
from typing import Optional, Union

from multiversx_sdk_core import typecheck


class Amount:
    def __init__(self, amount_in_atomic_unit: int, num_decimals: Optional[int] = None) -> None:
        typecheck.assert_is_integer(amount_in_atomic_unit, "in_atomic_unit must be an integer")

        self.in_atomic_unit = amount_in_atomic_unit
        self.num_decimals = num_decimals

    @classmethod
    def from_main_unit(cls, amount: Union[Decimal, str, int], num_decimals: int) -> 'Amount':
        amount_in_atomic_unit = convert_from_main_unit_to_atomic_unit(amount, num_decimals)
        return cls(amount_in_atomic_unit, num_decimals)

    @classmethod
    def from_atomic_unit(cls, amount: int, num_decimals: Optional[int] = None) -> 'Amount':
        return cls(amount, num_decimals)

    def to_main_unit(self, normalize: bool = False) -> str:
        if self.num_decimals is None:
            raise ValueError("cannot convert to main unit without knowing num_decimals")

        return convert_from_atomic_unit_to_main_unit(self.in_atomic_unit, self.num_decimals, normalize)

    def to_atomic_unit(self) -> int:
        return self.in_atomic_unit

    def __str__(self) -> str:
        return str(self.in_atomic_unit)

    def __repr__(self) -> str:
        return str(self.in_atomic_unit)


def convert_from_main_unit_to_atomic_unit(amount_in_main_unit: Union[Decimal, str, int], num_decimals: int) -> int:
    amount_in_main_unit = Decimal(amount_in_main_unit)

    with localcontext() as ctx:
        _adjust_decimal_context(ctx)
        amount_in_atomic_unit = int(amount_in_main_unit.scaleb(num_decimals))
        return amount_in_atomic_unit


def convert_from_atomic_unit_to_main_unit(amount_in_atomic_unit: int, num_decimals: int, normalize: bool = False) -> str:
    with localcontext() as ctx:
        _adjust_decimal_context(ctx)
        amount_in_main_unit = Decimal(amount_in_atomic_unit).scaleb(-num_decimals)

        if normalize:
            amount_in_main_unit = amount_in_main_unit.normalize()

        return f"{amount_in_main_unit:f}"


def _adjust_decimal_context(context: Context):
    context.prec = 128
    context.rounding = ROUND_DOWN
