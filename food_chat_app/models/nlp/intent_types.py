import enum

class IntentType(enum.Enum):
    restaurant_proximity_search = 'restaurant_proximity_search'
    restaurant_rating_search = 'restaurant_rating_search'
    restaurant_search_by_name = 'restaurant_search_by_name'
    restaurant_random_search = 'restaurant_random_search'
    restaurant_null_search = 'restaurant_null_search'
    update_database = 'update_database'
    delete = 'delete'
    greeting = 'greeting'
    gratitude = 'gratitude'
