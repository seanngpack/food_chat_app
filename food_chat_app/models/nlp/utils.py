from food_chat_app.models.nlp.entity import NamedEntityChunker
import nltk
from nltk.chunk import conlltags2tree, tree2conlltags
import numpy as np
import os
import pprint

lemmatizer = nltk.WordNetLemmatizer()
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)


def sentence_to_bow_vector(sentence, vocab):
    '''Given a sentence and vocab, create a bag of words vector.
    This disregards frequency counts.

    Example:
        sentence = "hey dog cool cool new"
        vocab = ['hey', 'cool', 'lol']
        bag_vector = np.array(1, 1, 0)

    '''

    seen = []
    words = tokenize_sentence(sentence)
    bag_vector = np.zeros(len(vocab))
    for w in words:
        for i, word in enumerate(vocab):
            if word == w and word not in seen:
                seen.append(word)
                bag_vector[i] += 1
    return bag_vector


def tokenize_sentence(sentence: str):
    '''Tokenize and lemmatize sentence. Lemmatize uses parts of speech tags
    for better lemmetization accuracy. Does not remove stop words from the sentence,
    but I should experiment to see if that impacts performance. Also see what happens
    if we dont ignore the exclamation and question marks.

    '''

    ignore = ['!', '?', ',']

    # stop = set(stopwords.words('english'))
    tokens = nltk.word_tokenize(sentence)
    cleaned_tokens = [t.lower() for t in tokens if t not in ignore]

    lemmatized_tokens = list(map(lemmatize_word, cleaned_tokens))

    return lemmatized_tokens



def lemmatize_word(word):
    '''Given a word, lemmatize it. Uses POS from get_pos() function.

    Args:
        word (str): the word to lemmatize

    Returns:
        the lemmatized word.

    '''

    return lemmatizer.lemmatize(word, get_pos(word))


def get_pos(word):
    '''Given a word, return its part of speech. Returns a noun is the object is not found.

    Args:
        word (str): the word to get the pos for

    Returns:
        the pos of the word.

    '''

    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": nltk.corpus.wordnet.ADJ,
                "N": nltk.corpus.wordnet.NOUN,
                "V": nltk.corpus.wordnet.VERB,
                "R": nltk.corpus.wordnet.ADV}

    return tag_dict.get(tag, nltk.corpus.wordnet.NOUN)


def extract_entity(sentence: str):
    chunker = NamedEntityChunker()
    chunked = chunker.parse(nltk.pos_tag(nltk.word_tokenize(sentence)))
    return chunked


def get_named_entity(chunked):
    '''Given a chunk, get the FIRST labeled chunk, if a labeled chunk
    doesn't exist then get a NNP proper noun, if that doesn't exist
    then return None

    ex. (geo Germany/NNP) -> Germany

    Returns:
        None if there is no entity

    '''

    stop_words = ['restaurant', 'restaurants', 'i']
    # for chunk in chunked:
    #     print(chunk)
    backup = None
    for chunk in chunked:
        if hasattr(chunk, 'label'):
            if str.lower(chunk[0][0]) not in stop_words: 
            #  print(chunk.label(), ' '.join(c[0] for c in chunk))
                return chunk[0][0]
        # backup, if the chunk is a proper noun, singular and not in stop words
        elif chunk[1] == 'NNP':
            backup = chunk[0]
        # second choice backup, jut a singular noun
        elif chunk[1] == 'NN':
            backup = chunk[0]
    return backup
