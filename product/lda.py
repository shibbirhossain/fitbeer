import string

import gensim
from gensim import corpora
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords


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

            word = final_word
            topic_word_list.append(word)
    return topic_word_list