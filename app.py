# https://horo.beget.com/phpMyAdmin/index.php?db=pari2020_comment - ссылка на БД

from flask import Flask, render_template, url_for, request, redirect, session, make_response, flash # Импорт библиотек
from db import DB # Импорт класса DB из файла db.py
from survey import SURVEY # Импорт класса SURVEY из файла survey.py
from datetime import datetime # Импортир даты и времени

# import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegration
# sentry_sdk.init(
#     dsn="https://edf95c656a5644c08e7f95753ede281a@o4504514952101888.ingest.sentry.io/4504514955313152",
#     integrations=[
#         FlaskIntegration(),
#     ],

#     traces_sample_rate=1.0
# )

db_worker = DB() # Присваивание переменной класс DB
survey_worker = SURVEY() # Присваивание переменной класс SURVEY
app = Flask (__name__) # Создание экземпляра приложения и присваивание ему переменную __name__, которая содержит имя текущего файла python
app.secret_key = 'my_secret_key' # Для работы с session


@app.route('/malfunction_base') # Обработка страницы malfunction_base
def malfunction_base(): # Функция для обработки страницы malfunction_base
    id = session.get('page_id', None) # Получение page_id
    comments = db_worker.show_comments(id) # Вызов функции show_comments (вывод комментариев, которые привязаны к определенной странице)
    comment_count = len(comments) # Количество комментариев на странице
    if comment_count == 0: # Условие: если на странице нет комментариев, то значение = 0
        comment_count = 0
    page = db_worker.show_page(id) # Вызов функции show_page (показ страницы)
    return render_template("malfunction_base.html", page = page, comment_count = comment_count, comments = comments) # Возвращение страницы со всеми переменными


@app.route('/form_send', methods=["GET"]) # Ссылка на form_send
def form_send(): # Функция для получения комментария
    if request.method == "GET": # Условие: если запрос метода GET
        data = request.args.get('comment_send','') # Получение комментария с фронта в переменную data
        page_id = session.get('page_id', None) # Получение page_id
        if (len(data) > 0): # Условие, чтобы комментарий не был пустой
            db_worker.add_comment(data, page_id) # Добавляем комментарий в БД
    return redirect('/malfunction_base') # Возвращение обновленной страницы


@app.route('/form_delete', methods=["GET"]) # Ссылка на form_delete
def form_delete(): # Функция для удаления комментария
    if request.method == "GET": # Условие: если запрос метода GET
        data = request.args.get('comment_delete','') # Получение комментария с фронта в переменную data
        id = request.args.get('id','') # Получение id с фронта в переменную id
        db_worker.delete_comment(id) # Вызов функции delete_comment (удаление комментария)
    return redirect('/malfunction_base') # Возвращение обновленной страницы


@app.route('/') # Обработка главной страницы
def index(): # Функция для обработки главной страницы
    data = db_worker.show_intresting_story() # Функция для вывода истории случайным образом
    return render_template("index.html", data = data) # Возвращение главной страницы


@app.route('/authorization') # Обработка страницы авторизации
def authorization(): # Функция для обработки страницы авторизации
    return render_template("authorization.html") # Возвращение страницы авторизации


@app.route('/form_login', methods=["GET"]) # Ссылка на form_login
def form_login(): # Функция для авторизации
    if request.method == "GET": # Условие: если запрос метода GET
        login = request.args.get('user_login') # Получение логина с фронта в переменную login
        password = request.args.get('user_password') # Получение пароля с фронта в переменную password
        button_login = request.args.get('button_login') # Получение кнопки "Войти"
        button_registration = request.args.get('button_registration') # Получение кнопки "Зарегистрироваться"
        check_password = db_worker.check_password(login, password) # Фунцкия для сравнения паролей пользователя
        data_profile = db_worker.show_profile(login) # Функция для передачи данных о пользователе на страницу профиля
        if button_login == 'Войти': # Условие, если нажата кнопка "Войти"
            if check_password: # Условие, если авторизация пройдена, то вернуть страницу профиля
                response = make_response(render_template("profile.html", data_profile = data_profile)) # Переход на профиль, если куки сохранены
                response.set_cookie('username', login) # Куки сохраняет логин польователя
                return response # Возвращение переменной response
            else: # Иначе вернуть страницу авторизации, если авторизация не прошла
                flash('Неверный логин или пароль') # Вывод окна с сообщением
                return render_template("authorization.html") # Вернуть ту же страницу авторизации
        if button_registration == 'Зарегистрироваться': # Условие, если нажата кнопка "Зарегистрироваться"
            return redirect('/registration') # Вернуть страницу регистрации


@app.route('/registration') # Обработка страницы регистрации
def registration(): # Функция для обработки страницы регистрации
    return render_template("registration.html") # Возвращение страницы регистрации


