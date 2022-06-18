# Описание тестового задания

Ответ на задание представлен в трех частях: 
- Обработчик гугл-таблицы (папка data_handler)
- API для сайта (папка api)
- Сайт (папка site) 
   
### Обработчик  
  
Данная папка состоит из трех скриптов. Сначала необходимо запустить handler.py
  
При запуске этот скрипт добавляет всю таблицу в базу данных, далее раз в 15 секунд сканирует таблицу на наличие изменений. ВАЖНО: чтобы скрипт корректно обрабатывал изменения в таблице, следует добавлять и удалять данные только с конца таблицы. Изменения можно производить в любой ячейке, кроме номера таблицы.  
  
Данный скрипт использует в своей работе checker.py, который помогает анализировать данные.
  
Для того, чтобы запустить handler.py, понадобится:
- установить модуль psycopg2
- установить модуль BeautifulSoup
- иметь установленную СУБД postgresql (в файле handler.py в 13-14 строках прописать данные для доступа к БД, предварительно создав таблицу с именем "orders_data")
  
Далее из терминала запускаете скрипт командой "python (на linux "python3") handler.py" и он начинает свою работу.  
Если все сделано верно, то вы должны увидеть такой вывод:  
<a href="https://ibb.co/VMvXGpr"><img src="https://i.ibb.co/RQCLK4Z/image.png" alt="image" border="0"></a>
  
После того, как вы запустили handler.py и он заполнил базу данными, нужно запустить скрипт tg_notification.py. Этот скрипт по сути является ботом, который проверяет наличие изменений в базе, и если изменения есть, проверяет дату заказа. Если дата заказа просрочена, то бот уведомляет пользователя об этом. 
  
Для того, чтобы запустить этот скрипт, понадобится:
- установить модуль aiogram
- указать токен в седьмой строке, если не указан
  
Далее из терминала запускаете скрипт командой "python (на linux "python3") tg_notification.py" и он начинает свою работу.  
Следом (если используете бота с моим токеном) ищете бота @tg_notif_test_bot и запускаете уведомления, отсылая ему команду "/start_notification". Остановить уведомления можно командой "/stop_notification".  
  
Если все сделано верно, то вы должны увидеть такой вывод в чате с ботом: 
<a href="https://imgbb.com/"><img src="https://i.ibb.co/6nKBfH7/image.png" alt="image" border="0"></a>
  
### API для сайта  
После запуска обработчика и бота необходимо запустить API, который будет использовать сайт
