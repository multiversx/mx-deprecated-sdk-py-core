import base64
from typing import List

from multiversx_sdk_core.errors import ParseTransactionOutcomeError
from multiversx_sdk_core.transaction_outcome_parsers.interfaces import (
    ITransactionEvent, ITransactionResultsAndLogsHolder)
from multiversx_sdk_core.transaction_outcome_parsers.token_management_transactions_outcome_parsers_types import \
    RegisterAndSetAllRolesOutcome


class TokenManagementTransactionsOutcomeParser:
    def __init__(self) -> None:
        pass

    def parse_issue_fungible(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> str:
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

        event = self.find_single_event_by_identifier(transaction_results_and_logs, "issue")
        return self.extract_token_identifier(event)

    def parse_issue_non_fungible(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> str:
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

        event = self.find_single_event_by_identifier(transaction_results_and_logs, "issueNonFungible")
        return self.extract_token_identifier(event)

    def parse_issue_semi_fungible(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> str:
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

        event = self.find_single_event_by_identifier(transaction_results_and_logs, "issueSemiFungible")
        return self.extract_token_identifier(event)

    def parse_register_meta_esdt(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> str:
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

        event = self.find_single_event_by_identifier(transaction_results_and_logs, "registerMetaESDT")
        return self.extract_token_identifier(event)

    def parse_register_and_set_all_roles(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> RegisterAndSetAllRolesOutcome:
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

        register_event = self.find_single_event_by_identifier(transaction_results_and_logs, "registerAndSetAllRoles")
        token_identifier = self.extract_token_identifier(register_event)

        set_role_event = self.find_single_event_by_identifier(transaction_results_and_logs, "ESDTSetRole")
        encoded_roles = set_role_event.topics[3:]

        roles: List[str] = []
        for role in encoded_roles:
            hex_encoded_role = base64.b64decode(role).hex()
            roles.append(bytes.fromhex(hex_encoded_role).decode())

        return RegisterAndSetAllRolesOutcome(token_identifier, roles)

    def ensure_no_error(self, transaction_events: List[ITransactionEvent]) -> None:
        for event in transaction_events:
            if event.identifier == "signalError":
                hex_data = base64.b64decode(event.data or "").hex()
                data = bytes.fromhex(hex_data).decode()

                hex_message = base64.b64decode(event.topics[1] or "").hex()
                message = bytes.fromhex(hex_message).decode()

                raise ParseTransactionOutcomeError(f"encountered signalError: {message} ({bytes.fromhex(data[1:]).decode()})")

    def find_single_event_by_identifier(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder, identifier: str) -> ITransactionEvent:
        events = self.gather_all_events(transaction_results_and_logs)
        events_with_matching_id = [event for event in events if event.identifier == identifier]

        if len(events_with_matching_id) == 0:
            raise ParseTransactionOutcomeError(f"cannot find event of type {identifier}")

        if len(events_with_matching_id) > 1:
            raise ParseTransactionOutcomeError(f"found more than one event of type {identifier}")

        return events_with_matching_id[0]

    def gather_all_events(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> List[ITransactionEvent]:
        all_events = [*transaction_results_and_logs.transaction_logs.events]

        for result in transaction_results_and_logs.transaction_results:
            all_events.extend([*result.logs.events])

        return all_events

    def extract_token_identifier(self, event: ITransactionEvent) -> str:
        if event.topics[0]:
            hex_ticker = base64.b64decode(event.topics[0]).hex()
            return bytes.fromhex(hex_ticker).decode()
        return ""
