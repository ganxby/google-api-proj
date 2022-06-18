from rest_framework.decorators import api_view
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

from psycopg2 import Error

import psycopg2


@csrf_exempt
@api_view(['GET', 'POST'])
def get_data(request):
    if request.method == 'GET':
        response_list = []

        conn = psycopg2.connect(dbname='test1', user='postgres',
                                password='2204', host='localhost')
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM orders_data;')

            for x in cursor:
                response = {
                    'num': x[0],
                    'order_num': x[1],
                    'cost_usd': x[2],
                    'delivery_time': x[4]
                }

                response_list.append(response)

        except (Exception, Error) as error:
            print('Postgresql error:', error)

        finally:
            cursor.close()
            conn.close()

        return JsonResponse(response_list, status=status.HTTP_200_OK, safe=False)
