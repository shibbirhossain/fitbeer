import datetime
import random
import time
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
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
    #filename = "coffee.txt"
    #sample_doc = read_from_file(filename)

    #print(sample_doc)
    doc_string = ""
    for line in sample_doc:
        #print(line)
        doc_string += line
    # compile documents
    doc_complete = [doc_string]



    stop = set(stopwords.words('english'))
    #string.punctuation = string.punctuation.__add__('rt')
    #string.punctuation = string.punctuation.__add__('http')

    exclude = set(string.punctuation)
    #print(string.punctuation)

    #exclude_twitter_specific_noise
    lemma = WordNetLemmatizer()
    doc_clean = [clean(doc, lemma, stop, exclude).split() for doc in doc_complete]
    # print(type(doc_clean))
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
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    #twitter_specific_noise_free = ''.join(ch for ch in punc_free if ch not in exclude_twitter_specific_noise)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    #print(type(normalized))
    return normalized