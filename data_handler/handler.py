import datetime
import time
import psycopg2
import requests
import checker

# from datetime import datetime
from bs4 import BeautifulSoup as bs
from psycopg2 import Error


def delete_table_data(table):
    conn = psycopg2.connect(dbname='test1', user='postgres',
                            password='2204', host='localhost')
    cursor = conn.cursor()

    try:
        cursor.execute(f"TRUNCATE TABLE {table}")
        conn.commit()

    except (Exception, Error) as error:
        print('Postgresql error:', error)

    finally:
        cursor.close()
        conn.close()


def db_create(num, order_num, cost_usd, cost_rub, delivery_time):
    """
    Данная функция предназначена для добавления первичной таблицы в БД.
    Принимает на вход из google sheet таблицы номер, номер заказа, стоимость в долларах, стоимость в рублях, дату.
    """

    conn = psycopg2.connect(dbname='test1', user='postgres',
                            password='2204', host='localhost')

    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO orders_data (num, order_num, cost_usd, cost_rub, delivery_time)
                       VALUES (%(num)s, %(order_num)s, %(cost_usd)s, %(cost_rub)s, %(delivery_time)s);""",
                       {'num': num, 'order_num': order_num, 'cost_usd': cost_usd, 'cost_rub': cost_rub,
                        'delivery_time': delivery_time})
        conn.commit()

    except (Exception, Error) as error:
        print('Postgresql error:', error)

    finally:
        cursor.close()
        conn.close()


def main():
    """
    Данная функция предназначена для форматирования данных из первичной google sheet таблицы с целью последующего
    добавления в БД.
    """

    values = checker.get_sheet()

    print('Google sheet table received')

    delete_table_data('orders_data')

    for x in range(1, len(values['values'][0])):
        date = values['values'][3][x].rsplit('.')
        date_now = datetime.datetime.now().strftime('%d/%m/%Y')
        date_to_pg = datetime.date(int(date[2]), int(date[1]), int(date[0]))

        data = requests.get(f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date_now}')

        bs_content = bs(data.content, "xml")
        course = bs_content.find('Valute', {'ID': 'R01235'})('Value')[0].text.rsplit(',')
        course_float = float('.'.join(course))

        print(values['values'][0][x], values['values'][1][x], values['values'][2][x], date_to_pg, course_float)

        db_create(values['values'][0][x], values['values'][1][x], values['values'][2][x],
                  round(float(values['values'][2][x]) * course_float, 2), date_to_pg)

    print('End add data\n')


if __name__ == '__main__':
    main()

    try:
        while True:
            checker.check_func()
            time.sleep(30)

    except Exception as err:
        print('Error:', err)

    except KeyboardInterrupt:
        print('\nExit...')
