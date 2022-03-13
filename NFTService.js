const { ethers } = require("ethers")
const box_abi = require("./abi/EpicWarBox.json")
const nft_abi = require("./abi/EpicWarNFT.json")
require("dotenv").config();

const buyBoxService = async (privateKey, eventId, amount, indexBoxList, tokenAddress) => {
    const provider= new ethers.providers.JsonRpcProvider(procees.env.BSC_RPC_URL)
    const signer = new ethers.Wallet(privateKey, provider);
    const boxContract = new ethers.Contract(process.env.EPIC_BOX_CONTRACT_ADDRESS, box_abi,signer)
    let eventById = await boxContract.eventById(eventId);
    let finalPrice = ethers.BigNumber.from(eventById.boxPrice).mul(amount);
    let tx = await boxContract.buyBox(eventId, amount, indexBoxList, tokenAddress, {value: finalPrice});
    let txr = await tx?.wait();
    return txr ? true: false;
}