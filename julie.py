from telegram import Update

def handleText(response: str, update: Update):
   update.message.reply_text(response)