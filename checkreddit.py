import sys
import praw
import os
from secrets import *
from slackclient import SlackClient

# Secrets.py defined vars:
#
# reddit_client:  name of praw client
# new_subreddits: list of subreddits to check for new posts 
# hot_subreddits: list of subreddits to check for hot posts
# slack_channel:  slack channel name
# slack_token:    slack secret token 

def slack_message(message, channel):
    sc = SlackClient(slack_token)

    sc.api_call('chat.postMessage', channel=channel, 
                text=message, username='Notify Bot',
                icon_emoji=':robot_face:')

r = praw.Reddit(reddit_client)

print("Logged in")

# Check if log exists
if not os.path.isfile("posts_log.txt"):
    posts_log = []
else:
    with open("posts_log.txt", "r") as f:
        posts_log = f.read()
        posts_log = posts_log.split("\n")
        posts_log = list(filter(None, posts_log))

# Check for new posts
for sub in new_subreddits:
    for submission in r.subreddit(sub).new(limit=10):
        if submission not in posts_log:
            message = 'New post in ' + str(submission.subreddit) + ':\n' + submission.title + '(' + submission.shortlink + ')'
            #print("new post! sending slack message")

            slack_message(message, slack_channel)
            posts_log.append(submission.id)


# Check for new hot posts
for sub in hot_subreddits:
    for submission in r.subreddit(sub).hot(limit=10):
        if submission not in posts_log and submission.score >= 1000:
            message = 'Hot post in ' + str(submission.subreddit) + ':\n' + submission.title + '(' + submission.shortlink + ')'
            #print("hot post! sending slack message")

            slack_message(message, slack_channel)
            posts_log.append(submission.id)

# Update log file with new list
with open("posts_log.txt", "w") as f:
    if len(posts_log) > 500:
        posts_log = posts_log[450:]

    for post_id in posts_log:
        f.write(post_id + "\n")


