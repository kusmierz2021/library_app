from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^admin/$', views.admin, name='admin'),
    url(r'^login/$', views.login, name='login'),
    url(r'^log/$', views.log, name='log'),
    url(r'^add_account/$', views.add_account, name='add_account'),
    url(r'^show_accounts/$', views.show_accounts, name='show_accounts'),
    url(r'^delete_account/$', views.delete_account, name='delete_account'),
    url(r'^add_book/$', views.add_book, name='add_book'),
    url(r'^delete_book/$', views.delete_book, name='delete_book'),
    url(r'^return_book/$', views.return_book, name='return_book'),
    url(r'^extend_book_rental/$', views.extend_book_rental, name='extend_book_rental'),
    url(r'^show_books/$', views.show_books, name='show_books'),
    url(r'^search_copy/$', views.search_copy, name='search_copy'),
    url(r'^add_autor/$', views.add_autor, name='add_autor'),
    url(r'^show_autors/$', views.show_autors, name='show_autors'),
    url(r'^delete_autor/$', views.delete_autor, name='delete_autor'),
    url(r'^show_rentals/$', views.show_rentals, name='show_rentals'),
    url(r'^add_rental/$', views.add_rental, name='add_rental'),
    url(r'^rent_book/$', views.rent_book, name='rent_book'),
    url(r'^reserve_book/$', views.reserve_book, name='reserve_book'),
    url(r'^show_reservations/$', views.show_reservations, name='show_reservations'),
    url(r'^remove_reservation/$', views.remove_reservation, name='remove_reservation'),
    url(r'^statistic/$', views.show_statistics, name='show_statistics'),
    url(r'^add_copy/$', views.add_copy, name='add_copy'),
]