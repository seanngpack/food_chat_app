import food_chat_app.models.nlp.utils as utils
import pytest

def test_entity():
    chunk = utils.extract_entity("Restaurants in Quincy")
    named = utils.get_named_entity(chunk)
    assert named == 'Quincy'

    chunk = utils.extract_entity("I want to eat at a vegan restaurant")
    named = utils.get_named_entity(chunk)
    assert named == 'vegan'
    
    
    chunk = utils.extract_entity("I want to see reviews for toro")
    named = utils.get_named_entity(chunk)
    assert named == 'toro'

    chunk = utils.extract_entity("I want to eat chinese food")
    named = utils.get_named_entity(chunk)
    assert named == 'chinese'

    chunk = utils.extract_entity("food nearby")
    named = utils.get_named_entity(chunk)
    assert named == None
    