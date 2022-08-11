from scripts.helpful_scripts import get_account, encode_function_data, upgrade
from brownie import (
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    network,
    Contract,
)


def main():
    account = get_account()
    box = Box.deploy({"from": account})
    print(box.retrieve())

    proxy_admin = ProxyAdmin.deploy({"from": account})
    initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data(initializer)

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    print(f"Proxy deployed to {proxy}, we move to v2~")

    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(2310, {"from": account})
    print(proxy_box.retrieve())

    # Upgrade
    box_v2 = BoxV2.deploy({"from": account})
    upgrade_transaction = upgrade(
        account, proxy, box_v2.address, proxy_admin_contract=proxy_admin
    )
    upgrade_transaction.wait(1)
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.increment({"from": account})
    print(proxy_box.retrieve())
