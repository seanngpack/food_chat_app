INSERT INTO food_chat_db.dish(dish_name, menu_id, is_popular) VALUES (%s,%s,%s)
ON DUPLICATE KEY
    UPDATE dish_name = VALUES(dish_name), menu_id = VALUES(menu_id), is_popular = VALUES(is_popular);