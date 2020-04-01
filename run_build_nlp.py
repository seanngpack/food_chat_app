from food_chat_app.models.nlp import build
from food_chat_app.models.nlp.predictor import Predictor
from food_chat_app.models.nlp import utils
from food_chat_app.models.nlp import entity


if __name__ == '__main__':
    # build.run()
    # predictor = Predictor()
    # predictor.predict_intent("find me a restaurant nearby")
    # predictor.predict_intent("find me a restaurant close to me")
    # predictor.predict_intent("I want to eat Malaysian food")
    # predictor.predict_intent("thank you!")
    # predictor.predict_intent("I want to eat at mcdonalds")
    # predictor.predict_intent("I want to eat at burger king")
    # predictor.predict_intent("what are the reviews at burger king")
    # print(utils.tokenize_sentence('I want to eat at Mcdonalds'))
    # entity.train_tagger()
    chunked = utils.extract_entity("I'm going to Mcdonalds this Monday.")
    print(utils.get_named_entity(chunked))

    chunked = utils.extract_entity("I want to eat Chinese food")
    print(utils.get_named_entity(chunked))


    # print(utils.sentence_to_bow_vector("hey dog dog cool", ['hey', 'dog', 'cool', 'cat']))


    # chunker = entity.NamedEntityChunker()

    # print(chunker.parse(pos_tag(word_tokenize(
    #     "I want to eat brazilian food at the restaurant"))))