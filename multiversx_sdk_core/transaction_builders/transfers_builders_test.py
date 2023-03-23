
from multiversx_sdk_core.address import Address
from multiversx_sdk_core.token_transfer import TokenTransfer
from multiversx_sdk_core.transaction_builders.default_configuration import \
    DefaultTransactionBuildersConfiguration
from multiversx_sdk_core.transaction_builders.transfers_builders import (
    EGLDTransferBuilder, ESDTNFTTransferBuilder, ESDTTransferBuilder,
    MultiESDTNFTTransferBuilder)

dummyConfig = DefaultTransactionBuildersConfiguration(chain_id="D")


def test_egld_transfer_builder():
    alice = Address.from_bech32("erd1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssycr6th")
    bob = Address.from_bech32("erd1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqzu66jx")
    transfer = TokenTransfer.of_egld(1000000000000000000)

    # With "data" field
    builder = EGLDTransferBuilder(
        config=dummyConfig,
        sender=alice,
        receiver=bob,
        transfer=transfer,
        data="for the book"
    )

    payload = builder.build_payload()
    tx = builder.build()
    assert payload.data == b"for the book"
    assert tx.chainID == "D"
    assert tx.sender == alice
    assert tx.receiver == bob
    assert tx.gas_limit == 50000 + payload.length() * 1500
    assert tx.data.encoded() == payload.encoded()

    # Without "data" field
    builder = EGLDTransferBuilder(
        config=dummyConfig,
        sender=alice,
        receiver=bob,
        transfer=transfer
    )

    payload = builder.build_payload()
    tx = builder.build()
    assert payload.data == b""
    assert tx.chainID == "D"
    assert tx.sender == alice
    assert tx.receiver == bob
    assert tx.gas_limit == 50000
    assert tx.data.encoded() == payload.encoded()


def test_esdt_transfer_builder():
    alice = Address.from_bech32("erd1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssycr6th")
    bob = Address.from_bech32("erd1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqzu66jx")
    transfer = TokenTransfer.of_fungible("COUNTER-8b028f", 10000)

    builder = ESDTTransferBuilder(
        config=dummyConfig,
        sender=alice,
        receiver=bob,
        transfer=transfer
    )

    payload = builder.build_payload()
    tx = builder.build()
    assert payload.data == b"ESDTTransfer@434f554e5445522d386230323866@2710"
    assert tx.chainID == "D"
    assert tx.sender == alice
    assert tx.receiver == bob
    assert tx.gas_limit == 50000 + payload.length() * 1500 + 100000 + 200000
    assert tx.data.encoded() == payload.encoded()


def test_esdt_nft_transfer_builder():
    alice = Address.from_bech32("erd1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssycr6th")
    bob = Address.from_bech32("erd1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqzu66jx")
    transfer = TokenTransfer.of_non_fungible("TEST-38f249", 1)

    builder = ESDTNFTTransferBuilder(
        config=dummyConfig,
        sender=alice,
        destination=bob,
        transfer=transfer
    )

    payload = builder.build_payload()
    tx = builder.build()
    assert payload.data == b"ESDTNFTTransfer@544553542d333866323439@01@01@8049d639e5a6980d1cd2392abcce41029cda74a1563523a202f09641cc2618f8"
    assert tx.chainID == "D"
    assert tx.sender == alice
    assert tx.receiver == alice
    assert tx.gas_limit == 50000 + payload.length() * 1500 + 200000 + 800000
    assert tx.data.encoded() == payload.encoded()


def test_multi_esdt_nft_transfer_builder():
    alice = Address.from_bech32("erd1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssycr6th")
    bob = Address.from_bech32("erd1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqzu66jx")

    transfer_one = TokenTransfer.of_non_fungible("TEST-38f249", 1)
    transfer_two = TokenTransfer.of_fungible("BAR-c80d29", 10000000000000000000)

    builder = MultiESDTNFTTransferBuilder(
        config=dummyConfig,
        sender=alice,
        destination=bob,
        transfers=[transfer_one, transfer_two]
    )

    payload = builder.build_payload()
    tx = builder.build()
    assert payload.data == b"MultiESDTNFTTransfer@8049d639e5a6980d1cd2392abcce41029cda74a1563523a202f09641cc2618f8@02@544553542d333866323439@01@01@4241522d633830643239@@8ac7230489e80000"
    assert tx.chainID == "D"
    assert tx.sender == alice
    assert tx.receiver == alice
    assert tx.gas_limit == 50000 + payload.length() * 1500 + 2 * (200000 + 800000)
    assert tx.data.encoded() == payload.encoded()
