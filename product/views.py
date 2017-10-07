from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import UpdateAPIView, GenericAPIView
from rest_framework.response import Response

from product.models import RawPhoto
from . import serializers

"""
    @author shibbir
    this is a gneric api view to get beers 
    will add add beers later

"""
class ProductsAPIView(GenericAPIView):
    #pagination_class = LargeResultsSetPagination
    serializer_class = serializers.InvokeCameraSerializer

    def get(self, request, format=None):
        return Response({'status': True, 'data': { 'beers': "we add the beers here"}})


"""
    @author shibbir
    unlike user/business photos 
    the User ID, and Photo ID is passed on along to unlike the photo
"""
class UnlikePhotoView(GenericAPIView):

    serializer_class = serializers.LikePhotoSerializer
    # def get(self, request, format=None):
    #     return Response({'status': True, 'data': { 'photos_likes': "you unlike the photos here"}})

    def post(self, request):
        serializer = serializers.LikePhotoSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.data.get('user_id')
            photo_id = serializer.data.get('photo_id')

            message = "{} {} photo unliked successfully".format(user_id, photo_id)
            print(message)
            try:
                photoobject = RawPhoto.query(photo_id)
                for photo in photoobject:
                    print(photo.photo_id)
                    print(photo.date_created)

                return Response({'message': message})
            except RawPhoto.DoesNotExist:
                print("photo id does not exist")
                return Response("no photo exists with the photo id", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response('there is something wrong', status=status.HTTP_400_BAD_REQUEST)

