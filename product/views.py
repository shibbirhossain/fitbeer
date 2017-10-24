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
from . util import compute_tweet, get_topic_modelled_words, scrap_dbpedia_ontology, get_abstract_text, pass_through_dbpedia_lda
from nltk.corpus import wordnet
from itertools import chain
from .wordnet_util import generate_synonym

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

"""
    nltp bag of words view
"""
class Tweet2NLTPAPIView(GenericAPIView):

    serializer_class = serializers.Tweet2NLTPSerializer

    def get(self, request, format=None):
        return Response({'data' : 'nothing to see here'})

    def post(self, request):
        serializer = serializers.Tweet2NLTPSerializer(data=request.data)
        if (serializer.is_valid()):
            tweet_with_syno = {}
            tweet_text = serializer.data.get('tweet_text')
            keyword_text = serializer.data.get('keyword')
            #print(keyword_text)
            keyword_list = keyword_text.split(',')
            #print(keyword_list)
            bow_list = []
            bag_of_nltp_words = compute_tweet(tweet_text)
            syno_list = []
            bag_of_nltp_words = bag_of_nltp_words[0]
            for word in bag_of_nltp_words:
                synonyms = wordnet.synsets(word)
                lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
                if not lemmas:
                    print("THE WORD TO BE REMOVED IS : {}".format(word))
                    bag_of_nltp_words.remove(word)
                #print(lemmas)
                for word in lemmas:
                    syno_list.append(word)
                tweet_with_syno[word] = lemmas
            bag_of_nltp_words = list(set(bag_of_nltp_words))

            #print(syno_list)
            #print(tweet_with_syno)
            #syno_list : is the list of all the synonyms that we will try to find match
            #tweet_with syno : if we find match in syno_list with the words from dbpedia abstract,
            # we get the original tweet word from tweet_with_syno list
            try:
                data = pass_through_dbpedia_lda(bag_of_nltp_words, syno_list, keyword_list)
            except:
                return Response({'data' : ""})
            return Response({'data' : data})

"""
    LDA bag of words view
"""
class DBPediaText2LDAAPIView(GenericAPIView):

    serializer_class = serializers.DBPedia2LDASerializer


    def post(self, request):
        serializer = serializers.DBPedia2LDASerializer(data=request.data)
        if (serializer.is_valid()):
            dbpedia_text = serializer.data.get('paragraph')
            bag_of_words_count = serializer.data.get('bow')

            lda_bow = get_topic_modelled_words(dbpedia_text, bag_of_words_count)
            print(lda_bow)

            return Response({'data' : lda_bow})


"""
    dbpedia abstract view
"""
class DBPediaAbstractView(GenericAPIView):

    serializer_class = serializers.DBPediaAbstractSerializer

    def post(self, request):
        serializer = serializers.DBPediaAbstractSerializer(data=request.data)

        if(serializer.is_valid()):
            topic = serializer.data.get('topic').title()
            print(topic)

            abstract_text = get_abstract_text(topic)


        return Response({'data' : abstract_text})


"""
    definition API view class
    
"""
class DefinitionAPIView(GenericAPIView):

    serializer_class = serializers.WordNetDefinitonSerializer

    def post(self, request):
        serializer = serializers.WordNetDefinitonSerializer(data=request.data)
        if(serializer.is_valid()):
            word = serializer.data.get('word')
            definition_list = generate_synonym(word)
            definition_list = list(set(definition_list))
        return Response({'data' : definition_list})

"""
    lda words with definition API view class
    
"""
class LDAPlusDefinitionAPIView(GenericAPIView):

    serializer_class = serializers.LDAPlusSynoSerializer

    def post(self, request):
        serializer = serializers.WordNetDefinitonSerializer(data=request.data)
        if(serializer.is_valid()):
            topic_name = serializer.data.get('word').title()

            lda_bag_of_words = scrap_dbpedia_ontology(topic_name)
            print(lda_bag_of_words)
            # definition_list = generate_synonym(word)
            # definition_list = list(set(definition_list))
            total_word_list_json = []
            for each_lda_word in lda_bag_of_words:
                definiton_list = list(set(generate_synonym(each_lda_word)))
                definiton_list_json = {
                    "keyword" : each_lda_word,
                    "def" : definiton_list
                }
                total_word_list_json.append(definiton_list_json)

        return Response({ "data" : total_word_list_json })


"""
    batch tweet and keyword serializer apiview
"""

class BatchTweetWithKeywordAPIView(GenericAPIView):

    serializer_class = serializers.BatchTweetWithKeywordSerializer

    def post(self, request):
        serializer = serializers.BatchTweetWithKeywordSerializer(data=request.data)

        if serializer.is_valid():
            tweet_list = serializer.data.get('tweet_list')
            keywords = serializer.data.get('keywords')
            print(keywords)

        return Response({ "data" : "empty"})