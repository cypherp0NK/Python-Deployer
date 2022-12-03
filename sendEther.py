from web3 import Web3
import os
from dotenv import load_dotenv

provider_url = os.getenv("NODE_PROVIDER")
web3 = Web3(Web3.HTTPProvider(provider_url))

first_account = "0x5645dA2A98FCC70Adb32F1af67Cee03643f6e0B4"
second_account = "0x655FCe1A97c7920544724Db56026D48891F43Ba7"
nonce = web3.eth.get_transaction_count(first_account)
built_transaction = {
    "nonce": nonce,
    "to": second_account,
    "value": web3.toWei(2, "ether"),
    "gas": 21000,
    "gasPrice": web3.eth.gas_price
}
load_dotenv()
signed_transaction = web3.eth.account.sign_transaction(
                     built_transaction,
                     os.getenv("PRIVATE_KEY")
                     )
tx = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
transaction_receipt = web3.eth.wait_for_transaction_receipt(tx)
print(transaction_receipt)