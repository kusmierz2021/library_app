from django.db import connection

class Rental:
    def __init__(self, rental_id, date_rented, date_returned,
                 employee_id, client_id, copy_id):
        self.rental_id = rental_id
        self.date_rented = date_rented
        self.date_returned = date_returned
        self.employee_id = employee_id
        self.client_id = client_id
        self.copy_id = copy_id

    def show_rentals():
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM wypozyczenie")
            rentals = []
            while True:
                rental = cursor.fetchone()
                if rental is None:
                    return rentals
                rental = Rental(rental[0], rental[1],
                                rental[2], rental[3],
                                rental[4], rental[5])
                rentals.append(rental)
    
    def add_rental(client_id, employee_id, book_copy_id):
        with connection.cursor() as cursor:
            query = (
                "CALL wypozycz_ksiazke (%s, %s, %s)"
            )

            data = (book_copy_id, client_id, employee_id)
            cursor.execute(query, data)
