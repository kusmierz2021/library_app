from django.db import connection


class Account:
    def __init__(self, login, haslo, imie, nazwisko, email, numer_telefonu, konto_id=None):
        self.konto_id = konto_id
        self.login = login
        self.haslo = haslo
        self.imie = imie
        self.nazwisko = nazwisko
        self.email = email
        self.numer_telefonu = numer_telefonu

    def get_info(self):
        return f'{self.konto_id} {self.login} {self.haslo} {self.imie} {self.nazwisko} {self.email} {self.numer_telefonu}'

    def add_account(self, is_admin):  # is_admin = None or on
        with connection.cursor() as cursor:
            if is_admin == 'on':
                query = (
                         "CALL dodaj_konto_pracownika(%s, %s, %s, %s, %s, %s)"
                        )
            else:
                query = (
                         "CALL dodaj_konto_klienta(%s, %s, %s, %s, %s, %s)"
                        )
            # query = (
            #     "INSERT INTO konto (login, haslo, imie, nazwisko, email, numer_telefonu)"
            #     "values (%s, %s, %s, %s, %s, %s)"
            # )
            
            data = (self.login, self.haslo, self.imie, self.nazwisko, self.email, self.numer_telefonu)
            cursor.execute(query, data)

    def delete_account(konto_id):
        with connection.cursor() as cursor:
            query = (
                "CALL del_account(%s)"
            )
            cursor.execute(query, (konto_id,))

    def show_pracownik(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT konto_konto_id from pracownik")
            list_of_pracownik_id = []
            while True:
                pracownik_id = cursor.fetchone()
                if pracownik_id is None:
                    return Account.show_accounts(list_of_pracownik_id)
                list_of_pracownik_id.append(pracownik_id[0])

    def show_klient(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT konto_konto_id from klient")
            list_of_klient_id = []
            while True:
                klient_id = cursor.fetchone()
                if klient_id is None:
                    return Account.show_accounts(list_of_klient_id)
                list_of_klient_id.append(klient_id[0])

    def show_accounts(list_of_account_id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM konto")
            list_of_accounts = []
            while True:
                account = cursor.fetchone()
                if account is None:
                    return list_of_accounts
                if (account[0] in list_of_account_id):
                    account = Account(account[1], account[2], account[3], account[4], account[5], account[6], account[0])
                    list_of_accounts.append(account)

    def get_clients():
        with connection.cursor() as cursor:
            cursor.execute("select * from konto_klienta")
            return cursor.fetchall()
    
    def get_account_id_by_login(login):
        with connection.cursor() as cursor:
            query = "select pracownik_id from pracownik as p join konto as k on ( k.konto_id = p.konto_konto_id ) where k.login = %s"
            data = [login]
            cursor.execute(query, data)
            id = cursor.fetchone()
            if not id:
                return None
            else:
                return int(id[0])
