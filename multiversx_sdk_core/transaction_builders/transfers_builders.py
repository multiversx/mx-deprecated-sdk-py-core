from typing import List, Optional, Protocol, Sequence

from multiversx_sdk_core.interfaces import (IAddress, IGasLimit, IGasPrice,
                                            INonce, ITokenTransfer,
                                            ITransactionValue)
from multiversx_sdk_core.serializer import arg_to_string
from multiversx_sdk_core.transaction_builders.transaction_builder import (
    ITransactionBuilderConfiguration, TransactionBuilder)


class IESDTTransferConfiguration(ITransactionBuilderConfiguration, Protocol):
    gas_limit_esdt_transfer: IGasLimit
    additional_gas_for_esdt_transfer: IGasLimit


class IESDTNFTTransferConfiguration(ITransactionBuilderConfiguration, Protocol):
    gas_limit_esdt_nft_transfer: IGasLimit
    additional_gas_for_esdt_nft_transfer: IGasLimit


class EGLDTransferBuilder(TransactionBuilder):
    def __init__(self,
                 config: ITransactionBuilderConfiguration,
                 sender: IAddress,
                 receiver: IAddress,
                 transfer: ITokenTransfer,
                 nonce: Optional[INonce] = None,
                 data: Optional[str] = None,
                 gas_limit: Optional[IGasLimit] = None,
                 gas_price: Optional[IGasPrice] = None
                 ) -> None:
        assert transfer.is_egld()
        super().__init__(config, nonce, transfer.amount_in_atomic_unit, gas_limit, gas_price)
        self.sender = sender
        self.receiver = receiver
        self.data = data

    def _estimate_execution_gas(self) -> IGasLimit:
        return 0

    def _build_payload_parts(self) -> List[str]:
        return [self.data] if self.data else []


class ESDTTransferBuilder(TransactionBuilder):
    def __init__(self,
                 config: IESDTTransferConfiguration,
                 sender: IAddress,
                 receiver: IAddress,
                 transfer: ITokenTransfer,
                 nonce: Optional[INonce] = None,
                 value: Optional[ITransactionValue] = None,
                 gas_limit: Optional[IGasLimit] = None,
                 gas_price: Optional[IGasPrice] = None
                 ) -> None:
        super().__init__(config, nonce, value, gas_limit, gas_price)
        self.gas_limit_esdt_transfer = config.gas_limit_esdt_transfer
        self.additional_gas_for_esdt_transfer = config.additional_gas_for_esdt_transfer

        self.sender = sender
        self.receiver = receiver
        self.transfer = transfer

    def _estimate_execution_gas(self) -> IGasLimit:
        return self.gas_limit_esdt_transfer + self.additional_gas_for_esdt_transfer

    def _build_payload_parts(self) -> List[str]:
        return [
            "ESDTTransfer",
            arg_to_string(self.transfer.token_identifier),
            arg_to_string(self.transfer.amount_in_atomic_unit)
        ]


class ESDTNFTTransferBuilder(TransactionBuilder):
    def __init__(self,
                 config: IESDTNFTTransferConfiguration,
                 sender: IAddress,
                 destination: IAddress,
                 transfer: ITokenTransfer,
                 nonce: Optional[INonce] = None,
                 value: Optional[ITransactionValue] = None,
                 gas_limit: Optional[IGasLimit] = None,
                 gas_price: Optional[IGasPrice] = None
                 ) -> None:
        super().__init__(config, nonce, value, gas_limit, gas_price)
        self.gas_limit_esdt_nft_transfer = config.gas_limit_esdt_nft_transfer
        self.additional_gas_for_esdt_nft_transfer = config.additional_gas_for_esdt_nft_transfer

        self.sender = sender
        self.receiver = sender
        self.destination = destination
        self.transfer = transfer

    def _estimate_execution_gas(self) -> IGasLimit:
        return self.gas_limit_esdt_nft_transfer + self.additional_gas_for_esdt_nft_transfer

    def _build_payload_parts(self) -> List[str]:
        return [
            "ESDTNFTTransfer",
            arg_to_string(self.transfer.token_identifier),
            arg_to_string(self.transfer.token_nonce),
            arg_to_string(self.transfer.amount_in_atomic_unit),
            arg_to_string(self.destination)
        ]


class MultiESDTNFTTransferBuilder(TransactionBuilder):
    def __init__(self,
                 config: IESDTNFTTransferConfiguration,
                 sender: IAddress,
                 destination: IAddress,
                 transfers: Sequence[ITokenTransfer],
                 nonce: Optional[INonce] = None,
                 value: Optional[ITransactionValue] = None,
                 gas_limit: Optional[IGasLimit] = None,
                 gas_price: Optional[IGasPrice] = None
                 ) -> None:
        super().__init__(config, nonce, value, gas_limit, gas_price)
        self.gas_limit_esdt_nft_transfer = config.gas_limit_esdt_nft_transfer
        self.additional_gas_for_esdt_nft_transfer = config.additional_gas_for_esdt_nft_transfer

        self.sender = sender
        self.receiver = sender
        self.destination = destination
        self.transfers = transfers

    def _estimate_execution_gas(self) -> IGasLimit:
        return (self.gas_limit_esdt_nft_transfer + self.additional_gas_for_esdt_nft_transfer) * len(self.transfers)

    def _build_payload_parts(self) -> List[str]:
        parts = [
            "MultiESDTNFTTransfer",
            arg_to_string(self.destination),
            arg_to_string(len(self.transfers))
        ]

        for transfer in self.transfers:
            parts.extend([
                arg_to_string(transfer.token_identifier),
                arg_to_string(transfer.token_nonce),
                arg_to_string(transfer.amount_in_atomic_unit)
            ])

        return parts
