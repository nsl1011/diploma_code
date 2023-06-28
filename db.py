import pymysql

class DB:
    def db_connect(self): # Функция для подключения к БД
        try:
            connect = pymysql.connect(
            host = "pari2020.beget.tech",
            user = "pari2020_comment",
            password = "Q12345!",
            database = "pari2020_comment",
            cursorclass = pymysql.cursors.DictCursor # Тип данных возвращаемых данных (словарь)
        )
        except Exception as connect_error:
            print(f"Connect error: {connect_error}")
        return connect # Вернуть connect
        

    def add_comment(self, comment, page_id): # Функция добавления комментария в БД
        try:
            connect = self.db_connect() # Подключение к БД
            with connect.cursor() as cursor:
                cursor.execute("""INSERT INTO `comments` (`comment`, `page_id`) value(%s, %s)""", (comment, page_id)) # Добавление в БД комментария
        except Exception as error:
            print(f"error_add_comment {error}") # Вывод ошибок
        finally: # Выполнить в любом случае, даже с ошибками
            connect.commit() # Сохранить данные в БД
            connect.close() # Закрыть БД


    def show_comments(self, id): # Функция вывода комментария на странице
        try:
            connect = self.db_connect() # Подключение к БД
            with connect.cursor() as cursor: 
                cursor.execute("""SELECT * FROM `comments` WHERE page_id=%s""", (id,)) # Получение комментария
                data = cursor.fetchall()
        except Exception as error:
            print(f"error_add_comment {error}") # Вывод ошибок
        finally: # Выполнить в любом случае, даже с ошибками
            connect.commit() # Сохранить данные в БД
            connect.close() # Закрыть БД
        return data # Вернуть data


    def delete_comment(self, id): # Функция удаления комментария в БД
        try:
            connect = self.db_connect() # Подключение к БД
            with connect.cursor() as cursor:
                cursor.execute("""DELETE FROM `comments` WHERE id=%s""", (id,)) # Удаление комментария из БД
        except Exception as error:
            print(f"error_add_comment {error}") # Вывод ошибок
        finally: # Выполнить в любом случае, даже с ошибками
            connect.commit() # Сохранить данные в БД
            connect.close() # Закрыть БД


    def show_page(self, id): # Функция показа страницы
        try:
            connect = self.db_connect() # Подключение к БД
            with connect.cursor() as cursor:
                cursor.execute("""SELECT * FROM `pages` WHERE id=%s""", (id)) # Получение страницы из БД
                data = cursor.fetchall()
        except Exception as error:
            print(f"error_show_page {error}") # Вывод ошибок
        finally: # Выполнить в любом случае, даже с ошибками
            connect.commit() # Сохранить данные в БД
            connect.close() # Закрыть БД
        return data # Вернуть data


    def show_page_malfunction(self, title): # Функция показа страницы неисправности
        try:
            connect = self.db_connect() # Подключение к БД
            with connect.cursor() as cursor:
                cursor.execute("""SELECT * FROM `pages` WHERE title=%s""", (title)) # Получение страницы из БД
                data = cursor.fetchall()
        except Exception as error:
            print(f"error_show_page {error}") # Вывод ошибок
        finally: # Выполнить в любом случае, даже с ошибками
            connect.commit() # Сохранить данные в БД
            connect.close() # Закрыть БД
        return data # Вернуть data


    def show_list_malfunction(self, place): # Функция показа неисправностей навесного оборудования и двигателя
        try:
            connect = self.db_connect() # Подключение к БД
            with connect.cursor() as cursor:
                cursor.execute("""SELECT * FROM `pages` WHERE place=%s""", (place)) # Получение страниц с неисправностями по навесному оборудованию и двигателю
                data = cursor.fetchall()
        except Exception as error:
            print(f"error_show_page {error}") # Вывод ошибок
        finally: # Выполнить в любом случае, даже с ошибками
            connect.commit() # Сохранить данные в БД
            connect.close() # Закрыть БД
        return data # Вернуть data


    def show_intresting_story(self): # Функция показа историй на главной странице
        try:
            connect = self.db_connect() # Подключение к БД
            with connect.cursor() as cursor:
                cursor.execute("""SELECT * FROM `intresting_stories` ORDER BY RAND() LIMIT 1""") # Получение страниц с историями
                data = cursor.fetchall()
        except Exception as error:
            print(f"error_show_page {error}") # Вывод ошибок
        finally: # Выполнить в любом случае, даже с ошибками
            connect.commit() # Сохранить данные в БД
            connect.close() # Закрыть БД
        return data # Вернуть data


    def check_password(self, login, password): # Функция сверки пароля
        try:
            connect = self.db_connect() # Подключение к БД
            with connect.cursor() as cursor:
                cursor.execute("""SELECT user_password FROM `users` WHERE user_name=%s""", (login)) # Получение пароля о пользователе по логину
                user_password = cursor.fetchall()
                if str(user_password[0]['user_password']) == str(password): # Если пароли совпадают
                    return True # Вернуть True
                return False # Вернуть False
        except Exception as error:
            print(f"error_show_page {error}") # Вывод ошибок
            return False
        finally: # Выполнить в любом случае, даже с ошибками
            connect.commit() # Сохранить данные в БД
            connect.close() # Закрыть БД


    def show_profile(self, login): # Функция получения информации о пользователе
        try:
            connect = self.db_connect() # Подключение к БД
            with connect.cursor() as cursor:
                cursor.execute("""SELECT * FROM `users` WHERE user_name=%s""", (login)) # Получение информации о пользователе
                data = cursor.fetchall()
        except Exception as error:
            print(f"error_show_page {error}") # Вывод ошибок
        finally: # Выполнить в любом случае, даже с ошибками
            connect.commit() # Сохранить данные в БД
            connect.close() # Закрыть БД
        return data # Вернуть data


    def add_user(self, login, password, key_word): # Функция добавления пользователя в БД
        try:
            connect = self.db_connect() # Подключение к БД
            with connect.cursor() as cursor:
                cursor.execute("""INSERT INTO `users` (`user_name`, `user_password`, `key_word`) value(%s, %s, %s)""", (login, password, key_word)) # Добавление пользователя в БД
        except Exception as error:
            print(f"error_add_comment {error}") # Вывод ошибок
        finally: # Выполнить в любом случае, даже с ошибками
            connect.commit() # Сохранить данные в БД
            connect.close() # Закрыть БД


    def check_user(self, login): # Функция проверки наличия пользователя в БД
        try:
            connect = self.db_connect() # Подключение к БД
            with connect.cursor() as cursor:
                if cursor.execute("""SELECT user_name FROM `users` WHERE user_name=%s""", (login)): # Проверка наличия пользователя
                    return True  # Вернуть True
                else:
                    return False # Вернуть False
        except Exception as error:
            print(f"error_show_page {error}") # Вывод ошибок
            return False # Вернуть False
        finally: # Выполнить в любом случае, даже с ошибками
            connect.commit() # Сохранить данные в БД
            connect.close() # Закрыть БД


    def check_key_word(self, login, key_word): # Функция проверки кодового слова
        try:
            connect = self.db_connect() # Подключение к БД
            with connect.cursor() as cursor:
                cursor.execute("""SELECT key_word FROM `users` WHERE user_name=%s""", (login)) # Получение кодового слова
                user_key_word = cursor.fetchall()
                if str(user_key_word[0]['key_word']) == str(key_word): # ЕСли кодовое слово совпадает
                    return True # Вернуть True
                return False # Вернуть False
        except Exception as error:
            print(f"error_show_page {error}") # Вывод ошибок
            return False # Вернуть False
        finally: # Выполнить в любом случае, даже с ошибками
            connect.commit() # Сохранить данные в БД
            connect.close() # Закрыть БД


    def change_password(self, login, new_password): # Функция смены пароя
        try:
            connect = self.db_connect() # Подключение к БД
            with connect.cursor() as cursor:
                cursor.execute("""UPDATE `users` SET user_password=%s WHERE user_name=%s""", (new_password, login)) # Обновление пароля пользователя
        except Exception as error:
            print(f"error_show_page {error}") # Вывод ошибок
            return False # Вернуть False
        finally: # Выполнить в любом случае, даже с ошибками
            connect.commit() # Сохранить данные в БД
            connect.close() # Закрыть БД