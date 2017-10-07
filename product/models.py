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
    date_created = UTCDateTimeAttribute()


if not Product.exists():
    Product.create_table(wait=True)

class UserIDIndex(GlobalSecondaryIndex):

    class Meta:
        index_name = "user_id"
        read_capacity_units = 2
        write_capacity_units = 1

        projection = AllProjection()

    user_id = NumberAttribute(default=0, hash_key=True)


class RawPhoto(Model):
    class Meta:
        table_name = 'raw_photo'
        region = 'ap-southeast-2'
        host = 'https://dynamodb.ap-southeast-2.amazonaws.com'
        write_capacity_units = 2
        read_capacity_units = 2

    photo_id = UnicodeAttribute(hash_key=True)
    user_id = NumberAttribute()
    view_index = UserIDIndex()
    user_id = NumberAttribute(default=0)
    restaurant_id = NumberAttribute(default=0)
    #caption_text = UnicodeAttribute()
    #photo_path = UnicodeAttribute()
    #hashtags = UnicodeSetAttribute()
    #is_posted = NumberAttribute()
    is_created = NumberAttribute(default=0)
    #is_deleted = NumberAttribute(default=0)
    #date_updated = UTCDateTimeAttribute()
    date_created = UTCDateTimeAttribute(range_key=True)