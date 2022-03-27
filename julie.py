from contextvars import Context
from telegram import Update

from constants import TAG_NAME


def handleText(response: str, update: Update, context: Context):
    if(response.find(TAG_NAME) != -1):
        update.message.reply_text("Dạ, em sẽ chuyển lời đến anh " + TAG_NAME + " ạ.")
    
