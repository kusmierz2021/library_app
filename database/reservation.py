from django.db import connection

class Reservation:
    def __init__(self, copy_id, date_valid, client_id):
        self.copy_id = copy_id
        self.date_valid= date_valid
        self.client_id = client_id

    def show_reservations():
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM rezerwacja")
            reservations = []
            while True:
                reservation = cursor.fetchone()
                if reservation is None:
                    return reservations
                reservation = Reservation(reservation[0], reservation[1], reservation[2])
                reservations.append(reservation)

    def add_reservation(book_copy_id, client_id):
        with connection.cursor() as cursor:
            query = (
                "CALL dodaj_rezerwacje (%s, %s)"
            )

            data = (book_copy_id, client_id)
            cursor.execute(query, data)
    
    def remove_reservation(copy_id):
        with connection.cursor() as cursor:
            cursor.callproc('usun_rezerwacje', [copy_id])
