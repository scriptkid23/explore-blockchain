from telegram import Update
import wikipedia
from googlesearch import search
from constants import QUESTION, TAG_NAME
wikipedia.set_lang('vi')

def handleText(response: str, update: Update):
    if(response.find(TAG_NAME) != -1):
        update.message.reply_text("Dạ, em sẽ chuyển lời đến anh " + TAG_NAME + " ạ.")
    else:
        for i in QUESTION:
            if response.find(i) != -1:
                _input = response.split(i)
                result = search(response, lang='vi', num_results=1)
                for i in result:
                    update.message.reply_text(i)
                    break
                update.message.reply_text(wikipedia.summary(_input[0],sentences=2))
