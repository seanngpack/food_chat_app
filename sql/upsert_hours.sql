INSERT INTO food_chat_db.hoursAvailable(restaurant_id,monday_hours,tuesday_hours,wednesday_hours,thursday_hours,friday_hours,saturday_hours,sunday_hours) 
VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
ON DUPLICATE KEY
    UPDATE monday_hours = VALUES(monday_hours), tuesday_hours = VALUES(tuesday_hours), wednesday_hours = VALUES(wednesday_hours),
    thursday_hours = VALUES(thursday_hours), friday_hours = VALUES(friday_hours), saturday_hours = VALUES(saturday_hours),
    sunday_hours = VALUES(sunday_hours);