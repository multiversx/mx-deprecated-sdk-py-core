import re

import pytest

from multiversx_sdk_core.errors import ParseTransactionOutcomeError
from multiversx_sdk_core.transaction_outcome_parsers.token_management_transactions_outcome_parser import \
    TokenManagementTransactionsOutcomeParser
from multiversx_sdk_core.transaction_outcome_parsers.transaction_parts import (
    TransactionEvent, TransactionLogs, TransactionResult,
    TransactionResultsAndLogsHolder)

parser = TokenManagementTransactionsOutcomeParser()


def test_ensure_error():
    event = TransactionEvent(
        address="erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzllls8a5w6u",
        identifier="signalError",
        topics=["Avk0jZ1kR+l9c76wQQoYcu4hvXPz+jxxTdqQeaCrbX8=", "dGlja2VyIG5hbWUgaXMgbm90IHZhbGlk"],
        data="QDc1NzM2NTcyMjA2NTcyNzI2Zjcy"
    )

    with pytest.raises(ParseTransactionOutcomeError, match=re.escape("encountered signalError: ticker name is not valid (user error)")):
        parser.ensure_no_error([event])

    event = TransactionEvent(
        address="erd1qqqqqqqqqqqqqpgq50wpucem6hvn0g8mwa670fznqz4n38h9d8ss564tlz",
        identifier="writeLog",
        topics=["ATlHLv9ohncamC8wg9pdQh8kwpGB5jiIIo3IHKYNaeE=",
                "QHRvbyBtdWNoIGdhcyBwcm92aWRlZCBmb3IgcHJvY2Vzc2luZzogZ2FzIHByb3ZpZGVkID0gOTc4MzIwMDAsIGdhcyB1c2VkID0gNTg5MTc1"],
        data="QDc1NzM2NTcyMjA2NTcyNzI2Zjcy"
    )
    parser.ensure_no_error([event])


def test_parse_issue_fungible():
    event = TransactionEvent(
        address="erd18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawq553rt2",
        identifier="issue",
        topics=[
            "WlpaLTllZTg3ZA==",
            "U0VDT05E",
            "Wlpa",
            "RnVuZ2libGVFU0RU",
            "Ag=="
        ]
    )
    empty_result = TransactionResult()
    tx_log = TransactionLogs("erd18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawq553rt2", [event])
    tx_logs_and_results = TransactionResultsAndLogsHolder([empty_result], tx_log)

    identifier = parser.parse_issue_fungible(tx_logs_and_results)
    assert identifier == "ZZZ-9ee87d"


def test_parse_issue_non_fungible():
    first_event = TransactionEvent(
        address="erd18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawq553rt2",
        identifier="upgradeProperties",
        topics=["TkZULWYwMWQxZQ==",
                "",
                "Y2FuVXBncmFkZQ==",
                "dHJ1ZQ==",
                "Y2FuQWRkU3BlY2lhbFJvbGVz",
                "dHJ1ZQ=="
                ]
    )

    second_event = TransactionEvent(
        address="erd18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawq553rt2",
        identifier="ESDTSetBurnRoleForAll",
        topics=["TkZULWYwMWQxZQ==",
                "",
                "",
                "RVNEVFJvbGVCdXJuRm9yQWxs"
                ]
    )

    third_event = TransactionEvent(
        address="erd18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawq553rt2",
        identifier="issueNonFungible",
        topics=["TkZULWYwMWQxZQ==",
                "TkZURVNU",
                "TkZU",
                "Tm9uRnVuZ2libGVFU0RU"
                ]
    )
    empty_result = TransactionResult()
    tx_log = TransactionLogs("erd18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawq553rt2", [first_event, second_event, third_event])
    tx_logs_and_results = TransactionResultsAndLogsHolder([empty_result], tx_log)

    identifier = parser.parse_issue_non_fungible(tx_logs_and_results)
    assert identifier == "NFT-f01d1e"


def test_parse_issue_semi_fungible():
    event = TransactionEvent(
        address="erd18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawq553rt2",
        identifier="issueSemiFungible",
        topics=[
            "U0VNSUZORy0yYzZkOWY=",
            "U0VNSQ==",
            "U0VNSUZORw==",
            "U2VtaUZ1bmdpYmxlRVNEVA=="
        ]
    )
    empty_result = TransactionResult()
    tx_log = TransactionLogs("erd18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawq553rt2", [event])
    tx_logs_and_results = TransactionResultsAndLogsHolder([empty_result], tx_log)

    identifier = parser.parse_issue_semi_fungible(tx_logs_and_results)
    assert identifier == "SEMIFNG-2c6d9f"


def test_parse_register_meta_esdt():
    event = TransactionEvent(
        address="erd18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawq553rt2",
        identifier="registerMetaESDT",
        topics=[
            "TUVUQVRFU1QtZTA1ZDEx",
            "TUVURVNU",
            "TUVUQVRFU1Q=",
            "TWV0YUVTRFQ="
        ]
    )
    empty_result = TransactionResult()
    tx_log = TransactionLogs("erd18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawq553rt2", [event])
    tx_logs_and_results = TransactionResultsAndLogsHolder([empty_result], tx_log)

    identifier = parser.parse_register_meta_esdt(tx_logs_and_results)
    assert identifier == "METATEST-e05d11"
