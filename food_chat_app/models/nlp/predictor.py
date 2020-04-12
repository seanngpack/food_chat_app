import json
from tensorflow.keras.models import load_model
from food_chat_app.models.nlp import utils
from food_chat_app.models.nlp.intent_types import IntentType
import numpy as np
import os
import pickle

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import nltk
import os
import random
from sklearn.model_selection import train_test_split

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)


class Predictor:
    '''This class represents a predictor model that uses a trained deep learning
    model to generate predictions for the user input. Also has functions to build a 
    new deep learning model.

    '''

    def __init__(self, nlp_model=None):
        if nlp_model == None:
            self.nlp_model = load_model(dir_path + '/data/' + 'nlp_model.h5')
        else:
            self.nlp_model = nlp_model
        self.intents = json.loads(
            open(dir_path + '/data/' + 'intents.json').read())
        self.vocab = pickle.load(open(dir_path + '/data/' + 'vocab.pkl', 'rb'))
        self.classes = pickle.load(
            open(dir_path + '/data/' + 'classes.pkl', 'rb'))

    def predict_intent(self, sentence):
        bow_sentence = utils.sentence_to_bow_vector(sentence, self.vocab)

        result = self.nlp_model.predict(bow_sentence.reshape(1, -1))

        # print(result[0])
        max = 0
        index = 0
        # print(self.classes)
        for i in range(0, result[0].size):
            # print("intent:" + str(self.classes[i]) + " -- " +
            #  str(np.around(result[0][i]* 100, decimals=2)) + '%')
            if result[0][i]*100 > max:
                max = result[0][i]
                index = i
        return IntentType(self.classes[index])

    def build(self):
        '''Build the model!!!

        '''

        vocab, classes, document_map = self._process_intents()
        training = self._build_training_set(vocab, classes, document_map)
        self._build_dl_model(training)

    def _process_intents(self):
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
            pickle.dump(classes, open(
                dir_path + '/data/' + 'classes.pkl', 'wb'))

            return vocab, classes, document_map

    def _build_training_set(self, vocab, classes, document_map):
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

    def _build_dl_model(self, training):
        '''Build and save the DL model using our training set.
        layer 1: 128 neurons, relu
        layer 2: 64 neurons, relu
        layer 3: # neurons = output shape (# of labels), softmax

        Args:
            training (numpy array): numpy array of the training set

        '''
        X = list(training[:, 0])
        y = list(training[:, 1])

        X = np.array(X)
        y = np.array(y)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42)

        model = Sequential()
        model.add(Dense(128, input_shape=(
            X_train[0].size,), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(y_train[0].size, activation='softmax'))

        # Compile model. Stochastic gradient descent with Nesterov accelerated gradient
        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy',
                      optimizer=sgd, metrics=['accuracy'])

        hist = model.fit(X_train, y_train, epochs=200, batch_size=5, verbose=1)
        model.save(dir_path + '/data/' + 'nlp_model.h5', hist)
        scores = model.evaluate(X_test, y_test, verbose=0)
        print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
