from django.db import connection
import datetime



class Search:
    def __init__(self, egzemplarz_id, ksiazka_id, tytul, isbn, jezyk, wydawca, imie_autora, nazwisko_autora, numer_alejki, numer_polki, pozycja_na_polce):
        if len(str(isbn)) != 13 and len(str(isbn)) != 10:
            raise ValueError(f'Incorrect ISBN number. 13 or 10 digit ISBN numbers accepted')
        self.egzemplarz_id = egzemplarz_id
        self.ksiazka_id = ksiazka_id
        self.tytul = tytul
        self.isbn = isbn
        self.jezyk = jezyk
        self.wydawca = wydawca
        self.imie_autora = imie_autora
        self.nazwisko_autora = nazwisko_autora 
        self.numer_alejki = numer_alejki
        self.numer_polki = numer_polki
        self.pozycja_na_polce = pozycja_na_polce

    def show_search(filters):
        with connection.cursor() as cursor:
            # print(filters)
            query = "select * from wyszukaj_ksiazke"
            flag_where = 0
            # print(filters.values())
            if None not in filters.values():
                for key in filters.keys():
                    if filters[key] != '' and key != "kategoria":
                        if flag_where == 0:
                            query += ' where '
                            flag_where = 1
                        else:
                            query += ' and '
                        query += '{} = "{}"'.format(key, filters[key])
                    if key == "kategoria":
                        
                        if filters[key] != '' and filters[key] is not None:
                            query_1 = '''select egzemplarz_id, ksiazka_id, tytul,
                            isbn, jezyk, wydawca, imie_autora, nazwisko_autora,
                            numer_alejki, numer_polki, pozycja_na_polce,
                            k.nazwa AS kategoria from ('''
                            query_2 = query
                            query_3 = ') wk INNER JOIN kategoryzacja ka ON (ka.ksiazka_ksiazka_id = wk.ksiazka_id) INNER JOIN kategoria k ON (ka.kategoria_kategoria_id = k.kategoria_id) where k.nazwa = "{}"'.format(filters[key])
                            query = query_1 + query_2 + query_3
                            # print('kategoria wybrana')
            query += " order by egzemplarz_id;"
            # print(query)
            cursor.execute(query)
            list_of_books = []
            while True:
                book = cursor.fetchone()
                if book is None:
                    break
                book = Search(book[0], book[1], book[2], book[3], book[4], book[5], book[6], book[7], book[8], book[9], book[10])
                list_of_books.append(book)
            return Search.divide_copies(list_of_books)

    def divide_copies(list_of_books):
        with connection.cursor() as cursor:
            available_copies = []
            borrowed_copies = []
            available_copies_id = []
            query ="select egzemplarz_id from wyszukaj_ksiazke as wk \
where wk.egzemplarz_id NOT IN (SELECT egzemplarz_egzemplarz_id FROM rezerwacja) \
and  wk.egzemplarz_id NOT IN (SELECT egzemplarz_egzemplarz_id FROM wypozyczenie)"
            # query = f"select egzemplarz_id from egzemplarz e join wypozyczenie w ON e.egzemplarz_id=w.egzemplarz_egzemplarz_id" \
            #         f" where w.data_wypozyczenia < DATE_ADD(now(),interval 1 hour) and w.data_oddania > DATE_ADD(now(),interval 1 hour);"
            cursor.execute(query)
            while True:
                egzamplarz_id = cursor.fetchone()
                if egzamplarz_id is None:
                    break
                available_copies_id.append(egzamplarz_id[0])
            for book in list_of_books:
                if book.egzemplarz_id in available_copies_id:
                    available_copies.append(book)
                else:
                    borrowed_copies.append(book)
        return available_copies, borrowed_copies

    def get_languages():
        with connection.cursor() as cursor:
            cursor.execute("select nazwa from jezyk;")
            list_of_languages = []
            while True:
                language = cursor.fetchone()
                if language is None:
                    return list_of_languages
                language = language[0]
                list_of_languages.append(language)

    def get_publishers():
        with connection.cursor() as cursor:
            cursor.execute("select nazwa from wydawca;")
            list_of_publishers = []
            while True:
                publisher = cursor.fetchone()
                if publisher is None:
                    return list_of_publishers
                publisher = publisher[0]
                list_of_publishers.append(publisher)

    def get_categories():
        with connection.cursor() as cursor:
            cursor.execute("select nazwa from kategoria;")
            list_of_categories = []
            while True:
                category = cursor.fetchone()
                if category is None:
                    return list_of_categories
                category = category[0]
                list_of_categories.append(category)
