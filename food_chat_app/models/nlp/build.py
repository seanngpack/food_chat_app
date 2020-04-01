import json
from food_chat_app.models.nlp import utils
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


def run():
    '''Build the model!!!

    '''

    vocab, classes, document_map = process_intents()
    training = build_training_set(vocab, classes, document_map)
    build_dl_model(training)


def process_intents():
    '''Creates the vocab & classes lists and the document_map dict.
    Also pickles the vocab and classes list to be used later in our model.

    Returns:
        vocab, classes, document_map

    '''

    vocab = []
    classes = []
    document_map = {}

    with open(dir_path + '/data/' + 'intents.json') as data:
        intents = json.load(data)
        for intent in intents['intents']:

            # map tokens to label
            document_map.update({intent['intent']: intent['utterances']})

            if intent['intent'] not in classes:
                classes.append(intent['intent'])

            for utterance in intent['utterances']:
                # tokenize utterance and add to vocab
                u_tokens = utils.tokenize_sentence(utterance)
                vocab.extend(u_tokens)

        vocab = sorted(list(set(vocab)))
        classes = sorted(list(set(classes)))
        document_map = dict(sorted(document_map.items()))
            
        # document_map = combination between utterances and intents
        print(len(document_map), "document_map", document_map)
        # classes = intents
        print(len(classes), "classes", classes)
        # words = all words, vocabulary
        print(len(vocab), "unique lemmatized words", vocab)

        pickle.dump(vocab, open(dir_path + '/data/' + 'vocab.pkl', 'wb'))
        pickle.dump(classes, open(dir_path + '/data/' + 'classes.pkl', 'wb'))

        return vocab, classes, document_map


def build_training_set(vocab, classes, document_map):
    '''Build the training set for our DL model using vocab, classes
    and document_map lists.

    Args:
        vocab (list): vocabulary for the model
        classes (classes): labels for the model
        document_map (dict): intent, sentence map

    Returns:
        A training set! (numpy array (x, y))

    '''
    # create our training data
    training = []
    i = 0
    for key, value in document_map.items():
        for sentence in value:
            bow_vector = utils.sentence_to_bow_vector(sentence, vocab)
            label = np.zeros(len(classes))
            label[i] = 1
            training.append([bow_vector, label])
        i += 1

    # shuffle our features and turn into np.array
    random.shuffle(training)
    training = np.array(training)
    return training


def build_dl_model(training):
    '''Build and save the DL model using our training set.
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
    model.compile(loss='categorical_crossentropy',
                  optimizer=sgd, metrics=['accuracy'])

    hist = model.fit(train_X, train_y, epochs=200, batch_size=5, verbose=1)
    model.save(dir_path + '/data/' + 'nlp_model.h5', hist)
