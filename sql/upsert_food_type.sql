INSERT INTO food_chat_db.foodType(restaurant_id,food_type) VALUES (%s,%s)
ON DUPLICATE KEY
    UPDATE food_type = VALUES(food_type);