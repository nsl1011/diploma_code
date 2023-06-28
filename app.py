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
            if (len(login) > 0) and (len(password) > 0): # Если длина логина и пароля > 0
                if check_password: # Если авторизация пройдена
                    response = make_response(render_template("profile.html", data_profile = data_profile)) # Переход на профиль, если куки сохранены
                    response.set_cookie('username', login) # Куки сохраняет логин польователя
                    return response # Возвращение переменной response
                else: # Иначе вернуть страницу авторизации, если авторизация не прошла
                    flash('Неверный логин или пароль') # Вывод окна с сообщением
                    return render_template("authorization.html") # Вернуть страницу авторизации
            else: # Иначе вернуть страницу авторизации, если длина логина или пароя < 0
                    flash('Длина логина или пароля < 0') # Вывод окна с сообщением
                    return render_template("authorization.html") # Вернуть страницу авторизации
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
        key_word = request.args.get('user_key_word') # Получение кодового слова
        button_registration = request.args.get('button_registration') # Получение кнопки "Зарегистрироваться"
        button_authorization = request.args.get('button_authorization') # Получение кнопки "Авторизоваться"
        if button_registration == 'Зарегистрироваться': # Если кнопка нажата
            if len(login) > 0: # Если длина логина > 0
                check_user = db_worker.check_user(login) # Функция для проверки наличия пользователя
                if check_user == True: # Если пользователь с данным логиным уже существует
                    flash('Логин уже существует') # Вывод окна с сообщением
                    return render_template("registration.html") # Вернуть страницу регистрации
                else:
                    if (password == password_omt) and (len(password) > 0) and (len(password_omt) > 0) and (len(key_word) > 0): # Если пароли при регистрации совпадают и пароль имеет длину больше 0
                        db_worker.add_user(login, password, key_word) # Функция для добавляения пользователя
                        data_profile = db_worker.show_profile(login) # Функция для передачи данных о пользователе на страницу профиля
                        response = make_response(render_template("profile.html", data_profile = data_profile)) # Переход на профиль, если куки сохранены
                        response.set_cookie('username', login) # Куки сохраняет логин польователя
                        return response # Возвращение переменной response
                    else:
                        flash('Пароли не совпадают') # Вывод окна с сообщением
                        return render_template("registration.html") # Вернуть страницу регистрации
        if button_authorization == 'Авторизоваться': # Если кнопка нажата
            return redirect('/authorization') # Вернуть страницу авторизации


@app.route('/profile') # Обработка страницы профиля
def profile(): # Функция для обработки страницы профиля
    login = request.cookies.get('username') # Получение логина из куки
    if login: # Если пользователь авторизован
        data_profile = db_worker.show_profile(login) # Получение данных о пользователе черз логин
        return render_template("profile.html", data_profile = data_profile) # Возвращение страницы профиля
    else: # Если пользователь не авторизован
        return render_template("authorization.html") # Возвращение страницы авторизации


@app.route('/change_password') # Обработка страницы смены пароля
def change_password(): # Функция для обработки страницы смены пароля
    return render_template("change_password.html") # Возвращение страницы смены пароля


@app.route('/form_button_change_password', methods=["GET"]) # Ссылка на form_change_password
def form_button_change_password(): # Функция для смены пароля
    if request.method == "GET": # Условие: если запрос метода GET
        button_change_password = request.args.get('button_change_password') # Получение значения кнопки смена пароля
        if button_change_password == 'Сменить пароль': # Если кнопка нажата
            return render_template("change_password.html") # Возвращение страницы смены пароля


@app.route('/form_logout', methods=["GET"]) # Ссылка на form_logout
def form_logout(): # Функция для выхода из профиля
    if request.method == "GET": # Условие: если запрос метода GET
        logout = request.args.get('button_logout') # Получение значения кнопки выхода из профиля
        if logout == 'Выйти из профиля': # Если кнопка нажата
            response = make_response(render_template("authorization.html")) # Вернуть страницу авторизации
            response.set_cookie('username', '', expires = 0) # Очистить куки
            return response # Возвращение переменной response


