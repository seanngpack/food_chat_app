from food_chat_app.models.nlp import build
from food_chat_app.models.nlp.predictor import Predictor
from food_chat_app.models.nlp import utils


if __name__ == '__main__':
    # build.run()
    predictor = Predictor()
    # predictor.predict_intent("find me a restaurant nearby")
    # predictor.predict_intent("find me a restaurant close to me")
    # predictor.predict_intent("I want to eat Malaysian food")
    # predictor.predict_intent("thank you!")
    predictor.predict_intent("I want to eat at mcdonalds")
    predictor.predict_intent("I want to eat at burger king")
    predictor.predict_intent("what are the reviews at burger king")

    # print(utils.sentence_to_bow_vector("hey dog dog cool", ['hey', 'dog', 'cool', 'cat']))
