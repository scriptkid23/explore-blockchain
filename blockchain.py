from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.logs import STRICT, IGNORE, DISCARD, WARN
import json
abi = open("./abi/NFTWEscrow.json", 'r').read();


address_contract = Web3.toChecksumAddress('0x448b00525ccd4552a5c9efbbaab9304e96500c60')

w3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545'))
print(w3.eth.block_number)
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
# if(w3.isConnected()):
#     print(w3.eth.get_transaction('0xddcff91ff93e590563b94c8ad053a20a1e910edfdd1dc895009790996af70d17').get('from'))

store_contract = w3.eth.contract(address_contract, abi = abi)



result = w3.eth.get_transaction_receipt("0xae43881a1a9726bb7490dd7593c08d4836294d0f707b6088218f175ad89ab4f5")
data = store_contract.events.TokenWithdrawed().processReceipt(result,errors=IGNORE)
print(data)