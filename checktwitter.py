import os
import tweepy
import sys

from slackclient import SlackClient
from secrets import *

# secrets.py defined vars:
#
# tw_consumer_key:    twitter consumer key
# tw_consumer_secret: twitter consumer secret
# tw_access_token:    twitter access token
# tw_access_secret:   twitter access secret
# tw_target_user:     user to monitor tweets from
# tw_keywords:        search strings for tweets
# slack_channel:      slack channel name
# slack_token:        slack secret token

def slack_message(message, channel):
    sc = SlackClient(slack_token)

    sc.api_call('chat.postMessage', channel=channel,
                text=message, username='Notify Bot',
                icon_emoji=':robot_face:')

# Create 0AuthHandler instance
auth = tweepy.OAuthHandler(tw_consumer_key, tw_consumer_secret)
auth.set_access_token(tw_access_token, tw_access_secret)

api = tweepy.API(auth)

#print("Logged In")

# Check if log exists
if not os.path.isfile("twitter_log.txt"):
    last_post_id = ""
    user_timeline = api.user_timeline(screen_name=tw_target_user)
else:
    with open("twitter_log.txt", "r") as f:
        last_post_id = int(f.read())
        user_timeline = api.user_timeline(screen_name=tw_target_user, since_id=last_post_id)

# Parse twitter timeline
for status in reversed(user_timeline):
    if any(word in status.text for word in tw_keywords):
        message = 'VQ: ' + status.text + '(' + status.source + ')'
        #print(message)
        slack_message(message, slack_channel) 

    # Update log file with last post ID
    if status == user_timeline[0]:
        last_post_id = status.id
        with open("twitter_log.txt", "w" ) as f:
            f.write(str(last_post_id))
        #print(status.text)
