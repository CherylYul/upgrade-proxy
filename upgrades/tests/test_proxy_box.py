from brownie import (
    Contract,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Box,
)
from scripts.helpful_scripts import get_account, encode_function_data


def test_proxy_delegates_calls():
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    encoded_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        encoded_function,
        {"from": account, "gas_limit": 1000000},
    )
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    assert proxy_box.retrieve() == 0
    proxy_box.store(19, {"from": account})
    assert proxy_box.retrieve() == 19
