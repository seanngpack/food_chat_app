import enum

class IntentType(enum.Enum):
    restaurant_proximity_search = 'restaurant_proximity_search'
    restaurant_food_type_search = 'restaurant_food_type_search'
    restaurant_rating_search = 'restaurant_rating_search'
    restaurant_search_by_name = 'restaurant_search_by_name'
    restaurant_null_search = 'restaurant_null_search'
    gratitude = 'gratitude'
