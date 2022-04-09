from django.db import connection
from datetime import datetime, timedelta


class Book:
    def __init__(self, tytul, isbn, jezyk_id, wydawca_id, ksiazka_id=None):
        if len(str(isbn)) != 13 and len(str(isbn)) != 10:
            raise ValueError(f'Incorrect ISBN number. 13 or 10 digit ISBN numbers accepted')
        self.ksiazka_id = ksiazka_id
        self.tytul = tytul
        self.isbn = isbn
        self.jezyk_id = jezyk_id
        self.wydawca_id = wydawca_id

    def add_book(self, author_id):
        with connection.cursor() as cursor:
            query = (
                "CALL dodaj_ksiazke(%s,%s, %s, %s, %s);"
                
            )

            data = (self.tytul, self.isbn, self.jezyk_id, self.wydawca_id, author_id)  # BUG: missing book.lokalizacja_id in database
            cursor.execute(query, data)

    def show_books():
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM ksiazka")
            list_of_books = []
            while True:
                book = cursor.fetchone()
                if book is None:
                    return list_of_books
                book = Book(book[1], book[2], book[3], book[4], book[0])
                list_of_books.append(book)

    def delete_book(book_id):
        with connection.cursor() as cursor:
            query = (
                "DELETE FROM ksiazka WHERE ksiazka_id = %s"
            )
            cursor.execute(query, (book_id,))

    def return_book(rental_id):
        with connection.cursor() as cursor:
            cursor.callproc('usun_wypozyczenie', [rental_id])

    def extend_book_rental(rental_id):
        with connection.cursor() as cursor:
            extended_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
            cursor.callproc('przedluz_wypozyczenie', [extended_date, rental_id])
