from food_chat_app.models.nlp.predictor import Predictor
import pytest


def test_predictoin():
    predictor = Predictor()
    predictor.predict_intent("where is the butter")
    
