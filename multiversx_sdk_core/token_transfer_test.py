
from multiversx_sdk_core.token_transfer import TokenTransfer


def test_of_egld():
    transfer = TokenTransfer.of_egld(123456789123456789)
    assert transfer.amount_in_atomic_unit == 123456789123456789
    assert transfer.token_nonce == 0
    assert transfer.token_identifier == "EGLD"


def test_of_fungible_esdt():
    transfer = TokenTransfer.of_fungible("USDC-c76f1f", 1000000)
    assert transfer.amount_in_atomic_unit == 1000000
    assert transfer.token_nonce == 0
    assert transfer.token_identifier == "USDC-c76f1f"


def test_of_meta_esdt():
    transfer = TokenTransfer.of_meta_esdt("MEXFARML-28d646", 12345678, 100000000000000000)
    assert transfer.amount_in_atomic_unit == 100000000000000000
    assert transfer.token_nonce == 12345678
    assert transfer.token_identifier == "MEXFARML-28d646"


def test_of_semi_fungible():
    transfer = TokenTransfer.of_semi_fungible("TEST-abf250", 3, 300)
    assert transfer.amount_in_atomic_unit == 300
    assert transfer.token_nonce == 3
    assert transfer.token_identifier == "TEST-abf250"


def test_of_non_fungible():
    transfer = TokenTransfer.of_non_fungible("TEST-38f249", 7)
    assert transfer.amount_in_atomic_unit == 1
    assert transfer.token_nonce == 7
    assert transfer.token_identifier == "TEST-38f249"
