import abc

class IntentStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self, entity):
        pass

class ProximityStrategy(IntentStrategy):
    def execute(self, entity):
        print('proximity search' + entity)
        return 'proximity search ' + entity


class FoodTypeStrategy(IntentStrategy):
    def execute(self, entity):
        print('food type search' + entity)
        return 'food type search ' + entity


class RatingStrategy(IntentStrategy):
    def execute(self, entity):
        print('rating search' + entity)
        return 'rating search ' + entity

class NameStrategy(IntentStrategy):
    def execute(self, entity):
        print('name search' + entity)
        return 'name search ' + entity

class RandomStrategy(IntentStrategy):
    def execute(self, entity):
        print('random search' + entity)
        return 'random search ' + entity

class NullStrategy(IntentStrategy):
    def execute(self, entity):
        print('null search' + entity)
        return 'null search ' + entity

class GratitudeStrategy(IntentStrategy):
    def execute(self, entity):
        print('gratitude' + entity)
        return 'gratitude ' + entity