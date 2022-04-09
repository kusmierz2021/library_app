from django.db import connection
from database.account import Account
from database.book import Book


class Database:
    def __init__(self):
        pass

    def check_password(self, login, password):
        with connection.cursor() as cursor:
            query = (
                "select login, haslo from pracownik p inner join konto k on (p.konto_konto_id = k.konto_id)"
            )

            cursor.execute(query)
            list_of_log_psw = []
            while True:
                log_psw = cursor.fetchone()
                if log_psw is None:
                    if (login, password) in list_of_log_psw:
                        return 'admin'
                    else:
                        return 'error_login'
                list_of_log_psw.append(log_psw)
