from rest_framework import serializers


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

