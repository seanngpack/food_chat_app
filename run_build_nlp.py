from food_chat_app.models.nlp import build
from food_chat_app.models.nlp.predictor import Predictor

if __name__ == '__main__':
    # build.run()
    predictor = Predictor()
    predictor.predict_intent("find me a restaurant nearby")