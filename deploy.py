from solcx import compile_standard
from web3 import Web3
import os
from dotenv import load_dotenv

with open("./epoch.sol", "r") as file:
    contract_source_code = file.read()

compiled_contract = compile_standard({
    "language": "Solidity",
    "sources": {"./epoch.sol": {
        "content": contract_source_code
    }},
    "settings": {
        "outputSelection": {
            "*": { "*": 
                    ["abi", "metadata", "evm.bytecode", "evm.sourceMap"] }
        }
    }
}, solc_version = "0.8.0")

abi = compiled_contract["contracts"]["./epoch.sol"]["Epoch"]["abi"]
bytecode = compiled_contract["contracts"]["./epoch.sol"]["Epoch"]["evm"]["bytecode"]["object"]


provider_url = os.getenv("NODE_PROVIDER")
web3 = Web3(Web3.HTTPProvider(provider_url))
first_account = "0x5645dA2A98FCC70Adb32F1af67Cee03643f6e0B4"
nonce = web3.eth.get_transaction_count(first_account)

contract = web3.eth.contract(abi = abi, bytecode = bytecode)
print(nonce)

built_transaction = contract.constructor().buildTransaction({
    "nonce": nonce,
    "gas": 2000000,
    "gasPrice": web3.eth.gas_price,
    "chainId": 1337 
    #Chain IDs are a way to differentiate between different networks. 1337 is the chain ID for the Ganache network. 1 is the chain ID for the Ethereum main network
})
load_dotenv()
signed_transaction = web3.eth.account.sign_transaction(
                     built_transaction,
                     os.getenv("PRIVATE_KEY")
                     )
tx = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
transaction_receipt = web3.eth.wait_for_transaction_receipt(tx)
print(transaction_receipt)
contract_instance = web3.eth.contract(address = transaction_receipt.contractAddress, abi = abi)
print(contract_instance.functions.check().call())