@app.route('/form_registration', methods=["GET"]) # Ссылка на form_registration
def form_registration(): # Функция для регистрации
    if request.method == "GET": # Условие: если запрос метода GET
        login = request.args.get('user_login') # Получение логина с фронта в переменную login
        password = request.args.get('user_password') # Получение пароля с фронта в переменную password
        password_omt = request.args.get('user_password_omt') # Повторное получение пароля
        button_registration = request.args.get('button_registration') # Получение кнопки "Зарегистрироваться"
        button_authorization = request.args.get('button_authorization') # Получение кнопки "Авторизоваться"
        if button_registration == 'Зарегистрироваться': # Условие, если нажата кнопка "Войти"
            check_user = db_worker.check_user(login) # Функция для проверки наличия пользователя
            if check_user == True: # Если пользователь с данным логиным уже существует
                flash('Логин уже существует') # Вывод окна с сообщением
                return render_template("registration.html") # Вернуть страницу регистрации
            else:
                if password == password_omt: # Если пароли при регистрации совпадают
                    db_worker.add_user(login, password) # Функция для добавляения пользователя
                    data_profile = db_worker.show_profile(login) # Функция для передачи данных о пользователе на страницу профиля
                    response = make_response(render_template("profile.html", data_profile = data_profile, title = "Profile")) # Переход на профиль, если куки сохранены
                    response.set_cookie('username', login) # Куки сохраняет логин польователя
                    return response # Возвращение переменной response
                else:
                    flash('Пароли не совпадают') # Вывод окна с сообщением
                    return render_template("registration.html") # Вернуть ту же страницу авторизации
        if button_authorization == 'Авторизоваться': # Условие, если нажата кнопка "Зарегистрироваться"
            return redirect('/authorization') # Вернуть страницу регистрации


@app.route('/profile') # Обработка страницы профиля
def profile(): # Функция для обработки страницы профиля
    login = request.cookies.get('username') # Получение логина из куки
    if login: # Если пользователь зарегистрирован
        data_profile = db_worker.show_profile(login) # Получение данных о пользователе черз логин
        return render_template("profile.html", data_profile = data_profile) # Возвращение страницы профиля
    else: # Если пользователь не авторизован
        return render_template("authorization.html") # Возвращение страницы авторизации


@app.route('/form_logout', methods=["GET"]) # Ссылка на form_logout
def form_logout(): # Функция для выхода из профиля
    if request.method == "GET": # Условие: если запрос метода GET
        logout = request.args.get('button_logout') # Получение значения кнопки выхода из профиля
        if logout == 'Выйти из профиля': # Если кнопка нажата
            response = make_response(render_template("authorization.html")) # Вернуть страницу авторизации
            response.set_cookie('username', '', expires = 0) # Очистить куки
            return response # Возвращение переменной response


@app.route('/attachments') # Обработка страницы со списком неисправностей в навесном оборудовании
def attachments(): # Функция для обработки страницы со списком неисправностей в навесном оборудовании
    if request.method == "GET": # Условие: если запрос метода GET
        place = 'Навесное оборудование' # Присваивание переменной параметра для вывода списка страниц неисправностей именно для навесного оборудования (place)
        data = db_worker.show_list_malfunction(place) # Вызов функции show_attachments (вывод неисправностей навесного оборудования)
        return render_template("attachments.html", data = data) # Возвращение страницы со всеми переменными


@app.route('/form_show_page_attachments', methods=["GET"]) # Ссылка на form_show_page_attachments
def form_show_page_attachments(): # Функция для показа страницы после выбора неисправности из навесного оборудования
    if request.method == "GET": # Условие: если запрос метода GET
        id = request.args.get('id') # Получение id с фронта в переменную id
        session['page_id'] = id # Присваивание id к сессии с page_id
        page = db_worker.show_page(id) # Вызов функции show_page (показ страницы)
        comments = db_worker.show_comments(id) # Вызов функции show_comments (вывод комментариев, которые привязаны к определенной странице)
        comment_count = len(comments) # Количество комментариев на странице
    return render_template("malfunction_base.html", page = page, comments = comments, comment_count = comment_count) # Возвращение страницы со всеми переменными


@app.route('/engine') # Обработка страницы со списком неисправностей в двигателе
def engine(): # Функция для обработки страницы со списком неисправностей в двигателе
    if request.method == "GET": # Условие: если запрос метода GET
        place = 'Двигатель' # Присваивание переменной параметра для вывода списка страниц неисправностей именно для двигателя (place)
        data = db_worker.show_list_malfunction(place) # Вызов функции show_attachments (вывод неисправностей навесного оборудования)
        return render_template("engine.html", data = data) # Возвращение страницы со всеми переменными


