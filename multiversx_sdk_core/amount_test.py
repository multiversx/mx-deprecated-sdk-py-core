
from decimal import Decimal

from multiversx_sdk_core.amount import Amount


def test_convert_between_units():
    assert Amount.from_main_unit(Decimal("1"), 18).to_atomic_unit() == 1000000000000000000
    assert Amount.from_main_unit(Decimal("10"), 18).to_atomic_unit() == 10000000000000000000
    assert Amount.from_main_unit(Decimal("100"), 18).to_atomic_unit() == 100000000000000000000
    assert Amount.from_main_unit(Decimal("1000"), 18).to_atomic_unit() == 1000000000000000000000

    assert Amount.from_main_unit(Decimal("0.1"), 18).to_atomic_unit() == 100000000000000000
    assert Amount.from_main_unit(Decimal("0.123456789"), 18).to_atomic_unit() == 123456789000000000
    assert Amount.from_main_unit(Decimal("0.123456789123456789"), 18).to_atomic_unit() == 123456789123456789
    assert Amount.from_main_unit(Decimal("0.123456789123456789777"), 18).to_atomic_unit() == 123456789123456789
    assert Amount.from_main_unit(Decimal("0.123456789123456789777777888888"), 18).to_atomic_unit() == 123456789123456789

    assert Amount.from_main_unit(Decimal("1"), 18).to_main_unit() == "1.000000000000000000"
    assert Amount.from_main_unit(Decimal("10"), 18).to_main_unit() == "10.000000000000000000"
    assert Amount.from_main_unit(Decimal("100"), 18).to_main_unit() == "100.000000000000000000"
    assert Amount.from_main_unit(Decimal("1000"), 18).to_main_unit() == "1000.000000000000000000"
    assert Amount.from_main_unit(Decimal("0.1"), 18).to_main_unit() == "0.100000000000000000"
    assert Amount.from_main_unit(Decimal("0.123456789"), 18).to_main_unit() == "0.123456789000000000"
    assert Amount.from_main_unit(Decimal("0.123456789123456789"), 18).to_main_unit() == "0.123456789123456789"
    assert Amount.from_main_unit(Decimal("0.123456789123456789777"), 18).to_main_unit() == "0.123456789123456789"
    assert Amount.from_main_unit(Decimal("0.123456789123456789777777888888"), 18).to_main_unit() == "0.123456789123456789"

    assert Amount.from_main_unit(Decimal("100"), 18).to_main_unit(normalize=True) == "100"
    assert Amount.from_main_unit(Decimal("1000"), 18).to_main_unit(normalize=True) == "1000"
