from django.db import models
from pynamodb.models import Model as Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute,
    UTCDateTimeAttribute)
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection, LocalSecondaryIndex

# Create your models here.



class Product(Model):
    class Meta:
        table_name = 'beer'
        region = 'ap-southeast-2'
        host = 'https://dynamodb.ap-southeast-2.amazonaws.com'
        write_capacity_units = 1
        read_capacity_units = 1

    beer_id = UnicodeAttribute(hash_key=True)
    beer_name = UnicodeAttribute()
    calorie = NumberAttribute(default=0)
    price = UnicodeAttribute(default=5)
    date_created = UTCDateTimeAttribute()


# if not Product.exists():
#     Product.create_table(wait=True)

class Barcode_Scan(Model):
    class Meta:
        table_name = 'barcode_scan'
        region = 'ap-southeast-2'
        host = 'https://dynamodb.ap-southeast-2.amazonaws.com'
        write_capacity_units = 1
        read_capacity_units = 1
    scan_id = UnicodeAttribute(hash_key=True)
    product_id = UnicodeAttribute()
    latitude = UnicodeAttribute()
    longitude = UnicodeAttribute()
    user_id = UnicodeAttribute()
    date_created = UTCDateTimeAttribute(range_key=True)

if not Barcode_Scan.exists():
    Barcode_Scan.create_table(wait=True)


class UserIDIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = "user_id"
        read_capacity_units = 2
        write_capacity_units = 1

        projection = AllProjection()

    user_id = NumberAttribute(default=0, hash_key=True)

class Rating(Model):
    class Meta:
        table_name = 'rating'
        region = 'ap-southeast-2'
        host = 'https://dynamodb.ap-southeast-2.amazonaws.com'
        write_capacity_units = 1
        read_capacity_units = 1
    product_id = UnicodeAttribute(hash_key=True)
    user_id = UnicodeAttribute(range_key=True)
    #view_index = UserIDIndex()
    #user_id = NumberAttribute(default=0)
    rating = UnicodeAttribute()
    date_created = UTCDateTimeAttribute()


if not Rating.exists():
    Rating.create_table(wait=True)
class Appuser(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    CYCLING = 0
    RUNNING = 1
    CROSSFIT = 2
    AFL = 3
    WEIGHTLIFTING = 4
    CRICKET = 5
    INTERESTS = (
        (CYCLING, 'Cycling'),
        (RUNNING, 'Running'),
        (CROSSFIT, 'Crossfit'),
        (AFL, 'AFL'),
        (WEIGHTLIFTING, 'Weightlifting'),
        (CRICKET, 'Cricket'),
    )

    CONSERVATIVE = 0
    LIBERAL = 1
    LIBERETERIAN = 2
    POLITICAL_CHOISES = (
        (CONSERVATIVE, 'Conservative'),
        (LIBERAL, 'Liberal'),
        (LIBERETERIAN, 'Libereterian'),
    )

    SINGLE = 0
    MARRIED = 1
    PARENT = 2
    RELATION_CHOISES = (
        (SINGLE,'Single'),
        (MARRIED, 'Married'),
        (PARENT, 'Parent'),
    )

    HIGHSCHOOL = 0
    UNDERGRADUATE = 1
    POSTGRADUATE = 2
    EDUCATION = (
        (HIGHSCHOOL,'Highschool'),
        (UNDERGRADUATE, 'Undergraduate'),
        (POSTGRADUATE, 'Postgraduate'),
    )

    user_name = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=55, unique=True)
    interest = models.IntegerField(default=0, choices=INTERESTS)
    age = models.IntegerField(default=18)
    sex = models.CharField(max_length=1, blank=True, null=True, choices=GENDER_CHOICES)
    political = models.IntegerField(default=0, choices=POLITICAL_CHOISES)
    relation = models.IntegerField(default=0, choices=RELATION_CHOISES)
    education = models.IntegerField(default=0, choices=EDUCATION)
    create_date = models.DateTimeField(auto_now_add=True)

