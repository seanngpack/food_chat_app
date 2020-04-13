CREATE DATABASE IF NOT EXISTS `food_chat_db`;

USE food_chat_db;

CREATE TABLE IF NOT EXISTS `restaurant` (
  `restaurant_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `restaurant_name` varchar(255) NOT NULL,
  `city` varchar(255),
  `star_rating` int(11),
  `price_range` VARCHAR(255),
  `reservation` boolean,
  `vegan_option` boolean,
  `delivery_option`     boolean,
  `website`     VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS `user` (
  `user_id`     varchar(255) NOT NULL PRIMARY KEY,
  `first_name`  varchar(255) DEFAULT NULL,
  `last_name`   varchar(255) DEFAULT NULL,
  `city`        varchar(255) DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS `message` (
  `message_id`      int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `user_id`         varchar(255) NOT NULL,
  `message_content`  varchar(255),
  FOREIGN KEY(user_id) REFERENCES user(user_id) 
  
);

CREATE TABLE IF NOT EXISTS `review` (
  `review_id`       int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `restaurant_id`   int(11) NOT NULL,
  `review_content`  varchar(15000),
  `rating`          int(11),
  FOREIGN KEY(restaurant_id) REFERENCES restaurant(restaurant_id) 
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `foodType` (
  `food_type_id`    int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `restaurant_id`   int(11) NOT NULL,
  `food_type`       varchar(255),
  FOREIGN KEY(restaurant_id) REFERENCES restaurant(restaurant_id) 
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `hoursAvailable` (
  `restaurant_id`   int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `monday_hours`    varchar(255),
  `tuesday_hours`   varchar(255),
  `wednesday_hours` varchar(255),
  `thursday_hours`  varchar(255),
  `friday_hours`    varchar(255),
  `saturday_hours`  varchar(255),
  `sunday_hours`    varchar(255),
  FOREIGN KEY(restaurant_id) REFERENCES restaurant(restaurant_id) 
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `menu` (
  `menu_id`         int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `restaurant_id`   int(11),
  FOREIGN KEY(restaurant_id) REFERENCES restaurant(restaurant_id) 
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `dish` (
  `dish_id`     int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `dish_name`   varchar(255),
  `menu_id`     int(11),
  `is_popular`  boolean,
  FOREIGN KEY(menu_id) REFERENCES menu(menu_id) 
  ON DELETE CASCADE ON UPDATE CASCADE
);