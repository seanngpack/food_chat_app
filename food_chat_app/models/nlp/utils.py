import nltk
import numpy as np

lemmatizer = nltk.WordNetLemmatizer()

# TODO: later I can add a named entity recognizer to pull
# entities from the user query so they can be used in the SQL
# select statement

def process_sentence(sentence: str):
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


def sentence_to_bow_vector(sentence, vocab):
    '''Given a sentence and vocab, create a bow vector

    Example:
        sentence = "hey dog cool new"
        vocab = ['hey', 'cool', 'lol']
        bag_vector = np.array(1, 1, 0)

    '''

    words = process_sentence(sentence)
    bag_vector = np.zeros(len(vocab))
    for w in words:
        for i, word in enumerate(vocab):
            if word == w:
                bag_vector[i] += 1
    return bag_vector
