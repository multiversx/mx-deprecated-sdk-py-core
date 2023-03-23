from multiversx_sdk_core import typecheck
from multiversx_sdk_core.constants import EGLD_TOKEN_IDENTIFIER
from multiversx_sdk_core.interfaces import INonce, ITokenIdentifier


class TokenTransfer:
    def __init__(self, token_identifier: ITokenIdentifier, token_nonce: INonce, amount_in_atomic_unit: int) -> None:
        typecheck.assert_is_integer(amount_in_atomic_unit, "amount_in_atomic_unit must be an integer")

        self.token_identifier: ITokenIdentifier = token_identifier
        self.token_nonce: INonce = token_nonce
        self.amount_in_atomic_unit: int = amount_in_atomic_unit

    def is_egld(self):
        return self.token_identifier == EGLD_TOKEN_IDENTIFIER

    def is_fungible(self):
        return self.token_nonce == 0

    @classmethod
    def of_egld(cls, amount_in_atomic_unit: int) -> 'TokenTransfer':
        return cls(EGLD_TOKEN_IDENTIFIER, 0, amount_in_atomic_unit)

    @classmethod
    def of_fungible(cls, token_identifier: ITokenIdentifier, amount_in_atomic_unit: int) -> 'TokenTransfer':
        return cls(token_identifier, 0, amount_in_atomic_unit)

    @classmethod
    def of_non_fungible(cls, token_identifier: ITokenIdentifier, nonce: INonce) -> 'TokenTransfer':
        return cls(token_identifier, nonce, 1)

    @classmethod
    def of_semi_fungible(cls, token_identifier: ITokenIdentifier, nonce: INonce, quantity: int) -> 'TokenTransfer':
        return cls(token_identifier, nonce, quantity)

    @classmethod
    def of_meta_esdt(cls, token_identifier: ITokenIdentifier, nonce: int, amount_in_atomic_unit: int) -> 'TokenTransfer':
        return cls(token_identifier, nonce, amount_in_atomic_unit)

    def __str__(self) -> str:
        return str(self.amount_in_atomic_unit)

    def __repr__(self) -> str:
        return str(self.amount_in_atomic_unit)
