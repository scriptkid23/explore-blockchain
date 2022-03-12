from email import message
import logging
from telegram import Update, File
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters
from dotenv import load_dotenv
import os
config = load_dotenv()

logger = logging.getLogger(__name__)


def process(update: Update, context: CallbackContext) -> None:
    with open('download/'+update.message.document.file_name, 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)
    
    # context.bot.send_document('download/'+update.message.document.file_name,update.message.document.file_name)
    update.message.reply_text('was send');


def main() -> None: 
    print('TELEBOT STARTED')
    updater = Updater(os.getenv('TELE_TOKEN'))

       # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.attachment, process))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
if __name__ == '__main__':
    main()