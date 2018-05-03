import asyncio
import logging

from server_conversaion import check, server_send

logging.basicConfig(level=logging.INFO)

# Запуск асинхронного цикла, вынесен отдельно, чтобы можно было спокойно импортить питоновые пакеты.
server_send('Бот запущен')
logging.info('Бот запущен.')
try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(check())
    loop.run_forever()
except KeyboardInterrupt:
    server_send('Бот входит в режим технического обслуживания. Команды не обслуживаются.')
