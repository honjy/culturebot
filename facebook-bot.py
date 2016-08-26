#Hon's First Facebook Bot
#I am very excited about this

import os
import sys
import json
import requests
import requests
import random
from flask import Flask, request

#Getting the New York Times' most popular stories
#Remember to take my API out
response = requests.get("http://api.nytimes.com/svc/mostpopular/v2/mostviewed/all-sections/1.json?offset=20&api-key=YOUR_API_KEY")
data = response.json()
results = data['results']

#Put all the urls for the top 20 most popular stories in a list
#Put all the urls for the photos from the top 20 most popular stories in a list
#Put all the headlines from the top 20 most popular stories in a list

results = data['results']
most_popular_list = []
photo_url_list = []
headline_list = []
for item in results:
    url = item['url']
    most_popular_list.append(url)
    headline = item['title']
    headline_list.append(headline)
    #headline_list = headline_list.append(headline)
    for item_2 in item['media']:
        for item_3 in item_2['media-metadata']:
            if item_3['format'] == 'Jumbo':
                photo_url = item_3['url']
                photo_url_list.append(photo_url)
most_popular_list
photo_url_list
headline_list

#Plucked some dog photos from the internet
#The user will get a random dumb dog photo whenever he or she types "dog"
dogs = ['http://images2.fanpop.com/image/photos/13600000/MORE-SUPER-CUTE-ANIMALS-dogs-13655586-500-402.jpg', 'http://cdn.emgn.com/wp-content/uploads/2015/01/EMGN-Faces-Dogs-Funny-Hilarious-Lol-Pets-Animals-16.jpg', 'http://ci.memecdn.com/16/2067016.jpg', 'https://files.brightside.me/files/news/part_7/75855/552505-650-1452527137-dog-sleeping-bed-funny-104__6051.jpg', 'http://www.ymbnews.com/wp-content/uploads/2015/12/5c97c8c2afa2cde40aa6330266389d90.jpg']
def dog_photo():
    dog = random.choice(dogs)
    return dog

#Here's where it all begins

app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must
    # return the 'hub.challenge' value in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

@app.route('/', methods=['POST'])
def webook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    if 'nytimes' in message_text:
                        send_news(sender_id, "Here are today's most popular stories on the New York Times")

                    elif 'news' in message_text:
                        send_button(sender_id, "Check out Hon's favourite news sites")

                    elif 'dog' in message_text:
                        send_photo(sender_id, "Click on the link to look at a silly dog!")

                    elif 'cat' in message_text:
                        send_message(sender_id, "We don't know what cats are. We hope you meant dog. Try typing 'dog'.")

                    elif 'hello' in message_text:
                        send_message(sender_id, "Why hello to you too! Type 'news' or 'dog' or 'nytimes' to look around and stuff.")

                    else:
                        send_message(sender_id, "Aww geez I didn't understand what you just said. Type 'news' or 'dog' or 'nytimes' to poke around.")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200

def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_photo(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "attachment":{
                "type":"image",
                "payload":{
                    "url":dog_photo(),
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_button(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text": message_text,
                    "buttons":[
                        {
                            "type":"web_url",
                            "url":"http://www.nytimes.com",
                            "title":"The New York Times"
                        },
                        {
                            "type":"web_url",
                            "url":"http://www.vanityfair.com",
                            "title":"Vanity Fair"
                        },
                        {
                            "type":"web_url",
                            "url":"http://www.newyorker.com/",
                            "title":"The New Yorker"
                        }
                    ]
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_news(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"generic",
                    "elements":[
                        {
                            "title":headline_list[0],
                            "image_url":photo_url_list[0],
                            "buttons":[
                            {
                            "type":"web_url",
                            "url":most_popular_list[0],
                            "title": "View Full Story"
                            }
                            ]
                        },
                        {
                            "title":headline_list[1],
                            "image_url":photo_url_list[1],
                            "buttons":[
                            {
                            "type":"web_url",
                            "url":most_popular_list[1],
                            "title": "View Full Story"
                            }
                            ]
                        },
                        {
                            "title":headline_list[2],
                            "image_url":photo_url_list[2],
                            "buttons":[
                            {
                            "type":"web_url",
                            "url":most_popular_list[2],
                            "title": "View Full Story"
                            }
                            ]
                        },
                        {
                            "title":headline_list[3],
                            "image_url":photo_url_list[3],
                            "buttons":[
                            {
                            "type":"web_url",
                            "url":most_popular_list[3],
                            "title": "View Full Story"
                            }
                            ]
                        },
                        {
                            "title":headline_list[4],
                            "image_url":photo_url_list[4],
                            "buttons":[
                            {
                            "type":"web_url",
                            "url":most_popular_list[4],
                            "title": "View Full Story"
                            }
                            ]
                        }
                    ]
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
