from email import message
import logging
from telegram import ParseMode, Update, File
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler
from dotenv import load_dotenv
import os
from julie import handleText
from service import getEvent, getEventByTx, getItemOffer, getMarketplaceItemDetail, getOwnerOfNFT, getNFTGameInfo, getTokenGameInfo, deployMarketplace
config = load_dotenv()

logger = logging.getLogger(__name__)
PORT = int(os.environ.get('PORT', '8443'))

def process(update: Update, context: CallbackContext) -> None:
    with open('download/'+update.message.document.file_name, 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)
    
    # context.bot.send_document('download/'+update.message.document.file_name,update.message.document.file_name)
    update.message.reply_text('was send');
def handleGetItemOffer(update: Update, context: CallbackContext) -> None:
    result  = getItemOffer(os.getenv('EPIC_NFT_CONTRACT_ADDRESS'), context.args[0], context.args[1])
    update.message.reply_text(result)

def handleGetMarketplaceDetail(update: Update, context: CallbackContext) -> None:
    result = getMarketplaceItemDetail(context.args[0])
    update.message.reply_text(result)

def handleGetOwnerOfNFT(update: Update, context: CallbackContext) -> None:
    result = getOwnerOfNFT(context.args[0])
    update.message.reply_text(result)

def handleGetTokenGameInfo(update: Update, context: CallbackContext) -> None:
    result = getTokenGameInfo(context.args[0])
    update.message.reply_text(result)
    
def handleGetNFTGameInfo(update: Update, context: CallbackContext) -> None:
    result = getNFTGameInfo(context.args[0])
    update.message.reply_text(result)

def handleGetEvent(update:Update, context: CallbackContext) -> None:
    getEvent(update,context.args[0], context.args[1], int(context.args[2]), int(context.args[3]));

def handleGetEventByTx(update:Update, context: CallbackContext) -> None:
    getEventByTx(update, context.args[0], context.args[1], context.args[2])

def handleDeployMarketplace(update:Update, context: CallbackContext) -> None:
    if(context.args[0] == "marketplace"):
        deployMarketplace(update=update)

def handleHelp(update: Update, context: CallbackContext) -> None:
     
    update.message.reply_text(
  '''contract_name = {game, marketplace, box, nft}\n/offer <tokenId> <buyer> - Get item offer \n/market <tokenId> - Get marketplace detail \n/owner <tokenId> - Get owner \n/tokengame <address> - Get token of game\n/nftgame <tokenId> - Get nft of game\n/event <contract_name> <event_name> <start_block> <end_block> - Get events of contract\n/eventbytx <contract_name> <event_name> <tx_hash> - Get event of contract by tx hash\n'''
    )
def handleStart(update: Update, context: CallbackContext) -> None:
     update.message.reply_text(
  '''contract_name = {game, marketplace, box, nft}\n/offer <tokenId> <buyer> - Get item offer \n/market <tokenId> - Get marketplace detail \n/owner <tokenId> - Get owner \n/tokengame <address> - Get token of game\n/nftgame <tokenId> - Get nft of game\n/event <contract_name> <event_name> <start_block> <end_block> - Get events of contract\n/eventbytx <contract_name> <event_name> <tx_hash> - Get event of contract by tx hash\n'''
    )
def handleResponseText(update: Update, context: CallbackContext) -> None:
    handleText(update.message.text, update=update, context=context)

def error(update, context):
    """Logs Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None: 
    print('TELEBOT STARTED')
    updater = Updater(os.getenv('TELE_TOKEN'))
    APP_NAME = 'https://juliebot-v1.herokuapp.com/'
       # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handleResponseText))
    dispatcher.add_handler(MessageHandler(Filters.attachment, process))
    dispatcher.add_handler(CommandHandler("start",handleStart))
    dispatcher.add_handler(CommandHandler("help",handleHelp))
    dispatcher.add_handler(CommandHandler("offer",handleGetItemOffer))
    dispatcher.add_handler(CommandHandler("market",handleGetMarketplaceDetail))
    dispatcher.add_handler(CommandHandler("owner",handleGetOwnerOfNFT))
    dispatcher.add_handler(CommandHandler("tokengame",handleGetTokenGameInfo))
    dispatcher.add_handler(CommandHandler("nftgame",handleGetNFTGameInfo))
    dispatcher.add_handler(CommandHandler("event",handleGetEvent))
    dispatcher.add_handler(CommandHandler("eventbytx",handleGetEventByTx))
    dispatcher.add_handler(CommandHandler("deploy",handleDeployMarketplace))
   
    # Start the Bot

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    dispatcher.add_error_handler(error)
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=os.getenv('TELE_TOKEN'), webhook_url=APP_NAME + os.getenv('TELE_TOKEN'))
    updater.idle()
if __name__ == '__main__':
    main()