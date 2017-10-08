from django.core.serializers import json
from django.shortcuts import render

# Create your views here.
from rest_framework import status, viewsets
from rest_framework.generics import UpdateAPIView, GenericAPIView
from rest_framework.response import Response
from datetime import datetime
from product.models import Product, Barcode_Scan, Rating, Appuser
from . import serializers
from . util import generate_scan_id, generate_random_arrayfill

"""
    @author shibbir
    email shibbirhssn@gmail.com
    this is a gneric api view to get beers 
    will add add beers later

"""
class ProductsAPIView(GenericAPIView):
    #pagination_class = LargeResultsSetPagination
    serializer_class = serializers.ProductSerializer

    def get(self, request, format=None):
        beers = Product.scan()
        beers_json = []
        for beer in beers:
            beer_json = {
                "beer_id" : beer.beer_id,
                "beer_name" : beer.beer_name,
                "calorie" : beer.calorie,
                "price" : beer.price
            }
            beers_json.append(beer_json)
        #json_resp = '"beer_id" : "1012234", "beer_name" : "pure blond", "calorie" : "56"'
        print(beers_json)
        return Response({ "data" : beers_json })

    def post(self, request):
        serializer = serializers.ProductSerializer(data=request.data)
        if(serializer.is_valid()):
            beer_id = serializer.data.get('beer_id')
            beer_name = serializer.data.get('beer_name')
            calorie = serializer.data.get('calorie')
            price = serializer.data.get('price')
            message = "{} {} {} {} ".format(beer_id, beer_name, calorie, price)
            print(message)
            try:

                post_beer = Product(
                    beer_id,
                    beer_name=beer_name,
                    calorie=calorie,
                    price=price,
                    date_created=datetime.now()
                )
                post_beer.save()

                return Response({'data' : message + " added successfully"})
            except Exception as e :
                return Response({'data': str(e)})

class BarcodeScanAPIView(GenericAPIView):
    serializer_class = serializers.BarcodeScanSerializer
    def get(self, request, format=None):
        barcode_invokes_from_db = Barcode_Scan.scan()
        barcode_invokes_json = []
        for barcode_invoke in barcode_invokes_from_db:
            barcode_invoke_json = {
                "product_id": barcode_invoke.product_id,
                "latitude": barcode_invoke.latitude,
                "longitude": barcode_invoke.longitude,
                "user_id": barcode_invoke.user_id
            }
            barcode_invokes_json.append(barcode_invoke_json)
        # json_resp = '"beer_id" : "1012234", "beer_name" : "pure blond", "calorie" : "56"'
        print(barcode_invokes_json)
        return Response({"data": barcode_invokes_json})

    def post(self, request):
        serializer = serializers.BarcodeScanSerializer(data=request.data)
        if (serializer.is_valid()):
            product_id = serializer.data.get('product_id')
            latitude = serializer.data.get('latitude')
            longitude = serializer.data.get('longitude')
            user_id = serializer.data.get('user_id')
            message = "{} {} {} ".format(product_id, latitude, longitude, user_id)
            print(message)
            try:
                scan_id = generate_scan_id(user_id)
                post_barcode_scan = Barcode_Scan(
                    scan_id,
                    product_id=product_id,
                    latitude=latitude,
                    longitude=longitude,
                    user_id=user_id,
                    date_created=datetime.now()
                )
                post_barcode_scan.save()

                return Response({'data': message + " added successfully"})
            except Exception as e:
                return Response({'data': e})

class RatingAPIView(GenericAPIView):
    serializer_class = serializers.RatingSerializer

    def get(self, request, format=None):
        ratings = Rating.scan()
        ratings_json = []
        for rating in ratings:
            rating_json = {
                "user_id": rating.user_id,
                "product_id": rating.product_id,
                "rating": rating.rating
                }
            ratings_json.append(rating_json)
            # json_resp = '"beer_id" : "1012234", "beer_name" : "pure blond", "calorie" : "56"'
            print(ratings_json)
        return Response({"data": ratings_json})

    def post(self, request):
        serializer = serializers.RatingSerializer(data=request.data)
        if (serializer.is_valid()):
            user_id = serializer.data.get('user_id')
            product_id = serializer.data.get('product_id')
            rating = serializer.data.get('rating')
            message = "{} {} {} ".format(user_id, product_id, rating)
            print(message)
            #rating_id = generate_rating_id(user_id)
            try:
                post_rating = Rating(
                    product_id,
                    user_id=user_id,
                    rating=rating,
                    date_created=datetime.now()
                    )
                post_rating.save()

                return Response({'data': message + " added successfully"})
            except Exception as e:
                return Response({'data': str(e)})
        else:
            return Response({'data': 'there is some error {}'.format(serializer.errors)})

class AppuserViewset(viewsets.ModelViewSet):
    serializer_class = serializers.AppuserSerializer
    queryset = Appuser.objects.all()
    def destroy(self, request, pk=None):

        try:
            camera = Appuser.objects.get(pk=pk)
            camera.delete()

            serializer_class = serializers.AppuserSerializer

            return Response({
                'status': True,
                'data':
                    {
                        'result': 'deleted successfully',
                        'HTTP_Status': status.HTTP_204_NO_CONTENT
                    }
            })
        except Appuser.DoesNotExist:
            return Response({
                'status': False,
                'data':
                    {
                        'result': 'appuser id does not exist',
                        'HTTP_Status': status.HTTP_404_NOT_FOUND
                    }
            })
#
# """
#     @author shibbir
#     the app user passes the product api while calling the API
#     and get the product details in response
#     return includes {
#         Product name
#         rating - total rating count, avg
#         myrating personal rating
#         price
#         calorie
#     }
# """
# class ProductsDetailsByProductIDAPIView(GenericAPIView):
#     pass

class RandomDataAPIView(GenericAPIView):
    def get(self, request, format=None):

        data = generate_random_arrayfill()
        print(data)
        return Response({"data":  data})