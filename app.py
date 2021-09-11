from flask import Flask, request
import pandas as pd
import telegram
from telebot.credentials import bot_token, bot_user_name,URL

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



        link = 'https://mtuci.ru/time-table/files/%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%B7%D0%B0%D0%BD%D1%8F%D1%82%D0%B8%D0%B9%20%D1%84-%D1%82%20%D0%98%D0%A2%20-%20%2002.03.02,%2009.03.01,%2009.03.02%20-%201,%202%20%D0%BA%D1%83%D1%80%D1%81%20-%20%D1%81%D0%B5%D0%BC%D0%B5%D1%81%D1%82%D1%80%201,3%20-2021-22%20%D1%83%D1%87%20%D0%B3%20(2%D0%BD).xls'
        data = pd.read_excel(link)

        msg = ''
        curr_pair = []

        flags = {'group_name': 0, 'pair_c': 0, 'end': 0, 'day_c': 1}

        for row in data['Unnamed: 6']:
            if flags['pair_c'] == 4:
                msg = msg + 'нечет:' + curr_pair[0] + ' ' + curr_pair[1] + '/чет:' + curr_pair[2] + ' ' + curr_pair[
                    3] + '\n'
                flags['pair_c'] = 0
                curr_pair = []
                flags['end'] += 1
            if flags['end'] == 5:
                flags['day_c'] = flags['day_c'] + 1
                msg = msg + str(flags['day_c']) + '\n'
                flags['end'] = 0
            if flags['day_c'] == 5:
                print(msg)
                break

            if row == 'БВТ2102':
                msg += row
                msg += '\n'
            elif msg != '' and flags['group_name'] != 1:
                flags['group_name'] = 1
            elif flags['group_name'] == 1:
                if str(row) != 'none':
                    curr_pair.append(str(row))
                else:
                    curr_pair.append(' ')
                flags['pair_c'] += 1

        bot.sendMessage(chat_id=chat_id, text='feature not ready yet', reply_to_message_id=msg_id)
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
    return 'NO answer'

if __name__ == '__main__':
    app.run(threaded = True)



