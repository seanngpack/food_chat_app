SELECT restaurant_id FROM restaurant WHERE SOUNDEX(restaurant_name) = SOUNDEX(%s);

