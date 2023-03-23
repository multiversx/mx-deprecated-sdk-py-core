from typing import Protocol


class IAddress(Protocol):
    def bech32(self) -> str: ...


INonce = int
IGasPrice = int
IGasLimit = int
IChainID = str
ITransactionVersion = int
ITransactionOptions = int
ISignature = bytes
ITokenIdentifier = str


class ITokenTransfer(Protocol):
    token_identifier: ITokenIdentifier
    token_nonce: INonce
    amount_in_atomic_unit: int

    def is_egld(self) -> bool: ...
    def is_fungible(self) -> bool: ...


class ITransactionValue(Protocol):
    def __str__(self) -> str: ...


class ITransactionPayload(Protocol):
    data: bytes
    def encoded(self) -> str: ...
    def length(self) -> int: ...


class ICodeMetadata(Protocol):
    def serialize(self) -> bytes: ...
