from food_chat_app.models.nlp import build_nlp_model
from food_chat_app.models.nlp.predictor import Predictor
from food_chat_app.models.nlp import utils
from food_chat_app.models.nlp import entity


if __name__ == '__main__':
    build_nlp_model.run()