@app.route('/form_show_page_engine', methods=["GET"]) # Ссылка на form_show_page_engine
def form_show_page_engine(): # Функция для показа страницы после выбора неисправности из навесного оборудования
    if request.method == "GET": # Условие: если запрос метода GET
        id = request.args.get('id') # Получение id с фронта в переменную id
        session['page_id'] = id # Присваивание id к сессии с page_id
        page = db_worker.show_page(id) # Вызов функции show_page (показ страницы)
        comments = db_worker.show_comments(id) # Вызов функции show_comments (вывод комментариев, которые привязаны к определенной странице)
        comment_count = len(comments) # Количество комментариев на странице
    return render_template("malfunction_base.html", page = page, comments = comments, comment_count = comment_count) # Возвращение страницы со всеми переменными


@app.route('/survey') # Обработка страницы опросника
def survey_start(): # Функция для обработки страницы опросниками со стартовым вопросом
    data = survey_worker.survey_yes_no() # Вызов функции show_survey_yes_no (начальный вопрос опроса)
    return render_template("survey.html", data = data) # Возвращение страницы со всеми переменными


@app.route('/form_survey', methods=["GET"]) # Ссылка на form_survey
def survey_vote(): # Функция для обработки ответов в опроснике
    vote = request.args.get('answer') # Получение ответа на вопрос с фронта в переменную vote
    if request.method == "GET": # Условие: если запрос метода GET
        if vote == 'Запускается':
            data = survey_worker.survey_yes_1()
            return render_template("survey.html", data = data)
        
        # Ветвление если двигатель запускается
        if vote == 'Не устойчиво':
            id = 13
            session['page_id'] = id
            page = db_worker.show_page(id)
            comments = db_worker.show_comments(id)
            comment_count = len(comments)
            return render_template("malfunction_base.html", page = page, comments = comments, comment_count = comment_count)
        if vote == 'Устойчиво':
            data = survey_worker.survey_yes_2()
            return render_template("survey.html", data = data)
        if vote == 'Да':
            id = 15
            session['page_id'] = id
            page = db_worker.show_page(id)
            comments = db_worker.show_comments(id)
            comment_count = len(comments)
            return render_template("malfunction_base.html", page = page, comments = comments, comment_count = comment_count)
        if vote == 'Нет':
            data = survey_worker.survey_yes_3()
            return render_template("survey.html", data = data)
        if vote == 'Ощущается':
            id = 17
            session['page_id'] = id
            page = db_worker.show_page(id)
            comments = db_worker.show_comments(id)
            comment_count = len(comments)
            return render_template("malfunction_base.html", page = page, comments = comments, comment_count = comment_count)
        if vote == 'Не ощущается':
            id = 19
            session['page_id'] = id
            page = db_worker.show_page(id)
            comments = db_worker.show_comments(id)
            comment_count = len(comments)
            return render_template("malfunction_base.html", page = page, comments = comments, comment_count = comment_count)

        # Ветвление если двигатель не запускается
        if vote == 'Не запускается':
            data = survey_worker.survey_no_1()
            return render_template("survey.html", data = data)
        if vote == 'Не крутит':
            id = 5
            session['page_id'] = id
            page = db_worker.show_page(id)
            comments = db_worker.show_comments(id)
            comment_count = len(comments)
            return render_template("malfunction_base.html", page = page, comments = comments, comment_count = comment_count)
        if vote == 'Крутит':
            data = survey_worker.survey_no_2()
            return render_template("survey.html", data = data)
        if vote == 'Плохо':
            id = 7
            session['page_id'] = id
            page = db_worker.show_page(id)
            comments = db_worker.show_comments(id)
            comment_count = len(comments)
            return render_template("malfunction_base.html", page = page, comments = comments, comment_count = comment_count)
        if vote == 'Хорошо':
            data = survey_worker.survey_no_3()
            return render_template("survey.html", data = data)
        if vote == 'Не имеется':
            id = 9
            session['page_id'] = id
            page = db_worker.show_page(id)
            comments = db_worker.show_comments(id)
            comment_count = len(comments)
            return render_template("malfunction_base.html", page = page, comments = comments, comment_count = comment_count)
        if vote == 'Имеется':
            id = 11
            session['page_id'] = id
            page = db_worker.show_page(id)
            comments = db_worker.show_comments(id)
            comment_count = len(comments)
            return render_template("malfunction_base.html", page = page, comments = comments, comment_count = comment_count)


if __name__ == "__main__": # Условия для точки входа (если запускаем этот файл, то функция app.run выполняется)
    app.run(debug = True) # При True выводит ошибки (поменять потом на False)