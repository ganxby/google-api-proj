import datetime
import time

import psycopg2
import httplib2
import apiclient.discovery
import requests
import pandas as pd

from bs4 import BeautifulSoup as bs
from psycopg2 import Error
from oauth2client.service_account import ServiceAccountCredentials


def database_handler(command):
    """
    Данная функция предназначена для подключения к базе данных, исполнения комманды, обработки ошибок при исполнении
    команды, а также для правильного закрытия соединения с БД.
    """

    conn = psycopg2.connect(dbname='test1', user='postgres',
                            password='2204', host='localhost')
    cursor = conn.cursor()

    try:
        cursor.execute(command[0], command[1])
        conn.commit()

    except (Exception, Error) as error:
        print('Postgresql error:', error)

    finally:
        cursor.close()
        conn.close()


def add_data_db(num, order_num, cost_usd, cost_rub, delivery_time):
    """
    Данная функция предназначена для добавления новых строк в базу данных.
    Принимает на вход из google sheet таблицы номер, номер заказа, стоимость в долларах, стоимость в рублях, дату.
    """

    command = ("""INSERT INTO orders_data (num, order_num, cost_usd, cost_rub, delivery_time)
                  VALUES (%(num)s, %(order_num)s, %(cost_usd)s, %(cost_rub)s, %(delivery_time)s);""",
               {'num': num, 'order_num': order_num, 'cost_usd': cost_usd,
                'cost_rub': cost_rub, 'delivery_time': delivery_time})
    database_handler(command)


def update_data_db(num, order_num, cost_usd, cost_rub, delivery_time):
    """
    Данная функция предназначена для добавления обновленных данных в БД.
    Принимает на вход из google sheet таблицы номер, номер заказа, стоимость в долларах, стоимость в рублях, дату.
    """

    command = ("""UPDATE orders_data 
                  SET order_num='%(order_num)s', cost_usd='%(cost_usd)s', cost_rub='%(cost_rub)s', delivery_time=%(delivery_time)s 
                  WHERE num=%(num)s;""",
               {'num': num, 'order_num': order_num, 'cost_usd': cost_usd, 'cost_rub': cost_rub,
                'delivery_time': delivery_time})
    database_handler(command)


def delete_data_db(num):
    """
    Данная функция предназначена для удаления строки из базы данных.
    Принимает на вход номер из google sheet таблицы.
    """

    command = ("""DELETE FROM orders_data WHERE num=%(num)s;""",
               {'num': num})
    database_handler(command)


def dataframe_db():
    """
    Функция, используемая для создания датафрейма по данным из БД. Возвращает датафрейм.
    """

    data_dict = {
        'num': [],
        'order_num': [],
        'cost': [],
        'delivery_time': []
    }

    conn = psycopg2.connect(dbname='test1', user='postgres',
                            password='2204', host='localhost')

    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM orders_data')  # Так как таблица в БД маленькая, то допустимо чтение
                                                     # данных целиком
        for x in cursor:
            data_dict['num'].append(str(x[0]))
            data_dict['order_num'].append(str(x[1]))
            data_dict['cost'].append(str(x[2]))
            data_dict['delivery_time'].append(str(x[4].strftime('%d.%m.%Y')))

        return pd.DataFrame(data_dict)

    except (Exception, Error) as error:
        print('Postgresql error:', error)

    finally:
        cursor.close()
        conn.close()


def dataframe_sheets(values):
    """
    Функция, используемая для создания датафрейма по данным из google sheet таблицы. Возвращает датафрейм.
    """

    data_dict = {
        'num': [],
        'order_num': [],
        'cost': [],
        'delivery_time': []
    }

    for x in range(1, len(values['values'][0])):
        data_dict['num'].append(str(values['values'][0][x]))
        data_dict['order_num'].append(str(values['values'][1][x]))
        data_dict['cost'].append(str(values['values'][2][x]))
        data_dict['delivery_time'].append(str(values['values'][3][x]))

    return pd.DataFrame(data_dict)


def get_sheet():
    """
    Функция запрашивает данные таблицы google sheet и возвращает их.
    """

    CREDENTIALS_FILE = 'credentials.json'
    spreadsheet_id = '1Yc6nsJ-p7uzuT2BPTJcAPtdPEFb1boq0FUBe0NOf_p0'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets']
    )

    httpAuth = credentials.authorize(httplib2.Http())

    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A:D',
        majorDimension='COLUMNS'
    ).execute()

    return values


def get_usd_course(row):
    """
    Функция принимает на вход строку из датафрейма, извлекает из нее дату, получает актуальный курс валюты для
    полученной даты и возвращает курс и измененную дату (чтобы подходила по формату для SQL запроса).
    """

    date = row['delivery_time'].values[0].rsplit('.')
    date_now = datetime.datetime.now().strftime('%d/%m/%Y')
    date_to_pg = datetime.date(int(date[2]), int(date[1]), int(date[0]))

    data = requests.get(f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date_now}')

    bs_content = bs(data.content, "xml")
    course = bs_content.find('Valute', {'ID': 'R01235'})('Value')[0].text.rsplit(',')
    course_float = float('.'.join(course))

    return date_to_pg, course_float


def check_func():
    """
    Данная функция на основе двух датафреймов (google sheet и базы данных) проверяет, есть ли изменения в
    в таблице google sheet. Если изменения имеются, то сначала проверяются добавленные и удаленные строки,
    затем - изменения в имеющихся ячейках таблицы.
    """

    while True:
        values = get_sheet()

        df_DB = dataframe_db()
        df_sheet = dataframe_sheets(values)

        res = pd.concat([df_sheet, df_DB]).drop_duplicates(keep=False)

        if len(res.values) == 0:  # Если изменений нет - цикл прерывается
            print('Changes not found')
            break

        if len(res.values) > 0:  # Если изменения есть - цикл начинает проверки
            if len(df_sheet['num'].values) < len(df_DB['num'].values):  # Оператор проверки на удаленные строки
                print('Deleted row(s) from Google Sheet\n')
                rows = pd.concat([res['num']]).drop_duplicates(keep=False).values

                for x in rows:
                    delete_data_db(int(x))

            elif len(df_sheet['num'].values) > len(df_DB['num'].values):  # Оператор проверки на добавленные строки
                print('Added row(s) in Google Sheet\n')
                rows = pd.concat([res['num']]).drop_duplicates(keep=False).values

                for x in rows:
                    if not x:
                        continue

                    row = df_sheet.loc[df_sheet['num'] == str(x)]
                    date_to_pg, course_float = get_usd_course(row)
                    cost_rub = round(course_float * float(row['cost'].values[0]), 2)

                    add_data_db(int(row['num'].values[0]), int(row['order_num'].values[0]),
                                int(row['cost'].values[0]), int(cost_rub), date_to_pg)

            else:  # Если имеются изменения в ячейках таблицы, то они проверяются на этом этапе.
                print('Changes in Google Sheet\n')

                current_values = []

                for x in res.values:
                    if x[0] not in current_values:
                        current_values.append(x[0])

                        current_line = df_sheet.iloc[[int(x[0]) - 1]]

                        num = int(current_line['num'].values[0])
                        order_num = int(current_line['order_num'].values[0])
                        cost = int(current_line['cost'].values[0])

                        date_to_pg, course_float = get_usd_course(current_line)
                        cost_rub = round(course_float * float(current_line['cost'].values[0]), 2)

                        update_data_db(num, order_num, cost, int(cost_rub), date_to_pg)


if __name__ == '__main__':
    check_func()
