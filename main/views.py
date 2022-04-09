from django.shortcuts import render
from database import account, book, database, author, rental, reservation, search, plot, book_copy
from database.statistic import Statistic


employee_id = None

def home(request):
    return render(request, 'login.html')


def log(request):
    if request.method == 'POST':
        return render(request, 'login.html')


def admin(request):
    return render(request, 'master_admin.html')


def login(request):
    global employee_id
    if request.method == 'POST':
        email = request.POST.get('email')
        checked_log_pas = database.Database.check_password(None, email, request.POST.get('password'))
        if checked_log_pas == 'admin':
            employee_id = database.Account.get_account_id_by_login(email)
            return render(request, 'master_admin.html')
        elif checked_log_pas == 'error_login':
            return render(request, 'login.html', {'error_login': True})
        return render(request, 'login.html')


def add_account(request):
    if request.POST.get('login') is not None:
        new_account = account.Account(request.POST.get('login'),
                                      request.POST.get('haslo'),
                                      request.POST.get('imie'),
                                      request.POST.get('nazwisko'),
                                      request.POST.get('email'),
                                      request.POST.get('numer_telefonu'))
        account.Account.add_account(new_account, request.POST.get('is_admin'))
    return render(request, 'add_account.html')


def delete_account(request):
    account.Account.delete_account(request.POST.get('konto_id'))
    return render(request, 'delete_account.html')


def show_accounts(request):
    return render(request, 'show_accounts.html',
                  {'list_of_pracownik': account.Account.show_pracownik(None),
                   'list_of_klient': account.Account.show_klient(None)})


def add_book(request):
    if request.POST.get('tytul') is not None:
        new_book = book.Book(request.POST.get('tytul'),
                             request.POST.get('isbn'),
                             request.POST.get('jezyk_jezyk_id'),
                             request.POST.get('wydawca_wydawca_id'))
        autor_id = request.POST.get('autor_id')
        book.Book.add_book(new_book, autor_id)
    return render(request, 'add_book.html',
                  {'list_of_autors': author.Author.show_autors()})


def delete_book(request):
    book.Book.delete_book(request.POST.get('book_id'))
    return render(request, 'delete_book.html')


def return_book(request):
    book.Book.return_book(request.POST.get('rental_id'))
    return render(request, 'show_rentals.html', {'list_of_rentals': rental.Rental.show_rentals()})


def remove_reservation(request):
    pass
    # book.Book.return_book(request.POST.get('rental_id'))
    # return render(request, 'show_rentals.html', {'list_of_rentals': rental.Rental.show_rentals()})
    reservation.Reservation.remove_reservation(request.POST.get('copy_id'))
    return render(request, 'show_reservations.html',
                  {'reservations': reservation.Reservation.show_reservations()})


def extend_book_rental(request):
    book.Book.extend_book_rental(request.POST.get('rental_id'))
    return render(request, 'show_rentals.html', {'list_of_rentals': rental.Rental.show_rentals()})


def show_books(request):
    return render(request, 'show_books.html',
                  {'list_of_books': book.Book.show_books()})

def search_copy(request):
    filters = {
        'jezyk': request.POST.get('language'),
        'wydawca': request.POST.get('publisher'),
        'tytul': request.POST.get('title'),
        'imie_autora': request.POST.get('name'),
        'nazwisko_autora': request.POST.get('surname'),
        'kategoria': request.POST.get('category'),
    } 
    
    available_copies, borrowed_copies = search.Search.show_search(filters)
    return render(request, 'search_copy.html',
                  {'list_of_borrowed_copies': borrowed_copies,
                   'list_of_available_copies': available_copies,
                   'list_of_languages': search.Search.get_languages(),
                   'list_of_publishers': search.Search.get_publishers(),
                   'list_of_categories': search.Search.get_categories()
                   })
def add_autor(request):
    if request.POST.get('imie') is not None:
        author.Author.add_autor(request.POST.get('imie'), request.POST.get('nazwisko'))
    return render(request, 'add_autor.html')


def delete_autor(request):
    author.Author.delete_autor(request.POST.get('autor_id'))
    return render(request, 'delete_autor.html')


def show_autors(request):
    return render(request, 'show_autors.html',
                  {'list_of_autors': author.Author.show_autors()})

def show_rentals(request):
    return render(request, 'show_rentals.html',
                  {'list_of_rentals': rental.Rental.show_rentals()})

def add_rental(request):
    return render(request, 'add_rental.html',
                  {'list_of_users': account.Account.get_clients(),
                   'list_of_books': book_copy.Book_copy.get_available_books()})

def rent_book(request):
    global employee_id
    if request.POST:
        client_id = request.POST.get('user')
        copy_id = request.POST.get('copy')
        rental.Rental.add_rental(client_id, employee_id, copy_id)
    return render(request, 'show_rentals.html',
                  {'list_of_rentals': rental.Rental.show_rentals()})

def reserve_book(request):
    if request.POST:
        client_id = request.POST.get('user')
        copy_id = request.POST.get('copy')
        reservation.Reservation.add_reservation(copy_id, client_id)
    return render(request, 'show_reservations.html',
                  {'reservations': reservation.Reservation.show_reservations()})

def show_reservations(request):
    return render(request, 'show_reservations.html',
                  {'reservations': reservation.Reservation.show_reservations()})

def show_statistics(request):

    selected_stat = str(request.POST.get('statistic'))
    last_ndays = request.POST.get('last_ndays')
    statistic = Statistic()

    if selected_stat != '' and last_ndays != '' and selected_stat is not None and last_ndays is not None:
        last_ndays = int(last_ndays)
        x = statistic.get_last_x_dates(last_ndays)
        if selected_stat=="Liczba_wypozyczen_z_ostatnich_n_dni":
            y = statistic.get_rentals_last_ndays(last_ndays)
            chart = plot.get_plot(x, y, "Liczba wypożyczeń wg dni", "Liczba wypożyczeń")
        elif selected_stat=="Liczba_rezerwacji_z_ostatnich_n_dni":
            y = statistic.get_reservations_last_ndays(last_ndays)
            chart = plot.get_plot(x, y, "Liczba rezeracji wg dni", "Liczba rezerwacji")
        elif selected_stat=="Liczba_dostepnych_egzemplarzy_z_ostanich_dni":
            y = statistic.get_available_books_last_ndays(last_ndays)
            chart = plot.get_plot(x,y, "Liczba dostepnych egzamplarzy wg dni","Liczba egzemplarzy")
    else:
        chart = None


    return render(request, 'show_statistics.html',
                    {'list_of_statistics': ["Liczba_wypozyczen_z_ostatnich_n_dni","Liczba_rezerwacji_z_ostatnich_n_dni","Liczba_dostepnych_egzemplarzy_z_ostanich_dni"],
                     'list_of_date_ranges': [1,10,30],
                     'chart': chart})

def add_copy(request):
    book = request.POST.get('book')
    quantity = request.POST.get('quantity')
    localization = request.POST.get('localization')

    if book is not None and book !='' and quantity is not None and quantity !='' and localization is not None and localization!='':
        book_copy.Book_copy.add_copy(eval(book),int(quantity),eval(localization))

    return render(request, 'add_copy.html',
                  {'list_of_books': book_copy.Book_copy.get_book_list(),
                   'list_of_localizations': book_copy.Book_copy.get_localization_list(),
                   'list_of_quantity': [1, 2, 3, 4, 5]})