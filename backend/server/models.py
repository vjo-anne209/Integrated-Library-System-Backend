# # This is an auto-generated Django model module.
# # You'll have to do the following manually to clean this up:
# #   * Rearrange models' order
# #   * Make sure each model has one field with primary_key=True
# #   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
# #   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# # Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django_mysql.models import EnumField
from django.contrib.auth.models import User

class Adminuser(models.Model):
    class params:
        db = 'default'
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    adminpassword = models.CharField(db_column='adminPassword', max_length=300)  # Field name made lowercase.

    class Meta:
        db_table = 'adminuser'


class Memberuser(models.Model):
    class params:
        db = 'default'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    username = models.CharField(db_column='username', max_length=50)  # Field name made lowercase
    memberpassword = models.CharField(db_column='memberPassword', max_length=300)  # Field name made lowercase.

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'memberuser'


class Book(models.Model):
    bookid = models.IntegerField(db_column='_id', primary_key=True)  # Field renamed because it started with '_'.
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    pagecount = models.IntegerField(db_column='pageCount')  # Field name made lowercase.
    publisheddate = models.CharField(db_column='publishedDate', max_length=200, blank=True, null=True)  # Field name made lowercase.
    categories = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book'


class Loan(models.Model):
    class params:
        db = 'default'

    bookid = models.ForeignKey(Book,db_column='_id', primary_key=True, on_delete = models.CASCADE)  # Field name made lowercase.
    borrowerid = models.ForeignKey(Memberuser,  on_delete = models.SET_NULL, db_column='BorrowerID', default = None,blank = True, null=True)  # Field name made lowercase.
    availabilitystatus = models.BooleanField(db_column='availabilityStatus', default = True)  # Field name made lowercase
    expectedduedate = models.DateField(db_column='expectedDueDate', blank= True,null=True, default = None)  # Field name made lowercase.

    class Meta:
        db_table = 'loan'


class Reservation(models.Model):
    reserverid = models.ForeignKey(Memberuser,db_column='reserverID', primary_key=True,on_delete = models.CASCADE)  # Field name made lowercase.
    bookid = models.ForeignKey(Book,db_column='BookID',on_delete = models.CASCADE)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'reservation'
        unique_together = (('reserverid', 'bookid'),)

class Fine(models.Model):
    memberid = models.ForeignKey(Memberuser,db_column='memberID', primary_key=True,on_delete = models.CASCADE)  # Field name made lowercase.
    amount = models.DecimalField(max_digits=10, decimal_places=2, default = 0.00)

    class Meta:
        managed = False
        db_table = 'fine'

class Payment(models.Model):
    paymentno = models.AutoField(db_column='paymentNo', primary_key=True)  # Field name made lowercase.
    paymentmethod = EnumField(db_column='paymentMethod', blank = True, null=True, choices = [
        ('DEBIT CARD', 'Debit Card'),
        ('CREDIT CARD', 'Credit Card'),
        ], default = None) 
    finememberid = models.ForeignKey(Fine, models.CASCADE, db_column='fineMemberID')  # Field name made lowercase.
    memberid = models.ForeignKey(Memberuser, models.CASCADE, db_column='MemberID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'payment'


from djongo import models
from django import forms
import pymongo

class Book_Instance(models.Model):
    class params:
        db = 'book_db'

    Book_Status = (
        ('PUBLISH', 'PUBLISH'),
        ('MEAP', 'MEAP')
        )
    _id = models.IntegerField(primary_key = True,blank = False)
    title = models.CharField(max_length = 100, blank = False)
    isbn = models.CharField(max_length = 50, blank = False)
    pageCount = models.IntegerField(blank = False)
    publishedDate = models.CharField(max_length = 100,blank = True)
    thumbnailUrl = models.CharField(max_length=200, blank = False)
    shortDescription = models.CharField(max_length =500, blank = True)
    longDescription = models.CharField(max_length = 2000, blank = True)
    status = models.CharField(max_length = 10, choices = Book_Status)
    authors = models.CharField(max_length=100, blank=False)
    categories = models.CharField(max_length=100, blank=False)