import time
import json
from eth_utils import to_checksum_address
from web3 import Web3

# Set up the node providers (e.g., Infura)
arbi_url = <ARBI_RPC_URL>
w3 = Web3(Web3.HTTPProvider(arbi_url))

eth_url = <ETH_RPC_URL>
w4 = Web3(Web3.HTTPProvider(eth_url))


# Your Ethereum wallet address and private key
my_address = <YOUR_WALLET_ADDRESS>
my_private_key = <YOUR_PRIVATE_KEY>

# ARB token contract address
contract_address = "0x67a24CE4321aB3aF51c2D0a4801c3E111D88C9d9"

# Load ABI for the contract
with open("arb_token_abi.json") as f:
    abi = json.load(f)

# Create the contract object
contract = w3.eth.contract(address=to_checksum_address(contract_address), abi=abi)


response = w4.provider.make_request("eth_getBlockByNumber", ["latest", False])
current_eth_block_number = response['result']['number']
print(f"Current eth block number is : {int(current_eth_block_number, 16)}")



# Monitor the Ethereum block height until it reaches 16,890,400.
while int(current_eth_block_number, 16) < 16890400:
    time.sleep(5)  # Check every 5 seconds

# Estimate the gas required for the claim() function
gas_estimate_claim = w3.eth.estimate_gas({"to": contract_address, "from": my_address, "data": contract.encodeABI(fn_name="claim")})
print(f"Current gas estimate is : {gas_estimate_claim}")

# Get the current gas price
gas_price = w3.eth.gas_price
print(f"Current gas price is : {gas_price}")

# Increase gas estimate by 20%
gas_estimate_with_increase = int(gas_estimate_claim * 1.2)
print(f"Increasing current gas estimate by : {gas_estimate_with_increase}")

gas_price_with_increase = int(gas_price * 1.1)


# Build the transaction for the claim() function
transaction = contract.functions.claim().buildTransaction({
    "from": my_address,
    "gas": gas_estimate_with_increase,
    "nonce": w3.eth.get_transaction_count(my_address),
    "gasPrice": gas_price_with_increase
})

# Sign the transaction
signed_transaction = w3.eth.account.sign_transaction(transaction, my_private_key)

# Send the transaction
transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
print(f"Transaction hash : {transaction_hash.hex()}")

# Wait for the transaction receipt
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
print(f"Transaction receipt : {transaction_receipt}")
print("Tokens claimed successfully!")
