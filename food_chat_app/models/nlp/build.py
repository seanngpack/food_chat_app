import json
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import nltk
import numpy as np
import pickle
import random
import os
import pprint

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

lemmatizer = nltk.WordNetLemmatizer()


def run():
    '''Build the model!!!

    '''

    vocab, classes, documents = process_intents()
    training = build_training_set(vocab, classes, documents)
    build_dl_model(training)


def process_intents():
    '''Creates the vocab & classes lists and the documents dict

    Returns:
        vocab, classes, documents lists!

    '''

    vocab = []
    classes = []
    documents = {}

    with open(dir_path + '/' + 'intents.json') as data:
        intents = json.load(data)
        for intent in intents['intents']:

            # map tokens to label
            documents.update({intent['intent']: intent['utterances']})
            # add intent to class labels
            if intent['intent'] not in classes:
                classes.append(intent['intent'])

            for utterance in intent['utterances']:
                # tokenize utterance and add to vocab
                u_tokens = process_sentence(utterance)
                vocab.extend(u_tokens)

        vocab = sorted(list(set(vocab)))
        classes = sorted(list(set(classes)))

        # documents = combination between utterances and intents
        print(len(documents), "documents", documents)
        # classes = intents
        print(len(classes), "classes", classes)
        # words = all words, vocabulary
        print(len(vocab), "unique lemmatized words", vocab)

        pickle.dump(vocab, open(dir_path + '/' + 'vocab.pkl', 'wb'))
        pickle.dump(classes, open(dir_path + '/' + '/classes.pkl', 'wb'))

        return vocab, classes, documents


def build_training_set(vocab, classes, documents):
    '''Build the training set for our DL model using vocab, classes
    and documents lists.

    Args:
        vocab (list): vocabulary for the model
        classes (classes): labels for the model
        documents (dict): intent, sentence map
    
    Returns:
        A training set! (numpy array (x, y))

    '''
    # create our training data
    training = []
    i = 0
    for key, value in documents.items():
        for sentence in value:
            bow_vector = sentence_to_bow_vector(sentence, vocab)
            label = np.zeros(len(classes))
            label[i] = 1
            training.append([bow_vector, label])
        i += 1

    # shuffle our features and turn into np.array
    random.shuffle(training)
    training = np.array(training)
    return training

def build_dl_model(training):
    '''Build the DL model using our training set.
    layer 1: 128 neurons, relu
    layer 2: 64 neurons, relu
    layer 3: # neurons = output shape (# of labels), softmax

    Args:
        training (numpy array): numpy array of the training set

    '''

    train_X = list(training[:, 0])
    train_y = list(training[:, 1])
    
    train_X = np.array(train_X)
    train_y = np.array(train_y)
    
    model = Sequential()
    model.add(Dense(128, input_shape=(train_X[0].size,), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(train_y[0].size, activation='softmax'))

    # Compile model. Stochastic gradient descent with Nesterov accelerated gradient 
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    hist = model.fit(train_X, train_y, epochs=200, batch_size=5, verbose=1)
    model.save(dir_path + '/' + 'chatbot_model.h5', hist)


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
