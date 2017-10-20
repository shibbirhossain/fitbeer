import datetime
import random
import time

from django.core.serializers import json
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import string
# Importing Gensim
import gensim
from gensim import corpora
from bs4 import BeautifulSoup
import requests
import json


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
    doc_string = ""
    for line in sample_doc:
        doc_string += line
    # compile documents
    doc_complete = [doc_string]


    ps = PorterStemmer()

    stop = set(stopwords.words('english'))
    #string.punctuation = string.punctuation.__add__('rt')
    #string.punctuation = string.punctuation.__add__('http')

    exclude = set(string.punctuation)
    #print(string.punctuation)

    #exclude_twitter_specific_noise
    lemma = WordNetLemmatizer()
    doc_clean = [clean(doc, lemma, stop, exclude).split() for doc in doc_complete]
    print(type(doc_clean))
    twitter_specific_noises = ['rt', 'tweet', 'http']
    # print(type(twitter_specific_noises))


    # print(doc_clean)

    # my_list = [l[0] for l in list]

    doc_clean = doc_clean[0]
    print(doc_clean)

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
    print("after custom noise removal")
    print(doc_clean)

    return doc_clean

def clean(doc, lemma, stop, exclude):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    #punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    #twitter_specific_noise_free = ''.join(ch for ch in punc_free if ch not in exclude_twitter_specific_noise)
    #it was punc_free, made it stop_free only now
    normalized = " ".join(lemma.lemmatize(word) for word in stop_free.split())
    #print(type(normalized))
    return normalized

def get_topic_modelled_words(data, bag_of_words_count):
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

            topic_word = {
                "weight" : weight_value,
                "word" : final_word
            }
            topic_word_list.append(topic_word)

        #print(weighted_word[0])
        #print(weighted_word[1])

    return topic_word_list

def scrap_dbpedia_ontology(topic_name):
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
                    print(data['value'])
                    abstract_text = data['value']
                    total_word_count = sum(len(line.split()) for line in abstract_text)
                    print("total number of words is {}".format(total_word_count))

        topic_modelled_words = get_topic_modelled_words(abstract_text, 10)
        print(topic_modelled_words)
        return abstract_text
    except KeyError:
        print("nothing here keyerror")
        return ""

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
