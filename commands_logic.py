import logging
import datetime
import server_conversaion as serv
import ACM_KEYS as api
import requests
CURRENT_WEATHER = 'http://api.openweathermap.org/data/2.5/weather?'
FIVE_DAYS_WEATHER = 'http://api.openweathermap.org/data/2.5/forecast?'


#Получение спраки по боту
def get_help():
    serv.server_send("Доступные команды : /help , /current , /tommorow, /week")



#Получение информации о текущей погоде
def get_current(requested_city):
    if check_city(requested_city):
        url = CURRENT_WEATHER + 'q=' + requested_city + '&units=metric&' + '&lang=ru&' + 'appid=' + api.OPENMAP_KEY
        res = requests.get(url)
        logging.info(res)
        data = res.json()
        city = data['name'] + " " + "(" + data['sys']['country'] + ")"
        # send_message(chat_id, city)
        temp = data['main']['temp']
        conditions = data['weather'][0]['description']
        result = "Город: " + city + " \nТемпература: " + str(temp) + "°C \n" + conditions
        serv.server_send(result)


#Получение прогноза погоды на следующий день
def get_tomorrow(requested_city):
    if check_city(requested_city):
        requested_city = str(requested_city).replace(' ', '%20')
        tomorrow_weather = get_tomorrow_weather(requested_city)
        tomorrow_weather_req = []
        for el in tomorrow_weather:
            date = "Дата: " + el['date'][0] + '\n'
            hours = "Время: " + el['date'][1]
            temp = "\nТемпература: " + str(el['temp']) + '°C\n'
            weather = "Условия: " + el['weather'] + '\n'
            answer = {'date': date,
                      'hours': hours,
                      'temp': temp,
                      'weather': weather}
            tomorrow_weather_req.append(answer)

            logging.info(tomorrow_weather_req)

        result = "Прогноз погоды на завтра в городе " + str(requested_city).replace('%20', ' ') + ":\n\n" + \
                  tomorrow_weather_req[2]['date'] + \
                  tomorrow_weather_req[2]['hours'] + "(Утро)" + \
                  tomorrow_weather_req[2]['temp']  + \
                  tomorrow_weather_req[2]['weather'] + \
                  " ----------------------- \n" + \
                  tomorrow_weather_req[4]['date'] + \
                  tomorrow_weather_req[4]['hours'] + "(День)" + \
                  tomorrow_weather_req[4]['temp'] + \
                  tomorrow_weather_req[4]['weather'] + \
                  " ----------------------- \n" + \
                  tomorrow_weather_req[6]['date'] + \
                  tomorrow_weather_req[6]['hours'] + "(Вечер)" + \
                  tomorrow_weather_req[6]['temp'] + \
                  tomorrow_weather_req[6]['weather']
        serv.server_send(result)

def get_tomorrow_weather(city):
    try:
        tomorrow_date = []
        answer = get_five_days_weather(city)
        for el in answer:
            if el['date'][0] == str(datetime.date.today() + datetime.timedelta(days=1)):
                tomorrow_date.append(el)
          #  el['date'] = el['date'][0] + " " + el['date'][1]
        print(tomorrow_date)
    except Exception as e:
        print("Exception (find):", e)
    return tomorrow_date





#Получение прогноза погоды на пять дней
def get_week(requested_city):
    if check_city(requested_city):
        tomorrow_weather = get_five_days_weather(requested_city)
        tomorrow_weather_req = []
        weather_arr = []
        n = 0
        for el in tomorrow_weather:
            date = "Дата: " + el['date'][0] + '\n' # + el['date'][1] + '\n'
            temp = "Температура: " + str(el['temp']) + '°C\n'
            weather = "Условия: " + el['weather'] + '\n'
            answer = {'date': date,
                      'temp': temp,
                      'weather': weather}
            if str(el['date'][1]) == "15:00:00":
                tomorrow_weather_req.append(answer)
        result = "Прогноз погоды на пять дней для города "  + str(requested_city).replace('%20', ' ') + ":\n\n" + \
                 tomorrow_weather_req[0]['date'] + \
                 tomorrow_weather_req[0]['temp'] + \
                 tomorrow_weather_req[0]['weather'] + \
                 " ----------------------- \n" + \
                 tomorrow_weather_req[1]['date'] + \
                 tomorrow_weather_req[1]['temp'] + \
                 tomorrow_weather_req[1]['weather'] + \
                 " ----------------------- \n" + \
                 tomorrow_weather_req[2]['date'] + \
                 tomorrow_weather_req[2]['temp'] + \
                 tomorrow_weather_req[2]['weather'] + \
                 " ----------------------- \n" + \
                 tomorrow_weather_req[3]['date'] + \
                 tomorrow_weather_req[3]['temp'] + \
                 tomorrow_weather_req[3]['weather'] + \
                 " ----------------------- \n" + \
                 tomorrow_weather_req[4]['date'] + \
                 tomorrow_weather_req[4]['temp'] + \
                 tomorrow_weather_req[4]['weather']

        serv.server_send(result)

def get_five_days_weather(city):
    try:
        url = FIVE_DAYS_WEATHER + 'q=' + city + '&units=metric&' + '&lang=ru&' + 'appid=' + api.OPENMAP_KEY
        # http://api.openweathermap.org / data / 2.5 / forecast?q=Екатеринбург&units=metric&&lang=ru&appid=be17e5c59354e617fc1ba2c33eb93a34
        res = requests.get(url)
        data = res.json()
        answer_list = []
        for el in data['list']:
            date = el['dt_txt']
            date = date.split(' ')
            temp = el['main']['temp']
            for i in el['weather']:
                weather_main = i['description']
                answer = {'date': date,
                          'temp': temp,
                          'weather': weather_main}
            answer_list.append(answer)
        print(answer_list)
    except Exception as e:
        print("Exception (find):", e)
    return answer_list

def check_city(requested_city):
    url = CURRENT_WEATHER + 'q=' + requested_city + '&units=metric&' + '&lang=ru&' + 'appid=' + api.OPENMAP_KEY
    res = requests.get(url).status_code
    logging.info(res)
    if res == 200:
        return True
    else:
        serv.server_send('Хмммм.... Интересно. Твой город не найден. Попробуй ввести еще разок, кожаный ублюдок')
        return False