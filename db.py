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
        return connect
        

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
        return data


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
                cursor.execute("""SELECT * FROM `pages` WHERE id=%s""", (id)) # Получение страницы, получить название
                data = cursor.fetchall()
        except Exception as error:
            print(f"error_show_page {error}") # Вывод ошибок
        finally: # Выполнить в любом случае, даже с ошибками
            connect.commit() # Сохранить данные в БД
            connect.close() # Закрыть БД
        return data


    def show_page_malfunction(self, title): # Функция показа страницы
        try:
            connect = self.db_connect() # Подключение к БД
            with connect.cursor() as cursor:
                cursor.execute("""SELECT * FROM `pages` WHERE title=%s""", (title)) # Получение страницы, получить название
                data = cursor.fetchall()
        except Exception as error:
            print(f"error_show_page {error}") # Вывод ошибок
        finally: # Выполнить в любом случае, даже с ошибками
            connect.commit() # Сохранить данные в БД
            connect.close() # Закрыть БД
        return data


    def show_list_malfunction(self, place): # Функция показа неисправностей навесного оборудования и двигателя
        try:
            connect = self.db_connect() # Подключение к БД
            with connect.cursor() as cursor:
                cursor.execute("""SELECT * FROM `pages` WHERE place=%s""", (place)) # Получение страниц с неисправностями по навесному оборудованию
                data = cursor.fetchall()
        except Exception as error:
            print(f"error_show_page {error}") # Вывод ошибок
        finally: # Выполнить в любом случае, даже с ошибками
            connect.commit() # Сохранить данные в БД
            connect.close() # Закрыть БД
        return data


    def show_intresting_story(self): # Функция показа интересных историй на главной странице
        try:
            connect = self.db_connect() # Подключение к БД
            with connect.cursor() as cursor:
                cursor.execute("""SELECT * FROM `intresting_stories` ORDER BY RAND() LIMIT 1""") # Получение страниц с интересными историями
                data = cursor.fetchall()
        except Exception as error:
            print(f"error_show_page {error}") # Вывод ошибок
        finally: # Выполнить в любом случае, даже с ошибками
            connect.commit() # Сохранить данные в БД
            connect.close() # Закрыть БД
        return data