# food_chat_app
An application that can be used to find food and restaurants through a chatbot


## Getting Started

These instructions will guide you through the process of setting up the application on your local machine

### Prerequisites

Python 3.x


### Installing

Let's setup your development environment


```
# Installing basic requirements

$ git clone https://github.com/baileyritchie/food_chat_app
$ cd food_chat_app
$ virtualenv venv
$ source venv/bin/activate
$ (venv) pip install -r requirements.txt
```

### Environment variables

When developing locally, create a .env file in your root folder that follows the structure below:
```
ACCESS_TOKEN = "Paste access token here. Check it from the facebook developer account section"
VERIFY_TOKEN = "Make your own activation token and make set it on facebook developer"

DB_NAME = "food_chat_db"
DB_USER = "root"
DB_HOST = "localhost"
DB_PASS = "password here"
```


### Running the application
1. make sure you have an .env file at the root location with the database and verification tokens inside it. Also make sure you have the database schema built. If not run ```run_build_db.py``` and make sure mysql is running on your computer.
2. run ```run_server.py``` 
3. run ```ngrok http 5000 -bind-tls=true``` in your terminal, then copy the https address
4. go to ```https://developers.facebook.com/apps/1270646319787767/messenger/settings/```
5. Click ```Edit Callback URL``` and enter the ```https address/webhook```
6. Enter the verification token you declared in your .env file
7. go to food chat app page and talk to the bot!


### Adding intents
Okay so you wannna do some NLP stuff. 

1. Go to ```food_chat_app/models/nlp/data/intents.json``` and follow the format. 

Be cognizant about these major model characteristics: word frequency is not rewarded, word counts are normalized to either 1 if the word exists, or 0 if it doesn't. Sentence structure is mildly important as lemmatization uses POS tagging. Pay careful attention to how your frame your questions, two intents should not have sentences framed the same way. If that happens maybe you should rethink your approach and might not need two separate intents. Prepositions seem to have a noticeable impact on performance. And finally, write a bunch of phrases for your intent to get better training.

2. Go to ```food_chat_app/controllers/app_routes.py``` and update the intent_to_strat() function.

3. Go to ```food_chat_app/models/nlp/intent_types.py``` and update with your new intent. 

4. Go to ```food_chat_app/models/nlp/intent_strategy.py``` and update with your new intent. 

5. run ```run_build_nlp.py``` if the accuracy is < 70%, then run again or consider changing training data for the model.

6. run ```pytest -s --disable-pytest-warnings``` to see results. Make sure all test cases pass.

### Scraping and updating data
Provided is a ```run_scraper.py``` file you can use to generate a .csv file with data. You can update your database using the csv file, calling the upsert_data() function, or asking your chatbot to do it for you "update database"

### Building your database
Provided ```run_build_db.py``` file builds the schema for you. Otherwise, use the create_all_tables.sql file to make the schema manually.
