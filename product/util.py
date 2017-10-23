import datetime
import random
import time
from itertools import chain

from django.core.serializers import json
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer, SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string
# Importing Gensim
import gensim
from gensim import corpora
from bs4 import BeautifulSoup
import requests
import json
from .file_util import write_to_file, read_from_file, read_list_from_file, write_line_to_file
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

"""
    @author shibbir
    shibbirhssn@gmail.com
"""

def generate_scan_id(user_id):
    timestamp = time.time()

    generated_scan_id = str(user_id)+'-'+datetime.datetime.fromtimestamp(timestamp).strftime('%Y%m%d%H%M%S')
    return generated_scan_id


def generate_rating_id(user_id):
    timestamp = time.time()

    generated_rating_id = str(user_id) + '-' + datetime.datetime.fromtimestamp(timestamp).strftime('%Y%m%d%H%M%S')
    return generated_rating_id

def generate_random_arrayfill():
    random_number_list = []
    for i in range(0,2513):
        random_number = generate_random_number(0, 2000)
        rand_json = {
            i : random_number
        }
        random_number_list.append(rand_json)

    print(random_number_list)

    return random_number_list



def generate_random_number(start_val, end_val):

    random_number = random.randint(start_val, end_val)
    return random_number


"""
    we compute the tweet text here for nltp 
    API
"""
def compute_tweet(sample_doc):

    print(word_tokenize(sample_doc))

    # tokenized_doc = word_tokenize(sample_doc)
    # # stemmed_word_list = []
    # # for word in tokenized_doc:
    # #     stemmed_word = sb.stem(word)
    # #     stemmed_word_list.append(stemmed_word)
    #
    # lemmatizer = WordNetLemmatizer()
    # lemmatized_word_list = []
    #
    # for word in tokenized_doc:
    #
    #     lemmatized_word = lemmatizer.lemmatize(word)
    #     lemmatized_word_list.append(lemmatized_word)
    #
    # print(lemmatized_word_list)
    doc_string = ""
    for line in sample_doc:
        doc_string += line
    #compile documents
    doc_complete = [doc_string]

    #
    #  ps = PorterStemmer()
    #
    # doc_complete = ps.stem(doc_complete)
    # print(doc_complete)
    stop = set(stopwords.words('english'))
    #string.punctuation = string.punctuation.__add__('rt')
    #string.punctuation = string.punctuation.__add__('http')

    exclude = set(string.punctuation)
    #print(string.punctuation)

    #exclude_twitter_specific_noise
    lemma = WordNetLemmatizer()
    doc_clean = [clean(doc, lemma, stop, exclude).split() for doc in doc_complete]
    #print(type(doc_clean))
    twitter_specific_noises = ['rt', 'tweet', 'http']
    # print(type(twitter_specific_noises))


    # print(doc_clean)

    # my_list = [l[0] for l in list]

    #doc_clean = doc_clean[0]
    #print(doc_clean)

    # line is doc, word is word to be removed
    # for word in doc_clean:
    #     # print('the word is {}'.format(word))
    #     if '…' in word:
    #         doc_clean.remove(word)
        # elif '' in word:
        #     doc_clean.remove(word)
        # else:
        #     print('no dot')
    # if 'ocean' in word:
    #         print('this word {} thing contains dot'.format(word))

    #doc_clean.remove('rt')
    #doc_clean.remove('ocean')
    #doc_clean.remove('http…')
    #print(doc_clean)

    #return doc_clean
    return doc_clean

def clean(doc, lemma, stop, exclude):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    #twitter_specific_noise_free = ''.join(ch for ch in punc_free if ch not in exclude_twitter_specific_noise)
    #it was punc_free, made it stop_free only now
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    #print(type(normalized))
    return normalized

# we get the topic name for saving calculation
# in file purpose
def get_topic_modelled_words(topic_name, data, bag_of_words_count):
    doc_complete = [data]
    # we run the cleaning process here
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()
    def clean(doc):
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
        return normalized

    doc_clean = [clean(doc).split() for doc in doc_complete]

    # Creating the term dictionary of our courpus, where every unique term is assigned an index.
    dictionary = corpora.Dictionary(doc_clean)

    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

    Lda = gensim.models.ldamodel.LdaModel

    # Running and Trainign LDA model on the document term matrix.
    ldamodel = Lda(doc_term_matrix, num_topics=1, id2word=dictionary, passes=20)
    lda_list = ldamodel.print_topics(num_topics=1, num_words=bag_of_words_count)

    for word in lda_list:
        #print("word is {}".format(word))

        weighted_word = word[1]
        #print(weighted_word)
        split_by_plus = weighted_word.split('+')
        #print(split_by_plus)
        topic_word_list = []
        for word in split_by_plus:
            split_by_multiply = word.split('*')
            #print(split_by_multiply)
            weight_value = split_by_multiply[0].strip()
            #print(weight_value)
            #print(split_by_multiply[1])
            final_word = split_by_multiply[1].replace('"', '').strip()
            print("{} {}".format(final_word, weight_value))

            # topic_word = {
            #     "weight" : weight_value,
            #     "word" : final_word
            # }
            word = final_word
            topic_word_list.append(word)

        #print(weighted_word[0])
        #print(weighted_word[1])
    write_line_to_file(topic_name, topic_word_list)
    return topic_word_list

