USE food_chat_db;

DELIMITER $$
CREATE TRIGGER restaurant_update
BEFORE UPDATE ON restaurant
    FOR EACH ROW 
	BEGIN
		SET new.updated = NOW();
	END;
$$
DELIMITER ;