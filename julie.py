from telegram import Update
from constants import QUESTION, TAG_NAME

def handleText(response: str, update: Update):
   update.message.reply_text(response)