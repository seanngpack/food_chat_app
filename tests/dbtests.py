def restaurant_data_tests(obj):
    """
    Queries the restaurant database to check for errors.
    Asks for a restaurant_id from a given name, Asks for restaurant names that don't have vegan options,
    Asks for restaurant names where price range is 3 or 4
    Asks for restaurant names where star_rating is equal to 3
    """
    db = obj
    id_query = "SELECT restaurant_id FROM restaurant WHERE restaurant_name = 'Toro'"
    vegan_query = "SELECT restaurant_name FROM restaurant WHERE vegan_option = TRUE "
    price_query = "SELECT restaurant_name FROM restaurant WHERE price_range = '$$ '"
    rating_query = "SELECT restaurant_name FROM restaurant WHERE star_rating = 4 "
    

    print("Now testing id")
    print(db.query(id_query))
    print("Now testing vegan or not")
    print(db.query(vegan_query))
    print("Now testing prices")
    print(db.query(price_query))
    print("Now testing rating")
    print(db.query(rating_query))

def reviews_data_tests(obj):
    db = obj
    review_id_query = "SELECT review_id FROM review WHERE rating = 3"
    rest_id_query = "SELECT restaurant_id FROM review WHERE rating = 4"
    review_content_query= "SELECT review_content FROM review WHERE review_id = 842"
    
    print("Now checking to see review_id health")
    print(db.query(review_id_query))

    print("Now checking to see if rest_id matches")
    print(db.query(rest_id_query))

    print("Now checking to see content of reviews")
    print(db.query(review_content_query))

