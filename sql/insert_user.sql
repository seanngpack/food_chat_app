INSERT INTO food_chat_db.user(user_id) VALUES (%s)
ON DUPLICATE KEY UPDATE user_id = user_id;