from rest_framework import serializers
from .models import Appuser


# class InvokeCameraSerializer(serializers.Serializer):
#     """
#         serializer for invoke beacon
#         beacon_uuid = hexadecimal beacon uuid
#         kind    0:Initial 1: repeated
#     """
#     user_id = serializers.IntegerField(required=True)
#     beacon_uuid = serializers.CharField(max_length=255, required=True)
#     minor = serializers.IntegerField(required=True)
#     major = serializers.IntegerField(required=True)
#     kind = serializers.IntegerField(required=True)
#
#
#     def validate(self, data):
#
#         """will handle the logical validation here """
#         return data



# """
# this is serializer for liking picture
# """
# class LikePhotoSerializer(serializers.Serializer):
#
#     photo_id = serializers.CharField(max_length=255)
#     user_id = serializers.IntegerField()
#
#
#     def validate(self, data):
#         """will handle the logical validation here """
#         return data
from rest_framework.exceptions import ValidationError

"""
    @author shibbir
    this is the serializer for adding beer 
"""
class ProductSerializer(serializers.Serializer):
    beer_id = serializers.CharField(max_length=255)
    beer_name = serializers.CharField(max_length=255)
    calorie = serializers.IntegerField()

    def validate(self, data):
        return data
"""
    @author shibbir
    this is barcode scan serializer
    prod_id
    lat
    lon 
    user_id
    date
"""
class BarcodeScanSerializer(serializers.Serializer):
    product_id = serializers.CharField(max_length=255)
    latitude = serializers.CharField(max_length=20)
    longitude = serializers.CharField(max_length=20)
    user_id = serializers.CharField(max_length=20)

    def validate(self, data):
        return data

"""
    @author shibbir
    serializer class for rating table
"""
class RatingSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=20)
    product_id = serializers.CharField(max_length=20)
    rating = serializers.IntegerField(default=0)

    def validate_rating(self, rating):
        if rating  > 5:
            raise ValidationError('rating should be less than 5')
            return 0
        else:
            return rating
    def validate(self, data):
        return data


"""
    @author shibbir
    appuser serializer
"""

class AppuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appuser
        fields = ('id', 'user_name', 'email', 'interest', 'age' , 'sex','political','relation' , 'education', 'create_date')

        def create(self, validated_data):
            return Appuser.objects.create(**validated_data)
    # user_name = serializers.CharField(max_length=20)
    # email = serializers.CharField(max_length=55)
    # interest = serializers.IntegerField()
    # age = serializers.IntegerField(max_value=100, min_value=18)
    # sex = serializers.IntegerField()
    # political = serializers.IntegerField()
    # relation = serializers.IntegerField()
    # education = serializers.IntegerField()

