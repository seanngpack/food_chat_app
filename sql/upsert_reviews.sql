INSERT INTO food_chat_db.review(restaurant_id,review_content,rating) VALUES (%s,%s,%s)
ON DUPLICATE KEY
    UPDATE review_content = VALUES(review_content), rating = VALUES(rating);