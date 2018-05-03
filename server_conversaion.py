import asyncio
import json
import requests
import logging
import commands_logic as cmd
import ACM_KEYS as server_api


async def message_listener():
    command_data = []
    request = requests.get(server_api.ACM_GET_MESSAGE, headers={"content-type": "text",
                                                                "X-ACM-Chanel": server_api.ACM_CHANNEL,
                                                                "X-ACM-Key": server_api.ACM_KEY})
    try:
        raw_data = request.json()
        if not raw_data:
            return []
        for every_message in range(0, len(raw_data)):
            message_body = raw_data[every_message]['nextState']
            message_text = message_body['message']
            channel_host = raw_data[every_message]['teamName']
            command_data.append(message_text)
            if len(command_data) > 1:
                return [command_data[len(command_data) - 1], channel_host]
            elif command_data:
                return [command_data[0], channel_host]
    except ValueError:
        return []


# Loop command to check messages
# Бесконечный цикл, который обслуживает прослушку сообщений и передачу команды в корутину.
# Из полей - первое сообщение; переведен ли бот в рабочий режим; дефолтный класс с настройками пользователя;
# Класс, который мы получаем из команды с проверками.
async def check():
    first_msg = True
    working_state = False
    user_prefs = None
    prefs = None
    # Листенер фида подписан на changes и ждет свой лист
    while 1:
        # Отправляем функцию в корутину, получаем оттуда канал и сообщение
        msg = await message_listener()
        if msg:
            channel = msg[1]
            message = msg[0]
            logging.info(msg)
            server_api.respond_msg = msg
            logging.info(msg[0])
            if msg[0] == "/help":
                cmd.get_help()
            #Команда получния текущей погоды
            elif str(message).startswith("/current"):
                logging.info("Current weather requested for default city")
                if str(message) == "/current":
                    cmd.get_current(server_api.DEFAULT_CITY)
                else:
                    city = str(message).split(server_api.SEPARATION_KEY)
                    logging.info(city[1])
                    cmd.get_current(city[1])
            #Команда получения прогноза на завтра
            elif str(message).startswith("/tomorrow"):
                logging.info("Tomorrow weather requested for default city")
                if str(message) == "/tomorrow":
                    cmd.get_tomorrow(server_api.DEFAULT_CITY)
                else:
                    city = str(message).split(server_api.SEPARATION_KEY)

                    cmd.get_tomorrow(city[1])

            elif str(message).startswith("/week"):
                logging.info("Tomorrow weather requested for default city")
                if str(message) == "/week":
                    cmd.get_week(server_api.DEFAULT_CITY)
                else:
                    city = str(message).split(server_api.SEPARATION_KEY)

                    cmd.get_week(city[1])
            else:
                server_send("Неверная команда. Попробуй еще разок!")

        await asyncio.sleep(1.2)

def server_send(msg, host_channel=server_api.ACM_TEAM_HEADER):
    data = {'message': msg}
    headers = {'Content-type': 'application/json',
               'X-ACM-Key': server_api.ACM_KEY,
               'X-ACM-Chanel': server_api.ACM_CHANNEL,
               'X-ACM-Transmitter': host_channel}
    url = server_api.ACM_POST_NEWS_API

    requests.post(url, headers=headers, data=json.dumps(data))
