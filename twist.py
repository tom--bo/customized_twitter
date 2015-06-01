#!/usr/bin/env python
#-*- coding:utf-8 -*-
# http://kimux.net/?p=1378
# next -> add (http://blog.unfindable.net/archives/4257)
# next -> add (http://monowasure78.hatenablog.com/entry/2013/11/26/tweepy%E3%81%A7streaming%E3%82%92%E4%BD%BF%E3%81%86)

import codecs, simplejson, time, guess_language
from tweepy.streaming import StreamListener, Stream
from tweepy.auth import OAuthHandler
from tweepy.api import API
from datetime import timedelta
# from pymongo import Connection

def get_oauth():
    consumer_key='YOUR CONSUMER_KEY'
    consumer_secret='YOUR CONSUMER_SECRET'
    access_key='YOUR ACCESS_KEY'
    access_secret='YOUR ACCESS_SECRET'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return auth
 
class AbstractedlyListener(StreamListener):
    def on_status(self, status):
        try: 
            text = status.text
            if guess_language.guessLanguage(text) == 'ja':
                status.created_at += timedelta(hours=9)
             
                print "-------------------"
                print "tweeted: " + str(status.created_at)
                print text + "\n"
                # col.insert({str(status.created_at): text})
        except Exception, e:
            print >> sys.stderr, 'Encountered ::', e
            pass

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream 

if __name__ == '__main__':

    #con = Connection('localhost')
    #db = con.tweettest
    #col = db.foo

    auth = get_oauth()
    stream = Stream(auth, AbstractedlyListener(), secure=True)
    stream.timeout = None
    # stream.filter(track=["twitter"])
    # stream.filter(languages=['ja'], track=['ja'])
    while True:
        try: 
            stream.sample()
        except Exception:
            time.sleep(20)
            print "sleep 20 sec"
            stream = Stream(auth, AbstractedlyListener(), secure=True)



