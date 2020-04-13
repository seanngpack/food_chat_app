SELECT distinct(restaurant_name) FROM restaurant 
JOIN foodType ON restaurant.restaurant_id = foodType.restaurant_id 
WHERE food_type = %s;