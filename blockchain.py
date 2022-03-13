from web3 import Web3
from web3.middleware import geth_poa_middleware
import json
f = open("./abi/Minesweeper.json", 'r');

contract_interface = json.load(f)

abi = contract_interface['abi']

address_contract = Web3.toChecksumAddress('0xcc9550849695a76febdabd44cc8a32c884196627')

w3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545'))
print(w3.eth.block_number)
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
# if(w3.isConnected()):
#     print(w3.eth.get_transaction('0xddcff91ff93e590563b94c8ad053a20a1e910edfdd1dc895009790996af70d17').get('from'))

store_contract = w3.eth.contract(address_contract, abi = abi)

start_block = 17426710
result = []
while start_block < w3.eth.block_number:
    if(w3.eth.block_number - start_block < 5000):
        event_filter = store_contract.events.BuyTurn().createFilter(fromBlock=start_block, toBlock=w3.eth.block_number)
    else:
         event_filter = store_contract.events.BuyTurn().createFilter(fromBlock=start_block, toBlock=start_block + 5000)
    temp  = json.loads(Web3.toJSON(event_filter.get_all_entries()))
    if(len(temp) != 0):
        result = result + temp
    
    start_block = start_block + 5001

print(result)
# receipt = w3.eth.get_transaction_receipt('0xb3ea2058e0467de3407e2f6ea7ea917cc8f2aa7a9334892f3a517b489dad3f52')
# data = store_contract.events.BuyTurn().processReceipt(receipt)
# print(data[0]['args'])