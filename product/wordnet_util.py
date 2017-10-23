from itertools import chain
from nltk.corpus import wordnet
from .lda import get_topic_modelled_words

def generate_synonym(keyword):
    syno_list = []
    synonyms = wordnet.synsets(keyword)
    lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
    for word in lemmas:
        syno_list.append(word)
    definition = synonyms[0].definition()
    try:
        word_count = 10
        lda_word_list = get_topic_modelled_words(definition, 10)
    except:
        word_count = word_count-1
        lda_word_list = get_topic_modelled_words(definition, word_count)
    for word in lda_word_list:
      syno_list.append(word)

    return syno_list