@app.route('/form_change_password', methods=["GET"]) # Ссылка на form_change_password
def form_change_password(): # Функция для смены пароля
    if request.method == "GET": # Условие: если запрос метода GET
        login = request.cookies.get('username') # Получение логина из куки
        user_old_password = request.args.get('user_old_password') # Получение старого пароля пользователя
        user_new_password = request.args.get('user_new_password') # Получение нового пароля пользователя
        user_new_password_omt = request.args.get('user_new_password_omt') # Получение нового пароля пользователя повторно
        user_key_word = request.args.get('user_key_word') # Получение кодового слова
        button_change_password = request.args.get('button_change_password') # Получение значения кнопки смены пароля
        button_back = request.args.get('button_back') # Получение значения кнопки назад
        check_password = db_worker.check_password(login, user_old_password) # Фунцкия для сравнения паролей пользователя
        if button_change_password == 'Сменить пароль': # Если кнопка нажата
            if (len(user_old_password) > 0) and (len(user_new_password) > 0) and (len(user_new_password_omt) > 0): # Если длина старого и нового пароля > 0
                if check_password: # Если пароли совпадают
                    if user_new_password == user_new_password_omt: # Если новый пароль и введенный повторно совпадают
                        if db_worker.check_key_word(login, user_key_word): # Если кодовое слово совпадает
                            db_worker.change_password(login, user_new_password) # Фунцкия смены пароля
                            data_profile = db_worker.show_profile(login) # Функция для передачи данных о пользователе на страницу профиля
                            flash('Пароль изменен') # Вывод окна с сообщением
                            return render_template("profile.html", data_profile = data_profile) # Возвращение страницы профиля
                        else:
                            flash('Кодовое слово не совпадает') # Вывод окна с сообщением
                            return render_template("change_password.html") # Вернуть страницу смены пароля
                    else:
                        flash('Пароли не совпадают') # Вывод окна с сообщением
                        return render_template("change_password.html") # Вернуть страницу смены пароля
                else:
                    flash('Старый пароль не совпадает') # Вывод окна с сообщением
                    return render_template("change_password.html") # Вернуть страницу смены пароля
            else:
                flash('Длина пароля < 0') # Вывод окна с сообщением
                return render_template("change_password.html") # Вернуть страницу смены пароля
        if button_back == 'Назад': # Если кнопка нажата
            return render_template("profile.html") # Возвращение страницы профиля


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
def form_show_page_engine(): # Функция для показа страницы после выбора неисправности из двигателя
    if request.method == "GET": # Условие: если запрос метода GET
        id = request.args.get('id') # Получение id с фронта в переменную id
        session['page_id'] = id # Присваивание id к сессии с page_id
        page = db_worker.show_page(id) # Вызов функции show_page (показ страницы)
        comments = db_worker.show_comments(id) # Вызов функции show_comments (вывод комментариев, которые привязаны к определенной странице)
        comment_count = len(comments) # Количество комментариев на странице
    return render_template("malfunction_base.html", page = page, comments = comments, comment_count = comment_count) # Возвращение страницы со всеми переменными


@app.route('/survey') # Обработка страницы опроса
def survey_start(): # Функция для обработки страницы опроса со стартовым вопросом
    data = survey_worker.survey_yes_no() # Вызов функции show_survey_yes_no (начальный вопрос опроса)
    return render_template("survey.html", data = data) # Возвращение страницы со всеми переменными


