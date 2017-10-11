from rest_framework import serializers
from .models import Appuser

from rest_framework.exceptions import ValidationError

"""
    @author shibbir
    shibbirhssn@gmail.com
    this is the serializer for adding beer 
"""
class ProductSerializer(serializers.Serializer):
    beer_id = serializers.CharField(max_length=255)
    beer_name = serializers.CharField(max_length=255)
    calorie = serializers.IntegerField()
    price = serializers.DecimalField(default=0.0, max_digits=3,decimal_places=2)
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
    rating = serializers.DecimalField(default=0.0, max_digits=3,decimal_places=2)

    def validate_rating(self, rating):
        if rating  > 5.0:
            raise ValidationError('rating should be less than 5')
            return 0.0
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


"""
    @author shibbir
    get the product details by product id
"""
class ProductDetailsSerializer(serializers.Serializer):
    product_id = serializers.CharField(max_length=255)
    latitude = serializers.CharField(max_length=20)
    longitude = serializers.CharField(max_length=20)
    user_id = serializers.CharField(max_length=20)

    def validate(self, data):
        return data
"""
    @author shibbir
    converting the tweet text into 
    natural laguage processed bag of words
    
"""
class Tweet2NLTPSerializer(serializers.Serializer):

    tweet_text = serializers.CharField(max_length=160)

    def validate(self, data):
        return data

"""
    @author shibbir
    converting the DBPedia paragraph into
    LDA processed bag of words
"""

class DBPedia2LDASerializer(serializers.Serializer):
    paragraph = serializers.CharField(max_length=5000)
    bow = serializers.IntegerField(max_value=20)
    def validate(self, data):
        return data

