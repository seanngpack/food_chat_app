INSERT INTO food_chat_db.menu(restaurant_id) VALUES (%s) 
ON DUPLICATE KEY UPDATE restaurant_id = restaurant_id;