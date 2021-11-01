from django.urls import path
from .views import *

urlpatterns = [
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
    path('booklist/', bookList),
    path('booklist/<int:pk>/', getBook),
    path('bookdata/<int:pk>/', getBookData),
    path('loandata/<int:pk>/', getLoanData),
    path('borrowedbooks/<int:userid>/', getUsersBorrowedBooks),
    path('reservedbooks/<int:userid>/', getUsersReservedBooks),
    path('borrowbook/', borrowBook),
    path('returnbook/', returnBook),
    path('reservebook/', reserveBook),
    path('cancelreservation/<int:bookid>/<int:memberid>/', cancelReservation),
    path('renewbook/', renewBook),
    path('search/', BookListView.as_view()),
    path('filter/', BookFilterList.as_view()),
    path('convertreservation/', convertToBorrow),
    path('getcategories/', getCategories),
    path('getyears/', getYears),
    path('fine/<int:memberid>/', get_fine),
    path('payfine/', pay_fine),
    path('adminreservedbooks/', ReservedBooksByAdminListView.as_view()),
    path('adminborrowedbooks/', LoanedBooksByAdminListView.as_view()),
    path('adminunpaidfines/', UnpaidFinesByAdminListView.as_view()),
    path('calculatefine/', calculateFine),
]