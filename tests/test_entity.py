import food_chat_app.models.nlp.utils as utils
import pytest

def test_entity():
    chunk = utils.extract_entity("Restaurants in Quincy")
    named = utils.get_named_entity(chunk)
    assert named == 'Quincy'
    