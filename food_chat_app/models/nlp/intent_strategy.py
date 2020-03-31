import abc

class IntentStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self, entity):
        pass

class ProximityStrategy(IntentStrategy):
    def execute(self, entity):
        print('proximity search')
        return 'proximity search'


class FoodTypeStrategy(IntentStrategy):
    def execute(self, entity):
        print('food type search')
        return 'food type search'


class RatingStrategy(IntentStrategy):
    def execute(self, entity):
        print('rating search')
        return 'rating search'

class NameStrategy(IntentStrategy):
    def execute(self, entity):
        print('name search')
        return 'name search'

class NullStrategy(IntentStrategy):
    def execute(self, entity):
        print('null search')
        return 'null search'

class GratitudeStrategy(IntentStrategy):
    def execute(self, entity):
        print('gratitude')
        return 'gratitude'