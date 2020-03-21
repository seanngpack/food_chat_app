import json
from keras.models import load_model
from food_chat_app.models.nlp import utils
import numpy as np
import os
import pickle

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)


class Predictor:
    '''This class represents a predictor model that uses a trained deep learning
    model to generate predictions for the user input.

    '''

    def __init__(self, nlp_model=None):
        if nlp_model == None:
            self.nlp_model = load_model(dir_path + '/data/' + 'nlp_model.h5')
        else:
            self.nlp_model = nlp_model
        self.intents = json.loads(open(dir_path + '/data/' + 'intents.json').read())
        self.vocab = pickle.load(open(dir_path + '/data/' + 'vocab.pkl','rb'))
        self.classes = pickle.load(open(dir_path + '/data/' + 'classes.pkl','rb'))

    def predict_intent(self, sentence):
        tokenized_sentence = utils.sentence_to_bow_vector(sentence, self.vocab)
        
        result = self.nlp_model.predict(tokenized_sentence.reshape(1, -1))

        print(result[0])
        print(self.classes)
        for i in range(0, result[0].size):
            print("intent:" + str(self.classes[i]) + " -- " +
             str(np.around(result[0][i]* 100, decimals=2)) + '%')