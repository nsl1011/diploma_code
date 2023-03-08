from flask import Flask, render_template, url_for, request, redirect # Импортируем библиотеки
import pymysql
from datetime import datetime
# import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegration

# sentry_sdk.init(
#     dsn="https://edf95c656a5644c08e7f95753ede281a@o4504514952101888.ingest.sentry.io/4504514955313152",
#     integrations=[
#         FlaskIntegration(),
#     ],

#     traces_sample_rate=1.0
# )

app = Flask (__name__) # Создаем экземпляр приложения и присваиваем ему переменную __name__, которая содержит имя текущего файла python


def db_connect(): # Функция для подключения к БД
    connect = pymysql.connect(
        host = "pari2020.beget.tech",
        user = "pari2020_comment",
        password = "Q12345!",
        database = "pari2020_comment",
        cursorclass = pymysql.cursors.DictCursor # ?
    )
    return connect
    

def add_comment(comment): # Функция добавления комментария в БД
    try:
        connect = db_connect() # Подключение к БД
        with connect.cursor() as cursor:
            cursor.execute("""INSERT INTO `comment` (`comment`) value(%s)""", (comment,)) # Добавление в БД комментария
    except Exception as error:
        print(f"error_add_comment {error}") # Вывод ошибок
    finally: # Выполнить в любом случае, даже с ошибками
        connect.commit() # Сохранить данные в БД
        connect.close() # Закрыть БД

@app.route('/form_send', methods=["GET"]) # Ссылка на form_send
def form_send(): # Функция для получения комментария
    if request.method == "GET":
        data = request.args.get('comment_send','')
        if(len(data) > 0): # Условие, чтобы комментарий не был пустой
            add_comment(data) # Добавляем комментарий в БД
    return redirect('/munfunction_battery_not_hold_charge')


def show_comment():
    try:
        connect = db_connect() # Подключение к БД
        with connect.cursor() as cursor: 
            cursor.execute("""SELECT * FROM `comment`""")
            data = cursor.fetchall()
    except Exception as error:
        print(f"error_add_comment {error}") # Вывод ошибок
    finally: # Выполнить в любом случае, даже с ошибками
        connect.commit() # Сохранить данные в БД
        connect.close() # Закрыть БД
    return data


@app.route('/')
def index():
    return render_template("index.html")

ч
@app.route('/authorization')
def authorization():
    return render_template("authorization.html")


@app.route('/munfunction_battery_not_hold_charge')
def munfunction_battery_not_hold_charge():
    # comments = { 
    #         'nickname': 'dod',
    #         'date': '21.05.2022 в 09:22',
    #         'comment': 'кто тебя звал????'
    #     }
    #comments = [{'id': 4, 'user_name': 'YYsdfgfiu', 'comment': 'aqw', 'datetime': datetime(2023, 3, 4, 10, 42, 51)}, {'id': 5, 'user_name': '', 'comment': 'ferfre', 'datetime': datetime(2023, 3, 4, 11, 1, 49)}]
    comments = show_comment()
    comment_count = len(comments)
    return render_template("munfunction_battery_not_hold_charge.html", comment_count = comment_count, comments = comments)


if __name__ == "__main__": # Условия для точки входа (если запускаем этот файл, то функция app.run выполняется)
    app.run(debug = True) # При True выводит ошибки (поменять потом на False)