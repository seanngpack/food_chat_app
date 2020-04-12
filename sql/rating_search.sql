SELECT * FROM restaurant WHERE restaurant_name = %s;
SELECT * FROM review WHERE restaurant_id = %s ORDER BY RAND() LIMIT 1;