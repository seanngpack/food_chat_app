
INSERT INTO food_chat_db.restaurant (restaurant_name,city,star_rating,price_range,reservation,vegan_option,delivery_option,website) 
VALUES (%s,%s,%s,%s,%s,%s,%s,%s) 
ON DUPLICATE KEY
    UPDATE city = VALUES(city), star_rating = VALUES(star_rating), price_range = VALUES(price_range),
    reservation = VALUEs(reservation), vegan_option = VALUES(vegan_option), delivery_option = VALUES(delivery_option),
    website = VALUES(website);