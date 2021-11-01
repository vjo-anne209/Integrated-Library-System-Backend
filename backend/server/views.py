from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken
import time
import json

from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from django.core import serializers
from .serializers import *
from .models import *
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from bson.json_util import dumps
from bson.json_util import loads
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

import datetime
from pymongo import MongoClient
import pymongo

# Create your views here.

# Get current user
@api_view(['GET'])
def current_user(request):
    """
    Return the data of current user
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get list of books
@api_view(['GET'])
@permission_classes((AllowAny, ))
def bookList(request):
    books = Book_Instance.objects.all()[:200]
    serializer = BookInstanceSerializer(books, many = True)
    return Response(serializer.data)

# Create Categories
@api_view(['GET'])
@permission_classes((AllowAny, ))
def getCategories(request):
    books = Book_Instance.objects.all()
    d = {}
    for book in books:
        for category in json.loads(book.categories.replace('\'', '"')):
            if category not in d:
                d[category] = 1
    lst = []
    for k in d.keys():
        lst.append(k)

    return Response({"res": lst}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def getYears(request):
    books = Book_Instance.objects.all()
    d = {}

    for book in books:
        year = book.publishedDate
        if year:
            year = json.loads(book.publishedDate.replace('\'', '"'))['$date'].split('-')[0]
            print(year)
            if year not in d:
                d[year] = 1

    lst = []
    for k in d.keys():
        lst.append(k)
    
    lst.sort()

    return Response({"res": lst}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny, ))
def getBook(request, pk):
    book = Book_Instance.objects.get(_id = pk)
    serializer = BookInstanceSerializer(book, many = False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def getBookData(request, pk):
    book = Book.objects.get(bookid = pk)
    serializer = BookSerializer(book, many = False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def getLoanData(request, pk):
    loan = Loan.objects.get(bookid = pk)
    serializer = LoanSerializer(loan, many = False)
    return Response(serializer.data)

@api_view(['GET'])
def getUsersBorrowedBooks(request, userid):
    loans = Loan.objects.filter(borrowerid = userid)
    # bookids = [loan.bookid for loan in loans]
    # books = Book.objects.filter(bookid__in=bookids)
    serializer = LoanSerializer(loans, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getUsersReservedBooks(request, userid):
    reservations = Reservation.objects.filter(reserverid = userid)
    bookids = [reservation.bookid for reservation in reservations]
    loans = Loan.objects.filter(bookid__in=bookids)
    serializer = LoanSerializer(loans, many = True)
    return Response(serializer.data)

#Borrow book (CHECKED)
@api_view(['POST'])
def borrowBook(request):
    data = request.data
    bookid = data["bookid"]
    memberid = data["memberid"]

    if request.user.is_authenticated:
        #Check book's availability
        member = Memberuser.objects.get(user_id = memberid)
        book = Loan.objects.get(bookid = bookid) #book = get_object_or_404(Book, bookid)
        isAvailable = book.availabilitystatus
        if isAvailable:
            # checking for unpaid fines
            try:
                fine = Fine.objects.get(memberid = member)
                return Response({"res": "Please Proceed to Pay Your Fines First"}, status=status.HTTP_403_FORBIDDEN)
            except ObjectDoesNotExist:
                numberOfBook = Loan.objects.filter(borrowerid = member).count()
                #Check the number of book user has borrowed
                if numberOfBook >= 4:
                    return Response({"res": "Book Limit Exceeded"}, status=status.HTTP_403_FORBIDDEN)

                else:
                    #proceed to borrow the book
                    book.borrowerid = member
                    book.expectedduedate = datetime.date.today() + datetime.timedelta(weeks=4)
                    book.availabilitystatus = False
                    book.save(update_fields=["borrowerid", "expectedduedate", "availabilitystatus"])
                    serializer = LoanSerializer(book)
                    return Response(serializer.data)

        return Response({"res": "Book is Currently Unavailable"}, status=status.HTTP_403_FORBIDDEN)
    return Response({"res": "User Not Authenticated"}, status=status.HTTP_403_FORBIDDEN)

# @login_required
@api_view(['POST'])
def returnBook(request): #not sure whether needs to take input memberid or use request.user.id
    # checking for unpaid fines
    data = request.data
    bookid = data['bookid']
    memberid = data['memberid']
    member = Memberuser.objects.get(user_id = memberid)
    book = Book.objects.get(bookid = bookid)
    fine = Fine.objects.get(memberid = member)
    if fine.amount > 0:
        return Response({"res": "Unable to return book as you still have unpaid fines."}, status=status.HTTP_403_FORBIDDEN)
    else:
        # returning the book
        currentBook = get_object_or_404(Loan, bookid = book)
        currentBook.borrowerid = None
        currentBook.availabilitystatus = True
        currentBook.expectedduedate = None
        currentBook.save()
        serializer = LoanSerializer(currentBook)
        return Response(serializer.data)

@api_view(['POST'])
# @login_required
def reserveBook(request):
    data = request.data
    bookid = data['bookid']
    memberid = data['memberid']
    member = Memberuser.objects.get(user_id = memberid)
    book = Book.objects.get(bookid = bookid)
    if request.user.is_authenticated:
        # checking for unpaid fines
        fine = Fine.objects.get(memberid =  member)
        if fine.amount > 0:
            return Response({"res": "User is unable to reserve the book. User has to pay the fines first."}, status=status.HTTP_403_FORBIDDEN)
        else:
            try:
                reservationStatus = Reservation.objects.get(bookid = book)
                if reservationStatus:
                    return Response({"res": "Book is currently reserved. User is unable to reserve the book."}, status=status.HTTP_403_FORBIDDEN)
            except ObjectDoesNotExist:
                # checking if available
                if Loan.objects.get(bookid = book).availabilitystatus:
                    return Response({"res": "Book is currently available. Please proceed to borrow the book instead."}, status=status.HTTP_403_FORBIDDEN)
                if Loan.objects.get(bookid = book).borrowerid == member:
                    return Response({"res": "You are currently borrowing this book."}, status=status.HTTP_403_FORBIDDEN)
                # reserving the book
                else:
                    reservation = Reservation(bookid = book, reserverid= member)
                    reservation.save()
                
                    reservation_serializer = ReservationSerializer(reservation)

                    return Response(reservation_serializer.data)
                                 

@api_view(['DELETE'])
def cancelReservation(request, bookid, memberid):
    member = Memberuser.objects.get(user_id = memberid)
    book = Book.objects.get(bookid = bookid)
    #gets the reservation tuple/entry 
    try:
        reservation = Reservation.objects.filter(reserverid=member, bookid=book).first()
        #deletes the entire reservation entry from Reservation table 
        reservation.delete()
        return Response({"res" : "Reservation Succesfully Cancelled"}, status = status.HTTP_200_OK)
        # from the user's input of the BookID, set status to false in Book table 
    except :
        return Response({"res" : "User does not have reservation for this book"}, status = status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def convertToBorrow(request):
    data = request.data
    bookid = data['bookid']
    memberid = data['memberid']


    book = Book.objects.get(bookid = bookid)
    member = Memberuser.objects.get(user_id = memberid)
    loan = Loan.objects.get(bookid = book)

    if not loan.borrowerid: #check whether it's null or not
        reservation = Reservation.objects.filter(reserverid = member, bookid = book).first()
        #set availability status to False
        loan.availabilitystatus = False
        loan.borrowerid = member
        loan.expectedduedate = datetime.date.today() + datetime.timedelta(days=30)
        loan.save(update_fields=['availabilitystatus','borrowerid','expectedduedate'])
        #delete reservation
        reservation.delete()
        serializer = LoanSerializer(loan)
        return Response(serializer.data)
    else:
        return Response({"res": "This Book has not been returned yet by the previous borrower"}, status = status.HTTP_403_FORBIDDEN)

@api_view(['POST']) 
# @login_required
def renewBook(request):
    data = request.data
    bookid = data['bookid']
    memberid = data['memberid']
    book = Book.objects.get(bookid = bookid)
    currentBook = Loan.objects.get(bookid = bookid)
    member = Memberuser.objects.get(user_id = memberid)
    #check if user has unpaid fine
    fine = Fine.objects.get(memberid = member)
    if fine.amount > 0:
        return Response({"res": "Unable to extend as you have unpaid fines."}, status=status.HTTP_403_FORBIDDEN)
        #check if book has a pending reservation
    else:
        try:
            reservation = Reservation.objects.get(bookid = book)
            return Response({"res": "Unable to renew as there is a pending reservation by another user"}, status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            if Loan.objects.filter(borrowerid = member).count() >= 4:
                return Response({"res": "Unable to renew as user has reached the limit of number of books borrowed"}, status=status.HTTP_403_FORBIDDEN)
            else:
                #if no pending reservation, allow user to borrow book again
                currentBook.borrowerid = member
                currentBook.availabilitystatus = False
                newDueDate = currentBook.expectedduedate + datetime.timedelta(days=30)
                currentBook.expectedduedate = newDueDate
                currentBook.save(update_fields=['borrowerid','availabilitystatus','expectedduedate'])
                serializer = LoanSerializer(currentBook)
                return Response(serializer.data) 
        
client = MongoClient('localhost',port = 27017)
db = client['library-django-db']
class BookListView(generics.ListAPIView):
    serializer_class = BookInstanceSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        if self.request.method == 'GET':
            query = self.request.GET.get('q', None)

            if query is not None:
                results = list(db.server_book_instance.find({"$text" : {"$search" : query}}))
                #lookups= Q(title_icontains=query) | Q(authors_icontains=query)
                #results= Book_Instance.objects.filter(lookups).distinct()
                results= loads(dumps(results, indent =2 ))
                queryset = results
            else:
                results = list(db.server_book_instance.find())
                results = loads(dumps(results, indent =2))
                queryset = results
            return queryset

class BookFilterList(generics.ListAPIView):
    serializer_class = BookInstanceSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        if self.request.method == 'GET':
            category = self.request.GET.get('category', None)
            year = self.request.GET.get('year', None)
            if category is not None and year is not None:
                lookups= Q(categories__icontains=category) & Q(publishedDate__icontains=year)
                results= Book_Instance.objects.filter(lookups).distinct()
                queryset = results
                
            elif category  is not None and year is None:
                lookups= Q(categories__icontains=category)
                results= Book_Instance.objects.filter(lookups).distinct()
                queryset = results

            elif (category is None) and (year is not None):
                lookups= Q(publishedDate__icontains=year)
                results= Book_Instance.objects.filter(lookups).distinct()
                queryset = results

            else:
                results = Book_Instance.objects.all().order_by('title')
                queryset = results
            return queryset


@api_view(['POST'])
def calculateFine(request) :
    listOfMember = Memberuser.objects.all()
    instances = []
    for member in listOfMember: 
        listOfBook = member.loan_set.all() #return empty queryset if does not exist
        if listOfBook.exists() : #Check whether member has borrowed books
            fine = 0
            currentDate = datetime.date.today()
            for book in listOfBook:
                if book.expectedduedate < currentDate:
                    fine += (currentDate - book.expectedduedate).days
                else:
                    continue
            record = Fine.objects.get(memberid = member)
            record.amount = fine
            record.save()
            instances.append(record)

        try:
            reservations = Reservation.objects.filter(reserverid = member)
            #deletes the entire reservation entry from Reservation table 
            for reservation in reservations:
                reservation.delete()

        except ObjectDoesNotExist:
            continue
        else:
            continue
    if len(instances) > 0:
        serializer = FineSerializer(instances, many = True)
        return Response(serializer.data)
    return Response({"res": "No Fine Recorded"}) 
@api_view(['GET'])
def get_fine(request, memberid):
    member = Memberuser.objects.get(user_id = memberid)
    fine = Fine.objects.get(memberid = member)
    amount = fine.amount
    if amount > 0:
        return Response({
            "memberid": memberid,
            "res": amount}, status=status.HTTP_200_OK)
    else:
        return Response({"memberid": memberid, 
        "res": "No Fines"}, status=status.HTTP_200_OK)


#pay fine, only show this for member who has fine
@api_view(['POST'])
def pay_fine(request):
    memberid = request.data['memberid']
    member = Memberuser.objects.get(user_id = memberid)
    memberInFine = Fine.objects.get(memberid = member)
    fine = Fine.objects.get(memberid = member)
    amount = fine.amount
    paymentmethod = request.data['paymentmethod'] #payment method updated
    
    #payment validation
    payment = Payment(memberid = member, finememberid = memberInFine, paymentmethod = paymentmethod )
    payment.save()
    #set fine amount to zero
    fine.amount = 0
    fine.save()
    #fine_serializer = FineSerializer(fine)
    serializer = PaymentSerializer(payment)
    return Response({'fine' : fine.amount, 
                     'payment' : serializer.data})

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.views import generic, View

class ReservedBooksByAdminListView(generics.ListAPIView):
    """Generic class-based view listing books on loan to current admin."""
    serializer_class = ReservationSerializer
    model = Reservation
    paginate_by = 10
    raise_exception = True
    def get_queryset(self):
        return Reservation.objects.all()
            

class LoanedBooksByAdminListView(generics.ListAPIView):
    """Generic class-based view listing books on reservation to current admin."""
    serializer_class = LoanSerializer
    model = Book
    raise_exception = True
    paginate_by = 10
    def get_queryset(self):
        return Loan.objects.filter(availabilitystatus = False).order_by('expectedduedate')


class UnpaidFinesByAdminListView(generics.ListAPIView):
    """Generic class-based view unpaid fines to current admin."""
    serializer_class = FineSerializer
    model = Fine
    raise_exception = True
    paginate_by = 10
    def get_queryset(request):
        return Fine.objects.filter(amount > 0).order_by('amount')
