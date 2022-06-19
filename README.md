# Описание тестового задания

Ответ на задание представлен в трех частях: 
- Обработчик гугл-таблицы (папка data_handler)
- API для сайта (папка api)
- Сайт (папка site) 
   
### Обработчик  
  
Данная папка состоит из трех скриптов. Сначала необходимо запустить handler.py
  
При запуске этот скрипт добавляет всю таблицу в базу данных, далее раз в 15 секунд сканирует таблицу на наличие изменений. ВАЖНО: чтобы скрипт корректно обрабатывал изменения в таблице (ссылка на мою таблицу https://docs.google.com/spreadsheets/d/1Yc6nsJ-p7uzuT2BPTJcAPtdPEFb1boq0FUBe0NOf_p0/edit#gid=0, которая используется в данном проекте), следует добавлять и удалять данные только с конца таблицы. Изменения можно производить в любой строке и в любой ячейке, кроме номера таблицы.  
  
Данный скрипт использует в своей работе checker.py, который помогает анализировать данные.
  
Для того, чтобы запустить handler.py, понадобится:
- установить модуль psycopg2
- установить модуль BeautifulSoup
- иметь файл credentials.json (данные для доступа к google sheet api) в одной папке со скриптом
- иметь установленную СУБД postgresql (в файле handler.py в 13-14 строках прописать данные для доступа к БД, предварительно создав таблицу с именем "orders_data", SQL-код прикреплен ниже)  
  
<a href="https://imgbb.com/"><img src="https://i.ibb.co/k8BhFH6/image.png" alt="image" border="0"></a><br />
  
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
После запуска обработчика и бота необходимо запустить API, который будет использовать сайт. В качестве бэка для API использован django. 
  
Для того, чтобы запустить API, нужно запустить файл manage.py, для которого нужно следующее:
- установить фреймворк django
- установить фреймворк Django Rest Framework
- установить библеотеку corsheaders
- в строках 89-93 файла settings.py изменить данные от БД на свои
- в строках 18-19 файла views.py в папке data_api данного django-проекта заменить данные от БД на свои
- сделать миграции в БД командами "python (на linux "python3") manage.py makemigrations" и "python (на linux "python3") migrate"  
  
Далее из терминала запускаете скрипт командой "python (на linux "python3") manage.py" и он начинает свою работу.  
  
Если все сделано верно, то вы должны увидеть такой вывод:  
<a href="https://ibb.co/WnbBd59"><img src="https://i.ibb.co/CBkVX8d/image.png" alt="image" border="0"></a>  
  
### Сайт  
После того, как выполнены все предыдущие пункты, можно переходить к запуску сайта. Сайт спроектирован на React. Все данные веб-приложение получает с эндпоинта API "http://127.0.0.1:8000/api/get-data".  
  
Для того, чтобы запустить сайт, необходимо:
- создать любой пустой react-проект командой "npx create-react-app site" (для запуска этой команды нужен установленный на ПК npx)
- папки public и src в вашем только что созданном проекте нужно заменить на аналогичные папки из данного проекта (папка site)
- установить библеотеку bootstrap командой "npm i bootstrap"
- далее из папки site запустить сайт командой "npm start"  
  
Если все сделано верно, то вы должны увидеть такой вывод по адресу "http://localhost:3000":  
<a href="https://ibb.co/7kZ7Tf7"><img src="https://i.ibb.co/rdznLjn/image.png" alt="image" border="0"></a>  
  
На этом этапе описание проекта закончено.
