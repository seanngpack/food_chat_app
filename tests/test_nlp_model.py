from food_chat_app.models.nlp.predictor import Predictor
import pytest


@pytest.fixture(scope="module")
def predictor():
    return Predictor()


# def test_proximity(predictor):
#     predictor.predict_intent_verbose('food near me?')
#     predictor.predict_intent_verbose('restaurants close to me in Malden')


# def test_rating(predictor):
#     predictor.predict_intent_verbose("reviews for Toro")
#     predictor.predict_intent_verbose("Highly reviewed restaurants")


# def test_name(predictor):
#     predictor.predict_intent_verbose("I want to eat at wendys")
#     predictor.predict_intent_verbose("I want to eat chinese food")


# def test_random(predictor):
#     predictor.predict_intent_verbose("I don't know where to eat")
#     predictor.predict_intent_verbose("I am not sure where to eat")

# def test_update(predictor):
#     predictor.predict_intent_verbose("refresh the database")
#     predictor.predict_intent_verbose("update the database")

# def test_delete(predictor):
#     predictor.predict_intent_verbose("delete our messages")
#     predictor.predict_intent_verbose("delete our conversation")

def test_gratitude(predictor):
    predictor.predict_intent_verbose("thanks!")
    predictor.predict_intent_verbose("cool")