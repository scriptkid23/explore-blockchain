from email import message
import logging
from telegram import ParseMode, Update, File
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler
from dotenv import load_dotenv
import os
from service import getItemOffer, getMarketplaceItemDetail, getOwnerOfNFT
config = load_dotenv()

logger = logging.getLogger(__name__)


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
def handleHelp(update: Update, context: CallbackContext) -> None:
    
    # <b>/offer:</b><code>&lt;token_id&gt; &lt;buyer&gt;: get item offer</code>\n
    # <b>/market:</b><code>&lt;token_id&gt;: get marketplace detail</code>\n
    # <b>/owner:</b><pre>&lt;token_id&gt; &lt;buyer&gt;: get owner</pre>\n
    
    update.message.reply_text(
  '''/offer <tokenId> <buyer> - Get item offer \n/market <tokenId> - Get marketplace detail \n/owner <tokenId> - Get owner \n'''
    )
def main() -> None: 
    print('TELEBOT STARTED')
    updater = Updater(os.getenv('TELE_TOKEN'))

       # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.attachment, process))
    dispatcher.add_handler(CommandHandler("help",handleHelp))
    dispatcher.add_handler(CommandHandler("offer",handleGetItemOffer))
    dispatcher.add_handler(CommandHandler("market",handleGetMarketplaceDetail))
    dispatcher.add_handler(CommandHandler("owner",handleGetOwnerOfNFT))
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
if __name__ == '__main__':
    main()