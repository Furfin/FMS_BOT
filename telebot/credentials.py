import pandas as pd

bot_token = "1993698998:AAGkN59E9Er98-WE7mnZwsGDz7G1AcQrqpw"
bot_user_name = "@FurfinsMtuciSchedule_bot"
URL = "https://fms-bot.herokuapp.com/"

def sch_msg():
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
    return msg