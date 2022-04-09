from django.db import connection


class Author:
    def __init__(self, imie, nazwisko, autor_id=None):
        self.autor_id = autor_id
        self.imie = imie
        self.nazwisko = nazwisko

    def add_autor(imie, nazwisko):
        with connection.cursor() as cursor:
            query = (
                "INSERT INTO autor (imie, nazwisko)"
                "values (%s, %s)"
            )

            data = (imie, nazwisko)
            cursor.execute(query, data)

    def show_autors():
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM autor")
            list_of_autors = []
            while True:
                autor = cursor.fetchone()
                if autor is None:
                    return list_of_autors
                autor = Author(autor[1], autor[2], autor[0])
                list_of_autors.append(autor)

    def delete_autor(autor_id):
        with connection.cursor() as cursor:
            query = (
                "DELETE FROM autor WHERE autor_id = %s"
            )
            cursor.execute(query, (autor_id,))
