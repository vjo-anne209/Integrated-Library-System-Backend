# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Adminuser(models.Model):
    adminid = models.AutoField(db_column='adminID', primary_key=True)  # Field name made lowercase.
    adminpassword = models.CharField(db_column='adminPassword', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AdminUser'


class Book(models.Model):
    bookid = models.IntegerField(db_column='BookID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=100)  # Field name made lowercase.
    borrowerid = models.ForeignKey('Memberuser', models.DO_NOTHING, db_column='BorrowerID', blank=True, null=True)  # Field name made lowercase.
    availabilitystatus = models.IntegerField(db_column='availabilityStatus')  # Field name made lowercase.
    expectedduedate = models.DateField(db_column='expectedDueDate', blank=True, null=True)  # Field name made lowercase.
    reservationstatus = models.IntegerField(db_column='reservationStatus')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Book'


class Fine(models.Model):
    memberid = models.ForeignKey('Memberuser', models.DO_NOTHING, db_column='memberID')  # Field name made lowercase.
    paymentno = models.AutoField(db_column='paymentNo', primary_key=True)  # Field name made lowercase.
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    paymentmethod = models.CharField(db_column='paymentMethod', max_length=22, blank=True, null=True)  # Field name made lowercase.
    paymentstatus = models.CharField(db_column='paymentStatus', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Fine'


class Memberuser(models.Model):
    memberid = models.AutoField(db_column='memberID', primary_key=True)  # Field name made lowercase.
    membername = models.CharField(db_column='memberName', max_length=100)  # Field name made lowercase.
    memberpassword = models.CharField(db_column='memberPassword', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MemberUser'


class Reservation(models.Model):
    reserverid = models.ForeignKey(Memberuser, models.DO_NOTHING, db_column='reserverID')  # Field name made lowercase.
    bookid = models.ForeignKey(Book, models.DO_NOTHING, db_column='BookID')  # Field name made lowercase.
    reservationno = models.IntegerField(db_column='ReservationNo', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Reservation'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
