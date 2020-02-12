import os
import praw
import time
import tweepy
import urllib.request

#sets the script root path 
root_path = os.path.dirname(__file__)

#tweepy settings
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#praw settings
reddit = praw.Reddit(client_id='CLIENT_ID',
                     client_secret='CLIENT_SECRET', password='PASSWORD',
                     user_agent='USER_AGENT', username='USERNAME')

#scans for saved items on reddit account and then posts it to twitter
while True:
    for item in reddit.user.me().saved():
        url = item.url
        filename = item.id + '.' + url.split('.')[-1]
        title = item.title
        urllib.request.urlretrieve(url, filename)
        api.update_with_media(os.path.join(root_path, filename), title)
        os.remove(filename)
        item.unsave()
        print('POSTED: ' + title)
    time.sleep(60)