import asyncio
import psycopg2

from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token="5539666555:AAFsPDJqdXP5c8TYYmAj0LT40sRCDMKxhqg")

dp = Dispatcher(bot)

users = []

state = False

current_line = 1
last_line = 0


async def check_delivery_date(user):
    """
    Функция, необходимая для извлечения данных из БД. Она анализирует строки, а именно дату, и если дата
    просрочена - уведомляет пользователя об этом. Работает в онлайн режиме, то есть если в гугл-таблицу
    добавить строку, то эта функция ее проанализирует.
    """

    global current_line
    global last_line
    global state

    now = (datetime.now())

    conn = psycopg2.connect(dbname='test1', user='postgres',
                            password='2204', host='localhost')

    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM orders_data ORDER BY num DESC LIMIT 1""")
    last_line = cursor.fetchall()[0][0]

    if last_line == current_line - 1:
        return

    cursor.execute(f'SELECT * FROM orders_data WHERE num={current_line}')

    for x in cursor:
        date = str(x[4]).rsplit('-')
        deadline = datetime(int(date[0]), int(date[1]), int(date[2]))

        if now > deadline:
            message = f'[Delivery time is over] Num: {x[0]}, order num: {x[1]}, ' \
                      f'cost usd: {x[2]}, delivery time: {x[4]}'

            await bot.send_message(user, message)

    cursor.close()
    conn.close()

    current_line += 1


@dp.message_handler(commands="start_notification")
async def start_broadcast(message: types.Message):
    """
    Функция предназначена для запуска бота командой /start_notification
    Nickname бота - @tg_notif_test_bot
    """

    users.append(message.from_user.id)

    global state
    state = True

    while state:
        for user in users:
            await check_delivery_date(user)
        await asyncio.sleep(2)  # Таймаут отправки уведомления в телеграм


@dp.message_handler(commands="stop_notification")
async def stop_broadcast(message: types.Message):
    """
    Функция предназначена для запуска бота командой /start_notification
    Nickname бота - @tg_notif_test_bot
    """

    global state
    state = False


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
