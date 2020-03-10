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
1. run ```main.py``` (By default, the application will run the server and query the database system locally on your machine.)
2. ```ngrok http 5000 -bind-tls=true``` copy the https address
3. go to ```https://developers.facebook.com/apps/1270646319787767/messenger/settings/```
4. Click ```Edit Callback URL``` and enter the https address + ```/webhook```, the verification token is somewhere in the code ;)
5. go to food chat app page and talk to the bot!