@app.route('/form_survey', methods=["GET"]) # Ссылка на form_survey
def survey_vote(): # Функция для обработки ответов в опросе
    vote = request.args.get('answer') # Получение ответа на вопрос с фронта в переменную vote
    if request.method == "GET": # Условие: если запрос метода GET
        if vote == 'Запускается': # Если нажата кнопка
            data = survey_worker.survey_yes_1() # Вывести начальный вопрос
            return render_template("survey.html", data = data) # Вернуть страницу опроса
        
        # Ветвление если двигатель запускается
        if vote == 'Не устойчиво': # Если нажата кнопка
            id = 13 # Присвоить id значение
            session['page_id'] = id # Присваивание сессии id
            page = db_worker.show_page(id) # Вызов функции show_page (показ страницы)
            comments = db_worker.show_comments(id) # Вызов функции show_comments (вывод комментариев, которые привязаны к определенной странице)
            comment_count = len(comments) # Количество комментариев на странице
            return render_template("malfunction_base.html", page = page, comments = comments, comment_count = comment_count) # Возвращение страницы неисправности
        if vote == 'Устойчиво': # Если нажата кнопка
            data = survey_worker.survey_yes_2() # Вывести следующий вопрос
            return render_template("survey.html", data = data) # Вернуть страницу опроса
        if vote == 'Да': # Если нажата кнопка
            id = 15 # Присвоить id значение
            session['page_id'] = id # Присваивание сессии id
            page = db_worker.show_page(id) # Вызов функции show_page (показ страницы)
            comments = db_worker.show_comments(id) # Вызов функции show_comments (вывод комментариев, которые привязаны к определенной странице)
            comment_count = len(comments) # Количество комментариев на странице
            return render_template("malfunction_base.html", page = page, comments = comments, comment_count = comment_count) # Возвращение страницы неисправности
        if vote == 'Нет': # Если нажата кнопка
            data = survey_worker.survey_yes_3() # Вывести следующий вопрос
            return render_template("survey.html", data = data) # Вернуть страницу опроса
        if vote == 'Ощущается': # Если нажата кнопка
            id = 17 # Присвоить id значение
            session['page_id'] = id # Присваивание сессии id
            page = db_worker.show_page(id) # Вызов функции show_page (показ страницы)
            comments = db_worker.show_comments(id) # Вызов функции show_comments (вывод комментариев, которые привязаны к определенной странице)
            comment_count = len(comments) # Количество комментариев на странице
            return render_template("malfunction_base.html", page = page, comments = comments, comment_count = comment_count) # Возвращение страницы неисправности
        if vote == 'Не ощущается': # Если нажата кнопка
            id = 19 # Присвоить id значение
            session['page_id'] = id # Присваивание сессии id
            page = db_worker.show_page(id) # Вызов функции show_page (показ страницы)
            comments = db_worker.show_comments(id) # Вызов функции show_comments (вывод комментариев, которые привязаны к определенной странице)
            comment_count = len(comments) # Количество комментариев на странице
            return render_template("malfunction_base.html", page = page, comments = comments, comment_count = comment_count) # Возвращение страницы неисправности

        # Ветвление если двигатель не запускается
        if vote == 'Не запускается': # Если нажата кнопка
            data = survey_worker.survey_no_1() # Вывести следующий вопрос
            return render_template("survey.html", data = data) # Вернуть страницу опроса
        if vote == 'Не крутит': # Если нажата кнопка
            id = 5 # Присвоить id значение
            session['page_id'] = id # Присваивание сессии id
            page = db_worker.show_page(id) # Вызов функции show_page (показ страницы)
            comments = db_worker.show_comments(id) # Вызов функции show_comments (вывод комментариев, которые привязаны к определенной странице)
            comment_count = len(comments) # Количество комментариев на странице
            return render_template("malfunction_base.html", page = page, comments = comments, comment_count = comment_count) # Возвращение страницы неисправности
        if vote == 'Крутит': # Если нажата кнопка
            data = survey_worker.survey_no_2() # Вывести следующий вопрос
            return render_template("survey.html", data = data) # Вернуть страницу опроса
        if vote == 'Плохо': # Если нажата кнопка
            id = 7 # Присвоить id значение
            session['page_id'] = id # Присваивание сессии id
            page = db_worker.show_page(id) # Вызов функции show_page (показ страницы)
            comments = db_worker.show_comments(id) # Вызов функции show_comments (вывод комментариев, которые привязаны к определенной странице)
            comment_count = len(comments) # Количество комментариев на странице
            return render_template("malfunction_base.html", page = page, comments = comments, comment_count = comment_count) # Возвращение страницы неисправности
        if vote == 'Хорошо': # Если нажата кнопка
            data = survey_worker.survey_no_3() # Вывести следующий вопрос
            return render_template("survey.html", data = data) # Вернуть страницу опроса
        if vote == 'Не имеется': # Если нажата кнопка
            id = 9 # Присвоить id значение
            session['page_id'] = id # Присваивание сессии id
            page = db_worker.show_page(id) # Вызов функции show_page (показ страницы)
            comments = db_worker.show_comments(id) # Вызов функции show_comments (вывод комментариев, которые привязаны к определенной странице)
            comment_count = len(comments) # Количество комментариев на странице
            return render_template("malfunction_base.html", page = page, comments = comments, comment_count = comment_count) # Возвращение страницы неисправности
        if vote == 'Имеется': # Если нажата кнопка
            id = 11 # Присвоить id значение
            session['page_id'] = id # Присваивание сессии id
            page = db_worker.show_page(id) # Вызов функции show_page (показ страницы)
            comments = db_worker.show_comments(id) # Вызов функции show_comments (вывод комментариев, которые привязаны к определенной странице)
            comment_count = len(comments) # Количество комментариев на странице
            return render_template("malfunction_base.html", page = page, comments = comments, comment_count = comment_count) # Возвращение страницы неисправности


if __name__ == "__main__": # Условия для точки входа (если запускаем этот файл, то функция app.run выполняется)
    app.run(debug = True) # При True выводит ошибки (поменять потом на False)