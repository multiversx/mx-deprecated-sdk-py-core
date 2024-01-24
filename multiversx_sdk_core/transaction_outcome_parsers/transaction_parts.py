from typing import List

from multiversx_sdk_core.transaction_outcome_parsers.interfaces import (
    ITransactionEvent, ITransactionLogs, ITransactionResult)


class TransactionEvent:
    def __init__(self,
                 address: str = "",
                 identifier: str = "",
                 topics: List[str] = [],
                 data: str = "") -> None:
        self.address = address
        self.identifier = identifier
        self.topics = topics
        self.data = data


class TransactionLogs:
    def __init__(self,
                 address: str = "",
                 events: List[ITransactionEvent] = []) -> None:
        self.address = address
        self.events = events


class TransactionResult:
    def __init__(self,
                 hash: str = "",
                 timestamp: int = 0,
                 sender: str = "",
                 receiver: str = "",
                 data: str = "",
                 original_tx_hash: str = "",
                 miniblock_hash: str = "",
                 logs: ITransactionLogs = TransactionLogs()) -> None:
        self.hash = hash
        self.timestamp = timestamp
        self.sender = sender
        self.receiver = receiver
        self.data = data
        self.original_tx_hash = original_tx_hash
        self.miniblock_hash = miniblock_hash
        self.logs = logs


class TransactionResultsAndLogsHolder:
    def __init__(self,
                 transaction_results: List[ITransactionResult],
                 transaction_logs: ITransactionLogs) -> None:
        self.transaction_results = transaction_results
        self.transaction_logs = transaction_logs
