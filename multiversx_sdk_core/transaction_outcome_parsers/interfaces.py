from typing import List, Protocol


class ITransactionEvent(Protocol):
    address: str
    identifier: str
    topics: List[str]
    data: str


class ITransactionLogs(Protocol):
    address: str
    events: List[ITransactionEvent]


class ITransactionResult(Protocol):
    hash: str
    timestamp: int
    sender: str
    receiver: str
    data: str
    original_tx_hash: str
    miniblock_hash: str
    logs: ITransactionLogs


class ITransactionResultsAndLogsHolder(Protocol):
    transaction_results: List[ITransactionResult]
    transaction_logs: ITransactionLogs
