import base64
from typing import List

from multiversx_sdk_core.address import Address
from multiversx_sdk_core.constants import DEFAULT_HRP
from multiversx_sdk_core.errors import ParseTransactionOutcomeError
from multiversx_sdk_core.transaction_outcome_parsers.interfaces import (
    ITransactionEvent, ITransactionResultsAndLogsHolder)
from multiversx_sdk_core.transaction_outcome_parsers.token_management_transactions_outcome_parsers_types import (
    AddQuantityOutcome, BurnOutcome, BurnQuantityOutcome, FreezeOutcome,
    MintOutcome, NFTCreateOutcome, RegisterAndSetAllRolesOutcome,
    SetSpecialRoleOutcome, UnFreezeOutcome, UpdateAttributesOutcome,
    WipeOutcome)


class TokenManagementTransactionsOutcomeParser:
    def __init__(self) -> None:
        pass

    def parse_issue_fungible(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> str:
        """Returns the identifier of the issued ESDT"""
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

        event = self.find_single_event_by_identifier(transaction_results_and_logs, "issue")
        return self.extract_token_identifier(event)

    def parse_issue_non_fungible(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> str:
        """Returns the identifier of the NFT collection"""
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

        event = self.find_single_event_by_identifier(transaction_results_and_logs, "issueNonFungible")
        return self.extract_token_identifier(event)

    def parse_issue_semi_fungible(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> str:
        """Returns the identifier of the SFT collection"""
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

        event = self.find_single_event_by_identifier(transaction_results_and_logs, "issueSemiFungible")
        return self.extract_token_identifier(event)

    def parse_register_meta_esdt(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> str:
        """Returns the identifier of the MetaESDT collection"""
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

    def parse_set_burn_role_globally(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> None:
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

    def parse_unset_burn_role_globally(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> None:
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

    def parse_set_special_role(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> SetSpecialRoleOutcome:
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

        event = self.find_single_event_by_identifier(transaction_results_and_logs, "ESDTSetRole")
        user_address = event.address
        token_identifier = self.extract_token_identifier(event)

        encoded_roles = event.topics[3:]
        roles: List[str] = []

        for role in encoded_roles:
            hex_encoded_role = base64.b64decode(role).hex()
            roles.append(bytes.fromhex(hex_encoded_role).decode())

        return SetSpecialRoleOutcome(user_address, token_identifier, roles)

    def parse_nft_create(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> NFTCreateOutcome:
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

        event = self.find_single_event_by_identifier(transaction_results_and_logs, "ESDTNFTCreate")
        token_identifier = self.extract_token_identifier(event)
        nonce = self.extract_nonce(event)
        amount = self.extract_amount(event)

        return NFTCreateOutcome(token_identifier, nonce, amount)

    def parse_local_mint(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> MintOutcome:
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

        event = self.find_single_event_by_identifier(transaction_results_and_logs, "ESDTLocalMint")
        user_address = event.address
        token_identifier = self.extract_token_identifier(event)
        nonce = self.extract_nonce(event)
        minted_supply = self.extract_amount(event)

        return MintOutcome(user_address, token_identifier, nonce, minted_supply)

    def parse_local_burn(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> BurnOutcome:
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

        event = self.find_single_event_by_identifier(transaction_results_and_logs, "ESDTLocalBurn")
        user_address = event.address
        token_identifier = self.extract_token_identifier(event)
        nonce = self.extract_nonce(event)
        burnt_supply = self.extract_amount(event)

        return BurnOutcome(user_address, token_identifier, nonce, burnt_supply)

    def parse_pause(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> str:
        """Returns the identifier of the paused token"""
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

        event = self.find_single_event_by_identifier(transaction_results_and_logs, "ESDTPause")
        return self.extract_token_identifier(event)

    def parse_unpause(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> str:
        """Returns the identifier of the unpaused token"""
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

        event = self.find_single_event_by_identifier(transaction_results_and_logs, "ESDTUnPause")
        return self.extract_token_identifier(event)

    def parse_freeze(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> FreezeOutcome:
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

        event = self.find_single_event_by_identifier(transaction_results_and_logs, "ESDTFreeze")
        user_address = self.extract_address(event)
        token_identifier = self.extract_token_identifier(event)
        nonce = self.extract_nonce(event)
        balance = self.extract_amount(event)

        return FreezeOutcome(user_address, token_identifier, nonce, balance)

    def parse_unfreeze(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> UnFreezeOutcome:
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

        event = self.find_single_event_by_identifier(transaction_results_and_logs, "ESDTUnFreeze")
        user_address = self.extract_address(event)
        token_identifier = self.extract_token_identifier(event)
        nonce = self.extract_nonce(event)
        balance = self.extract_amount(event)

        return UnFreezeOutcome(user_address, token_identifier, nonce, balance)

    def parse_wipe(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> WipeOutcome:
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

        event = self.find_single_event_by_identifier(transaction_results_and_logs, "ESDTWipe")
        user_address = self.extract_address(event)
        token_identifier = self.extract_token_identifier(event)
        nonce = self.extract_nonce(event)
        balance = self.extract_amount(event)

        return WipeOutcome(user_address, token_identifier, nonce, balance)

    def parse_update_attributes(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> UpdateAttributesOutcome:
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

        event = self.find_single_event_by_identifier(transaction_results_and_logs, "ESDTNFTUpdateAttributes")
        token_identifier = self.extract_token_identifier(event)
        nonce = self.extract_nonce(event)
        attributes = base64.b64decode(event.topics[3]) if event.topics[3] else b""

        return UpdateAttributesOutcome(token_identifier, nonce, attributes)

    def parse_add_quantity(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> AddQuantityOutcome:
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

        event = self.find_single_event_by_identifier(transaction_results_and_logs, "ESDTNFTAddQuantity")
        token_identifier = self.extract_token_identifier(event)
        nonce = self.extract_nonce(event)
        added_quantity = self.extract_amount(event)

        return AddQuantityOutcome(token_identifier, nonce, added_quantity)

    def parse_burn_quantity(self, transaction_results_and_logs: ITransactionResultsAndLogsHolder) -> BurnQuantityOutcome:
        self.ensure_no_error(transaction_results_and_logs.transaction_logs.events)

        event = self.find_single_event_by_identifier(transaction_results_and_logs, "ESDTNFTBurn")
        token_identifier = self.extract_token_identifier(event)
        nonce = self.extract_nonce(event)
        added_quantity = self.extract_amount(event)

        return BurnQuantityOutcome(token_identifier, nonce, added_quantity)

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

    def extract_nonce(self, event: ITransactionEvent) -> str:
        if event.topics[1]:
            hex_nonce = base64.b64decode(event.topics[1]).hex()
            return str(int(hex_nonce, 16))
        return ""

    def extract_amount(self, event: ITransactionEvent) -> str:
        if event.topics[2]:
            hex_amount = base64.b64decode(event.topics[2]).hex()
            return str(int(hex_amount, 16))
        return ""

    def extract_address(self, event: ITransactionEvent) -> str:
        if event.topics[3]:
            hex_address = base64.b64decode(event.topics[3]).hex()
            return Address.new_from_hex(hex_address, DEFAULT_HRP).to_bech32()
        return ""
