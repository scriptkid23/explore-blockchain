from email import message
import logging
from telegram import Update, File
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters, CommandHandler
from dotenv import load_dotenv
import os
from service import getItemOffer, getMarketplaceItemDetail, getOwnerOfNFT
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
config = load_dotenv()

logger = logging.getLogger(__name__)


def process(update: Update, context: CallbackContext) -> None:
    with open('download/'+update.message.document.file_name, 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)
    
    # context.bot.send_document('download/'+update.message.document.file_name,update.message.document.file_name)
    update.message.reply_text('was send');
def handleGetItemOffer(update: Update, context: CallbackContext) -> None:
    result  = getItemOffer(ZERO_ADDRESS, context.args[0], context.args[1])
    update.message.reply_text(result)

def handleGetMarketplaceDetail(update: Update, context: CallbackContext) -> None:
    result = getMarketplaceItemDetail(context.args[0])
    update.message.reply_text(result)

def handleGetOwnerOfNFT(update: Update, context: CallbackContext) -> None:
    result = getOwnerOfNFT(context.args[0])
    update.message.reply_text(result)

def main() -> None: 
    print('TELEBOT STARTED')
    updater = Updater(os.getenv('TELE_TOKEN'))

       # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.attachment, process))
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