import twitter
import json
from time import strftime

def post_vehicle_image(image):
    creds = json.load(open("/home/josh/.twitter_credentials"))

    api = twitter.Api(consumer_key=creds['consumer_key'], consumer_secret=creds['consumer_secret'],
                      access_token_key=creds['access_token_key'], access_token_secret=creds['access_token_secret'])

    img = api.PostMedia('SemiSnaped at:'  + strftime("%a, %d %b %Y %H:%M:%S"), )