def scrap_dbpedia_ontology(topic_name):
    is_file_exists = os.path.isfile(topic_name+".txt")
    print("is file exists {}".format(is_file_exists))
    if is_file_exists == False:
        try:
            url = "http://dbpedia.org/data/"+topic_name+".json"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            abstract_text = ""
            #http://dbpedia.org/data/Fever.json
            #print(soup)
            if soup is not None:
                first_level_resource_json_parse = 'http://dbpedia.org/resource/'+topic_name
                json_data = json.loads(str(soup))
                json_data = json_data[first_level_resource_json_parse]['http://dbpedia.org/ontology/abstract']
                #['http://dbpedia.org/ontology/abstract']

                for data in json_data:
                    if(data['lang'] == 'en'):
                        #print(data['value'])
                        abstract_text = data['value']
                        write_to_file(topic_name+".txt", abstract_text)
                        # total_word_count = sum(len(line.split()) for line in abstract_text)
                        # print("total number of words is {}".format(total_word_count))
            TOPIC_WORD_TEXT = topic_name+"_lda"+".txt"
            # we have to check here if topic_word_text file exists or not as well
            is_topic_word_file_exists = os.path.isfile(TOPIC_WORD_TEXT)

            if is_topic_word_file_exists == True:
                topic_modelled_words = read_list_from_file(TOPIC_WORD_TEXT)

                topic_modelled_word_list = topic_modelled_words.split()
                print(topic_modelled_words)

                # for word in topic_modelled_word_list:
                #     print(word)
                print("scrap_db if == False if condition")
                print(topic_modelled_word_list)

                return topic_modelled_word_list
            else:
                topic_modelled_words = get_topic_modelled_words(TOPIC_WORD_TEXT, abstract_text, 15)
                print("scrap_db if==False else condition")
                #print(topic_modelled_words)
                print("the topic name is {}".format(topic_name))
                return topic_modelled_words
        except KeyError:
            print("nothing here keyerror")
            return ""
    else:
        abstract_text = read_from_file(topic_name+".txt")
        #print("we are printing the abstract text here")
        #print(abstract_text)
        TOPIC_WORD_TEXT = topic_name+"_lda"+".txt"
        is_words_exists_in_file = os.path.isfile(TOPIC_WORD_TEXT)
        print("lets see if lda word file exists {}".format(is_words_exists_in_file))
        if is_words_exists_in_file == False:
            topic_modelled_words = get_topic_modelled_words(TOPIC_WORD_TEXT, abstract_text, 15)
            print("vkshibbir")
            print("scrap_db if == True(else) if condition")
            #print(topic_modelled_words)
            print("the topic name is {}".format(topic_name))
            return topic_modelled_words
        elif is_words_exists_in_file == True:
            print("we are inside the inner most loop")
            topic_modelled_words = read_from_file(TOPIC_WORD_TEXT)

            print(topic_modelled_words)
            topic_modelled_word_list = topic_modelled_words.split(' ')
            print(topic_modelled_word_list)
            topic_modelled_word_list = [i for i in topic_modelled_word_list if i != '']
            print(topic_modelled_word_list)
            #print("scrap_db if == True(else) else condition")
            #print("########")
            #for word in topic_modelled_word_list:
                #print(word)
            #print(topic_modelled_word_list)

            return topic_modelled_word_list

def get_abstract_text(topic_name):
    try:
        url = "http://dbpedia.org/data/"+topic_name+".json"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        abstract_text = ""
        if soup is not None:
            first_level_resource_json_parse = 'http://dbpedia.org/resource/'+topic_name
            json_data = json.loads(str(soup))
            json_data = json_data[first_level_resource_json_parse]['http://dbpedia.org/ontology/abstract']
            #['http://dbpedia.org/ontology/abstract']

            for data in json_data:
                if(data['lang'] == 'en'):
                    print(data['value'])
                    abstract_text = data['value']

        return abstract_text
    except KeyError:
        print("nothing here keyerror")
        return ""


def pass_through_dbpedia_lda(bag_of_nltp_words, syno_list, keyword_list):
    json_response_list = []
    for each_word in keyword_list:
        each_word = each_word.title()
        #print("VKFILE {}".format(is_file_exists))
        lda_words = scrap_dbpedia_ontology(each_word)

        print("the lda words areeeee {}".format(lda_words))
        print("the syno owrds aeer {}".format(syno_list))

        lda_syno_list = []

        for word in lda_words:
            synonyms = wordnet.synsets(word)
            lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
            print(lemmas)
            for word in lemmas:
                lda_syno_list.append(word)


        #matched_word = set(lda_words) & set(syno_list)
        matched_word = set(lda_syno_list) & set(syno_list)

        if(len(matched_word)):
            print("length of this is {}".format(len(matched_word)))
            json_response = {
                "topic_name" : each_word,
                "tweet_word" : matched_word
            }
            json_response_list.append(json_response)

        #print(matched_word)
        #print(lda_words)
    return json_response_list