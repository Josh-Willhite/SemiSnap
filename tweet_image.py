'''
Created on July 27, 2014

[Copyright (c) 2014 Josh Willhite]
Repository: https://github.com/Josh-Willhite/SemiSnap Email: jwillhite@gmail.com

This program is released under the MIT license. See the COPYING file for terms.
'''

import twitter
import json
from time import strftime
import os
import glob
from time import sleep

def post_vehicle_image():
    print 'getting ready to post'

    creds = json.load(open("/home/josh/.twitter_credentials"))

    api = twitter.Api(consumer_key=creds['consumer_key'], consumer_secret=creds['consumer_secret'],
                      access_token_key=creds['access_token_key'], access_token_secret=creds['access_token_secret'])

    while True:
        images = glob.glob("/home/josh/SemiSnap/images/*.png")
        for i in images:
            print 'posting %s' % i
            api.PostMedia('SemiSnaped at:'  + strftime("%a, %d %b %Y %H:%M:%S"), i)
            os.remove(i)
            sleep(1)





