from ast import Dict
import string
from textwrap import indent
from telegram import Update
from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv
import os
import requests
import json
import constants
load_dotenv()

abi_nft = open("./abi/EpicWarNFT.json", 'r').read()
abi_box = open("./abi/EpicWarBox.json", 'r').read()
abi_token = open("./abi/EpicWarToken.json", 'r').read()
abi_marketplace = open("./abi/Marketplace.json", 'r').read()
abi_game = open("./abi/NFTWEscrow.json", 'r').read()

box_contract_address = Web3.toChecksumAddress(os.getenv('EPIC_BOX_CONTRACT_ADDRESS'))
nft_contract_address = Web3.toChecksumAddress(os.getenv('EPIC_NFT_CONTRACT_ADDRESS'))
token_contract_address = Web3.toChecksumAddress(os.getenv('EPIC_TOKEN_CONTRACT_ADDRESS'))
marketplace_contract_address = Web3.toChecksumAddress(os.getenv('MARKETPLACE_CONTRACT_ADDRESS'))
game_contract_address = Web3.toChecksumAddress(os.getenv('EPIC_GAME_CONTRACT_ADDRESS'))

w3 = Web3(Web3.HTTPProvider(os.getenv('BSC_RPC_URL')))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

box_contract = w3.eth.contract(box_contract_address, abi=abi_box)
nft_contract = w3.eth.contract(nft_contract_address, abi=abi_nft)
token_contract = w3.eth.contract(token_contract_address, abi=abi_token)
marketplace_contract = w3.eth.contract(marketplace_contract_address, abi=abi_marketplace)
game_contract = w3.eth.contract(game_contract_address, abi=abi_game)


def mappingArray2Dict(array:list, pattern: list) -> Dict:
    obj = {}
    for i in range(0, len(pattern)):
        obj[pattern[i]] = array[i]
    return obj

def getMarketplaceItemDetail(tokenId) -> Dict:
    try:
        r = requests.get('http://23.22.198.29:8080/api/v1/market/'+tokenId)

        if r.status_code == 200:
            data = r.json()
            if(not bool(data)):
                return json.dumps({"message": "NFT was unlisted"}, indent=4, sort_keys=True)

            if(data['market_item_id'] != -1):
                pattern = ["tokenId", "endTime","reservePrice","price","tokenAddress","tokenOwner","bidder","currency","marketItemType"]
                marketplaceDetail = marketplace_contract.functions.marketPlaceItems(int(data['market_item_id'])).call()
                return json.dumps(mappingArray2Dict(marketplaceDetail, pattern),indent=4, sort_keys=True)
            else:
                return {"message": "NFT was unlisted"}
        else:
            return {"message": "Data not found"}
    except:
        return {}

def getOwnerOfNFT(tokenId) -> string:
    try:
        return nft_contract.functions.ownerOf(int(tokenId)).call()
    except:
        return {}

def getItemOffer(tokenAddress, tokenId, buyer):
    try:  
        pattern = ["currency","price"]
        itemOffer = marketplace_contract.functions.itemOffers(tokenAddress, int(tokenId), buyer).call()
        return mappingArray2Dict(itemOffer, pattern)
    except:
        return {}
def getNFTGameInfo(tokenId):
    try:
        pattern = ["owner", "claimable"]
        result = game_contract.functions.NftInfo(int(tokenId)).call()
        return mappingArray2Dict(result, pattern)
    except:
        return {}
def getTokenGameInfo(address):
    try:
        return game_contract.functions.TokenInfo(address).call()
    except:
        return {}

# /event <contract_name> <event_name> <start_block> <end_block>
def getEventByTx(update:Update, contract, event, tx_hash):
    contractSwitcher = {
        "game" : game_contract,
        "marketplace": marketplace_contract,
        "nft": nft_contract,
        "box":box_contract
    }   
    print(contract,event,tx_hash)
    try:
        update.message.reply_text("Processing...🥴")
        txr = w3.eth.get_transaction_receipt(tx_hash)
        receipt = contractSwitcher.get(contract,game_contract).events[event]().processReceipt(txr)
        update.message.reply_text(json.dumps(json.loads(w3.toJSON(receipt)),indent=4,sort_keys=True))
        update.message.reply_text("end.😪")
    except Exception as e:
        update.message.reply_text(str(e) +" "+"😵")
        
def getEvent(update: Update, contract, event, start_block:int, end_block:int):
    contractSwitcher = {
        "game" : game_contract,
        "marketplace": marketplace_contract,
        "nft": nft_contract,
        "box":box_contract
    }
    try:
        update.message.reply_text("Crawling...🥴")
        while start_block < end_block:
            if(end_block - start_block < 5000):
                event_filter = contractSwitcher.get(contract,game_contract).events[event].createFilter(fromBlock=start_block, toBlock=end_block)
            else:
                event_filter = contractSwitcher.get(contract,game_contract).events[event].createFilter(fromBlock=start_block, toBlock=start_block + 4999)
            temp  = json.loads(Web3.toJSON(event_filter.get_all_entries()))
            if(len(temp) != 0):
                update.message.reply_text(json.dumps(temp, indent=4,sort_keys=True))
            
            start_block = start_block + 5000
        update.message.reply_text("end.😪")
    except Exception as e:
        update.message.reply_text(str(e) +" "+"😵")


