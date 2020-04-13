SELECT restaurant_name, star_rating, review_content, city FROM restaurant 
JOIN food_chat_db.review on restaurant.restaurant_id = review.restaurant_id 
WHERE restaurant_name = %s ORDER BY RAND() LIMIT 1;