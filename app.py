from flask import Flask, request
import pandas as pd
import telegram
from telebot.credentials import bot_token, bot_user_name,URL,sch_msg

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

# start the flask app
app = Flask(__name__)


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True),bot)

    chat_id = update.message.chat_id
    msg_id = update.message.message_id

    text = update.message.text
    print('got text message:',text)
    if text == '/start':
        bot_msg = """Welcome home, fellow student, feel free to ask me a thing or two about your beloved MTUCI !
        commands :
        - /sch
        """
        bot.sendMessage(chat_id=chat_id,text = bot_msg,reply_to_message_id = msg_id)
    elif text == '/sch':

        bot.sendMessage(chat_id=chat_id, text='Feature not ready yet', reply_to_message_id=msg_id)
    else:
        bot_msg = 'Unknown message, please try again'
        bot.sendMessage(chat_id=chat_id, text=bot_msg, reply_to_message_id=msg_id)
    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))

    if s:
        return 'webhook setup ok'
    else:
        return 'webhook setup failed'

@app.route('/')
def index():
    return sch_msg()

if __name__ == '__main__':
    app.run(threaded = True)



