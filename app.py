from flask import Flask, request

import telegram
from telebot.credentials import bot_token, bot_user_name,URL
from telebot import db_controller

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)


app = Flask(__name__)


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    try:
        update = telegram.Update.de_json(request.get_json(force=True),bot)

        chat_id = update.message.chat_id
        msg_id = update.message.message_id

        text = update.message.text
        print('got text message:',text)
        if text == '/st2art':
            bot_msg = """
            Привtl!
            Этот бот поможет тебе узнать актуальное расписание
                """
            bot.sendMessage(chat_id=chat_id,text = bot_msg)

        elif text == '/sch':
            bot.sendMessage(chat_id=chat_id, text='Feature not ready yet')
        elif '/group' in text:
            group = text.replace('/group')
            if group.upper() in ['БВТ210' + str(i) for i in range(1,9)]:

                msg = db_controller.add_db(chat_id,group.upper())

            else:
                msg = 'Введена неправильная группа'
            bot.sendMessage(chat_id=chat_id,text=msg)

        elif text =='/help':
            bot_msg = """Список команд:
            - /sch
            - /help
            - /start
                                """
            bot.sendMessage(chat_id=chat_id,text = bot_msg)


        else:
            bot_msg = 'Неизвестная комманда. Используйте /help для вывода списка команд'
            bot.sendMessage(chat_id=chat_id, text=bot_msg)

        return 'ok'
    except:
        return 'Bad request'
@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))

    if s:
        return 'webhook setup ok'
    else:
        return 'webhook setup failed'

@app.route('/')
def index():
    return 'NOne'

if __name__ == '__main__':
    app.run(threaded = True)



