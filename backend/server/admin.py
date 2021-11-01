from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Book)
admin.site.register(Book_Instance)
admin.site.register(Reservation)
admin.site.register(Fine)
admin.site.register(Loan)
admin.site.register(Memberuser)

#current books reservation --> just refer to reservation table
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('bookid', 'memberid', 'reservationno')
#current books borrowing --> filter book table --> availabilityStatus == False

class BooksAdmin(admin.ModelAdmin):
    list_display = ('bookid', 'booktitle', 'reservationstatus', 'availablitystatus', 'expectedduedate')
    list_filter = ('availabilitystatus', 'expectedduedate')

#unpaid Fines --> filter Fine table --> paymentStatus == Not Approved

class FineAdmin(admin.ModelAdmin):
    list_display = ("memberid", "paymentstatus", "amount")
    list_filter = ('paymentstatus')
