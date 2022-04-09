import datetime
from django.db import connection


class Statistic:

    def get_last_x_dates(self, x):
        base = datetime.datetime.today()
        datetime_list = [base - datetime.timedelta(days=x) for x in range(x)]
        dates=[]
        for d in datetime_list:
            dates.append(d.strftime('%d-%m-%Y'))
        return dates

    def get_rentals_last_ndays(self, ndays):
        with connection.cursor() as cursor:
            query = "select count(wypozyczenie_id), data_wypozyczenia from historia_wypozyczen where data_wypozyczenia >= ( SYSDATE() - INTERVAL"
            query += f" {ndays-1} DAY ) group by data_wypozyczenia;"
            cursor.execute(query)
            list_counted_rentals = [0]*ndays
            d0 = datetime.date.today()
            while True:
                tick = cursor.fetchone()
                if tick is None:
                    return list_counted_rentals
                delta = (d0-tick[1].date()).days
                list_counted_rentals[delta] = tick[0]

    def get_reservations_last_ndays(self, ndays):
        with connection.cursor() as cursor:
            query = "select count(klient_klient_id),czas_rezerwacji - INTERVAL 7 DAY as poczatek from historia_rezerwacji where czas_rezerwacji - INTERVAL 7 DAY >= ( CURDATE() - INTERVAL"
            query += f" {ndays-1} DAY ) group by czas_rezerwacji;"
            cursor.execute(query)
            list_counted_rentals = [0]*ndays
            d0 = datetime.date.today()
            while True:
                tick = cursor.fetchone()
                if tick is None:
                    return list_counted_rentals
                delta = (d0-tick[1].date()).days
                list_counted_rentals[delta] = tick[0]

    def get_available_books_last_ndays(self, ndays):
        with connection.cursor() as cursor:
            query = "select count(*) from egzemplarz;"
            cursor.execute(query)
            c = cursor.fetchone()
            book_count = c[0]
            d0 = datetime.date.today()
            available_books = []
            for i in range(ndays):
                date = d0.strftime("%Y-%m-%d %H:%M:%S")
                query2 = f"select count(*) from egzemplarz e join historia_wypozyczen w ON e.egzemplarz_id=w.egzemplarz_egzemplarz_id" \
                         f" where w.data_oddania >='{date}' and w.data_wypozyczenia <='{date}';"
                cursor.execute(query2)
                c = cursor.fetchone()
                rent = c[0]
                query3 = f"select count(*) from egzemplarz e join historia_rezerwacji r ON e.egzemplarz_id=r.egzemplarz_egzemplarz_id" \
                         f" where r.czas_rezerwacji >='{date}' and r.czas_rezerwacji - INTERVAL 7 DAY <='{date}';"
                cursor.execute(query3)
                c = cursor.fetchone()
                d0 -= datetime.timedelta(1)
                available_books.append(book_count-rent-c[0])
            return available_books
