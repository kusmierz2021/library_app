from django.db import connection

class Book_copy:
    def add_copy(book,quantity,localization):
        with connection.cursor() as cursor:
            query=f"INSERT INTO egzemplarz(ksiazka_ksiazka_id,lokalizacja_lokalizacja_id) VALUES ({book[0]},{localization[0]})"
            for i in range(quantity):
                cursor.execute(query)

    def get_book_list():
        with connection.cursor() as cursor:
            query ="SELECT ksiazka_id,tytul,jezyk FROM wyszukaj_ksiazke GROUP BY ksiazka_id"
            cursor.execute(query)
            book_list=[]
            while True:
                book = cursor.fetchone()
                if book is None:
                    return book_list
                book_list.append(book)
    
    def get_available_books():
        with connection.cursor() as cursor:
            query ="select egzemplarz_id, CONCAT(tytul, ' - ', imie_autora, ' ', nazwisko_autora, '; j. ', jezyk) as info from wyszukaj_ksiazke as wk \
                    where wk.egzemplarz_id NOT IN (SELECT egzemplarz_egzemplarz_id FROM rezerwacja) \
                    and  wk.egzemplarz_id NOT IN (SELECT egzemplarz_egzemplarz_id FROM wypozyczenie)"
            cursor.execute(query)
            return cursor.fetchall()

    def get_localization_list():
        with connection.cursor() as cursor:
            query ="SELECT l.lokalizacja_id,a.numer,p.numer,p.pozycja FROM lokalizacja l LEFT JOIN alejka a ON l.alejka_alejka_id=a.alejka_id LEFT JOIN polka p ON  l.polka_polka_id=p.polka_id"
            cursor.execute(query)
            localization_list=[]
            while True:
                loc = cursor.fetchone()
                if loc is None:
                    return localization_list
                localization_list.append(loc)
