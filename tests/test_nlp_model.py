from food_chat_app.models.nlp.predictor import Predictor
from food_chat_app.models.nlp.intent_types import IntentType
import pytest


@pytest.fixture(scope="module")
def predictor():
    return Predictor()


def test_proximity(predictor):
    assert predictor.predict_intent('food near me?') == IntentType.restaurant_proximity_search
    assert predictor.predict_intent('restaurants close to me in Malden') == IntentType.restaurant_proximity_search


def test_rating(predictor):
    assert predictor.predict_intent("reviews for Toro") == IntentType.restaurant_rating_search
    assert predictor.predict_intent("Highly reviewed restaurants") == IntentType.restaurant_rating_search


def test_name(predictor):
    assert predictor.predict_intent("I want to eat at wendys") == IntentType.restaurant_search_by_name
    assert predictor.predict_intent("I want to eat chinese food") == IntentType.restaurant_search_by_name
    assert predictor.predict_intent("I want to eat Thai food") == IntentType.restaurant_search_by_name
    assert predictor.predict_intent("I want to eat at a Thai restaurant") == IntentType.restaurant_search_by_name


def test_random(predictor):
    assert predictor.predict_intent("I don't know where to eat") == IntentType.restaurant_random_search
    assert predictor.predict_intent("I am not sure where to eat") == IntentType.restaurant_random_search
    # assert predictor.predict_intent_verbose("I want to eat at a random restaurant") == IntentType.restaurant_random_search
    assert predictor.predict_intent("I would like a random restaurant") == IntentType.restaurant_random_search

def test_update(predictor):
    assert predictor.predict_intent("refresh the database") == IntentType.update_database
    assert predictor.predict_intent("update the database") == IntentType.update_database

def test_delete(predictor):
    assert predictor.predict_intent("delete our messages") == IntentType.delete
    assert predictor.predict_intent("delete our conversation") == IntentType.delete

def test_gratitude(predictor):
    assert predictor.predict_intent("thanks!") == IntentType.gratitude
    assert predictor.predict_intent("cool") == IntentType.gratitude