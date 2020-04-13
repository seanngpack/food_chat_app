# food_chat_app
An application that can be used to find food/restaurants through a chatbot


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
$ (venv) pip install -e .
```

### Running the application
1. make sure you have an .env file at the root location with the database and verification tokens inside it.
2. run ```run_server.py``` 
3. run ```ngrok http 5000 -bind-tls=true``` in your terminal, then copy the https address
4. go to ```https://developers.facebook.com/apps/1270646319787767/messenger/settings/```
5. Click ```Edit Callback URL``` and enter the ```https address/webhook```, and the verification token you should know
6. go to food chat app page and talk to the bot!


### Adding intents
Okay so you wannna do some NLP stuff. 

1. Go to ```food_chat_app/models/nlp/data/intents.json``` and follow the format. 

Be cognizant about these major model characteristics: word frequency is not rewarded, word counts are normalized to either 1 if the word exists, or 0 if it doesn't. Sentence structure is mildly important as lemmatization uses POS tagging. Prepositions seem to have a noticeable impact on performance. And finally, write a bunch of phrases for your intent to get better training.

2. Go to ```food_chat_app/controllers/app_routes.py``` and update the intent_to_strat() function.

3. Go to ```food_chat_app/models/nlp/intent_types.py``` and update with your new intent. 

4. Go to ```food_chat_app/models/nlp/intent_strategy.py``` and update with your new intent. 

5. Finally, run ```run_build_nlp.py```


### running pytest
```pytest -s --disable-pytest-warnings```